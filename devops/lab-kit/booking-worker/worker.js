// booking-worker — long-polls SQS and "sends a reminder" for each booking.created message.
//   QUEUE_URL=https://sqs.ap-southeast-1.amazonaws.com/<acct>/<queue>   WORK_MS=200
import { SQSClient, ReceiveMessageCommand, DeleteMessageCommand } from "@aws-sdk/client-sqs";

const sqs = new SQSClient({});
const QUEUE_URL = process.env.QUEUE_URL;
const WORK_MS = Number(process.env.WORK_MS || 200);
let running = true;
const log = (level, msg, extra = {}) =>
  console.log(JSON.stringify({ ts: new Date().toISOString(), level, msg, service: "booking-worker", ...extra }));

if (!QUEUE_URL) { log("error", "QUEUE_URL is required"); process.exit(1); }
process.on("SIGTERM", () => { running = false; log("info", "SIGTERM: finishing current batch"); });

while (running) {
  const out = await sqs.send(new ReceiveMessageCommand({ QueueUrl: QUEUE_URL, MaxNumberOfMessages: 10, WaitTimeSeconds: 20 }));
  for (const m of out.Messages ?? []) {
    const evt = JSON.parse(m.Body);
    await new Promise((r) => setTimeout(r, WORK_MS));                 // pretend to send an SMS
    log("info", "reminder sent", { bookingId: evt.booking?.id });
    await sqs.send(new DeleteMessageCommand({ QueueUrl: QUEUE_URL, ReceiptHandle: m.ReceiptHandle })); // ack only after work
  }
}
log("info", "worker stopped cleanly");
