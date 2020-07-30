import { connect } from "amqplib/callback_api";

connect("amqp://localhost", function (err0, connection) {
  if (err0) throw err0;
  connection.createChannel(function (err1, channel) {
    if (err1) {
      throw err1;
    }
    const queue = "task_queue";

    channel.assertQueue(queue, { durable: true });
    channel.prefetch(1);

    channel.consume(
      queue,
      function (msg) {
        let secs = msg.content.toString().split(".").length - 1;

        console.log(" [x] Received %s", msg.content.toString());
        setTimeout(() => {
          console.log(" [x] Done");
          channel.ack(msg);
        }, secs * 1000);
      },
      { noAck: false }
    );
  });
});
