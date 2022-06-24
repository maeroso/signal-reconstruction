const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const app = express();
const port = 3333;
const knex = require("./knex/index");

const amqp = require("amqplib/callback_api");

app.use(cors());

// parse application/json
app.use(bodyParser.json({ limit: "50mb" }));
app.use(bodyParser.urlencoded({ limit: "50mb", extended: true }));

const auth = require("./controllers/auth");

app.use("/auth", auth);

app.get("/jobs/:email", async (req, res) => {
  const { email } = req.params;
  try {
    const jobs = await knex.select("*").from("jobs").where("userEmail", email).orderBy('id', 'desc');

    if (jobs.length === 0) {
      res.status(200).send({ message: "Nenhum job encontrado" });
    } else {
      res.status(200).send({ message: "Lista obtida com sucesso", jobs });
    }
  } catch (err) {
    console.log(err);
    res.status(500).send({ message: "Erro ao obter lista de jobs" });
  }
});

app.post("/job/:id", async (req, res) => {
  const { id } = req.params
  const { init_datetime, final_datetime, interactions, status } = req.body

  try {
    await knex('jobs')
      .where('id', '=', id)
      .update({
        status: status,
        iterations: interactions,
        startTime: init_datetime,
        endTime: final_datetime
      })
    res.status(200).send({ message: 'Job atualizado com sucesso' })
  } catch {
    res.status(500).send({ message: 'Não foi possível atualizar job' })
  }
})

app.post("/upload", async (req, res) => {
  const { g, alg, imageSize, increaseRep, email, fileName } = req.body;

  console.log("type", typeof alg);

  if (alg === undefined) {
    res.status(400).send({ message: "Campo alg necessário" });
  }
  if (!(typeof alg === "number")) {
    res.status(400).send({ message: "Campo alg precisa ser número" });
  }
  if (alg !== 1 && alg !== 2 && alg !== 3) {
    res.status(400).send({ message: "Algoritmo inválido" });
  }

  try {
    const id = await knex("jobs").insert({
      userEmail: email.toLowerCase(),
      originalSignalName: fileName,
      algorithm: alg,
      signalIncreaseRep: increaseRep,
      status: 1,
      pixelSize: imageSize,
      createdAt: new Date(),
      updatedAt: new Date(),
    }).returning('id');
    const queue = "worker";

    amqp.connect("amqp://0.0.0.0", function (error0, connection) {
      if (error0) {
        throw error0;
      }
      connection.createChannel(function (error1, channel) {
        if (error1) {
          throw error1;
        }

        const msg = {
          index: id[0],
          algorithm: alg,
          signal_array: g,
          image_size: imageSize
        };

        channel.assertQueue(queue, {
          durable: true,
        });
        channel.sendToQueue(queue, Buffer.from(JSON.stringify(msg)), {
          persistent: true,
        });
        console.log(" [x] Sent '%s'", msg);
        res.send(msg);
      });
      setTimeout(function () {
        connection.close();
      }, 500);
    });
    res.status(200).send({ message: "Sinal na fila de jobs" });
  } catch {
    res.status(500).send({ message: "Erro ao processar sinal" });
  }
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
