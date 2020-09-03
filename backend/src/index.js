const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const app = express();
const port = 3333;

var amqp = require("amqplib/callback_api");

app.use(cors());

// parse application/json
app.use(bodyParser.json({ limit: "50mb" }));
app.use(bodyParser.urlencoded({ limit: "50mb", extended: true }));

app.post("/upload", (req, res) => {
  const { g } = req.body;

  amqp.connect("amqp://localhost", function (error0, connection) {
    if (error0) {
      throw error0;
    }
    connection.createChannel(function (error1, channel) {
      if (error1) {
        throw error1;
      }
      var queue = "cgne_queue";
      var msg = g;

      channel.assertQueue(queue, {
        durable: true,
      });
      channel.sendToQueue(queue, Buffer.from(msg, "base64"), {
        persistent: true,
      });
      console.log(" [x] Sent '%s'", msg);
    });
    setTimeout(function () {
      connection.close();
      process.exit(0);
    }, 500);
  });

  res.send(g);
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
