import { connect } from "amqplib/callback_api";

connect("amqp://localhost", function (err0, connection) {
  if (err0) throw err0;
  connection.createChannel(function (err1, channel) {
    if (err1) {
      throw err1;
    }
    const queue = "hello";
    const msg = "Hello world";

    channel.assertQueue(queue, { durable: false });
    channel.sendToQueue(queue, Buffer.from(msg));
    console.log(" [x] Sent %s", msg);
  });
  setTimeout(() => {
      connection.close();
      process.exit(0)
  }, 500);
});