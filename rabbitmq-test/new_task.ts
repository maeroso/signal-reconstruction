import { connect } from "amqplib/callback_api";

connect("amqp://localhost", function (err0, connection) {
  if (err0) throw err0;
  connection.createChannel(function (err1, channel) {
    if (err1) {
      throw err1;
    }
    const queue = "task_queue";
    const msg = process.argv.slice(2).join(" ") || "Hello world!";

    channel.assertQueue(queue, { durable: true });
    channel.sendToQueue(queue, Buffer.from(msg), { persistent: true });
    console.log(" [x] Sent %s", msg);
  });
  setTimeout(() => {
    connection.close();
    process.exit(0);
  }, 500);
});
