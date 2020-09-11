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

    const queue = alg === 0 ? 'cgne_queue' : 'fista_queue'

    amqp.connect("amqp://localhost", function (error0, connection) {
        if (error0) {
            throw error0;
        }
        connection.createChannel(function (error1, channel) {
            if (error1) {
                throw error1;
            }
            // var queue = queue;
            let msg = /* '[' */ g.join() /*.toString().replace(/,\s*$/, "]"); */

            while (true) {
                if (msg.substring(msg.length - 1, msg.length) === ',') {
                    msg = msg.substring(0, msg.length - 1);
                } else {
                    break;
                }
            }


            channel.assertQueue(queue, {
                durable: true,
            });
            channel.sendToQueue(queue, Buffer.from(msg), {
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
