const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const app = express();
const port = 3333;

const amqp = require("amqplib/callback_api");

app.use(cors());

// parse application/json
app.use(bodyParser.json({limit: "50mb"}));
app.use(bodyParser.urlencoded({limit: "50mb", extended: true}));

app.post("/upload", (req, res) => {
    const {g, alg} = req.body;

    console.log('type', typeof alg)

    if (alg === undefined) {
        res.status(400).send({message: 'Campo alg necessário'})
    }
    if (!(typeof alg === 'number')) {
        res.status(400).send({message: 'Campo alg precisa ser número'})
    }
    if (alg !== 0 && alg !== 1) {
        res.status(400).send({message: 'Algoritmo inválido'})
    }

    const queue = "worker"

    amqp.connect("amqp://0.0.0.0", function (error0, connection) {
        if (error0) {
            throw error0;
        }
        connection.createChannel(function (error1, channel) {
            if (error1) {
                throw error1;
            }

            const msg = {
                signalArray: g,
                algorithmType: alg
            }

            channel.assertQueue(queue, {
                durable: true,
            });
            channel.sendToQueue(queue, Buffer.from(JSON.stringify(msg)), {
                persistent: true,
            });
            // console.log(" [x] Sent '%s'", msg);
            res.send(msg);
        });
        setTimeout(function () {
            connection.close();

        }, 500);
    });
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});
