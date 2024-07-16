const os = require("os");
// const dns = require("dns").promises;
const { program: optionparser } = require("commander");
const { Kafka } = require("kafkajs");
// const mariadb = require("mariadb");
const weaviate = require("weaviate-client").default;
const { dataType } = require("weaviate-client");
// const MemcachePlus = require("memcache-plus");
const express = require("express");
const fs = require("fs");
const { parse } = require("csv-parse");
//const { readCSV } = require("./populate_weaviate");

const app = express();
//const cacheTimeSecs = 15;

// -------------------------------------------------------
// Command-line options (with sensible defaults)
// -------------------------------------------------------

let options = optionparser
 .storeOptionsAsProperties(true)
 // Web server
 .option("--port <port>", "Web server port", 3030)
 // Kafka options
 .option(
  "--kafka-broker <host:port>",
  "Kafka bootstrap host:port",
  "bachmatch-kafka-bootstrap:9092"
 )
 .option(
  "--kafka-topic-tracking <topic>",
  "Kafka topic to tracking data send to",
  "bachmatch"
 )
 .option(
  "--kafka-client-id < id > ",
  "Kafka client ID",
  "tracker-" + Math.floor(Math.random() * 100000)
 )
 .option(
  "--weaviate-service-host <host>",
  "Weaviate out-facing service host",
  "bachmatch-weaviate"
 )
 .option(
  "--weaviate-service-port <port>",
  "Weaviate out-facing service port",
  "80"
 )
 .option(
  "--weaviate-grpc-service-host <host>",
  "Weaviate gRPC out-facing service host",
  "bachmatch-weaviate-grpc"
 )
 .option(
  "--weaviate-grpc-service-port <port>",
  "Weaviate gRPC out-facing service port",
  "50051"
 )
 // Misc
 .parse()
 .opts();

// -------------------------------------------------------
// Database Configuration
// -------------------------------------------------------

const weavOptions = {
 httpHost: options.weaviateServiceHost,
 httpPort: options.weaviateServicePort,
 httpSecure: false,
 grpcHost: options.weaviateGrpcServiceHost,
 grpcPort: options.weaviateGrpcServicePort,
 grpcSecure: false,
};

// -------------------------------------------------------
// Kafka Configuration
// -------------------------------------------------------

// Kafka connection
const kafka = new Kafka({
 clientId: options.kafkaClientId,
 brokers: [options.kafkaBroker],
 retry: {
  retries: 0,
 },
});

const producer = kafka.producer();
// End

// Send tracking message to Kafka
async function sendTrackingMessage(data) {
 //Ensure the producer is connected
 await producer.connect();

 //Send message
 let result = await producer.send({
  topic: options.kafkaTopicTracking,
  messages: [{ value: JSON.stringify(data) }],
 });

 console.log("Send result:", result);
 return result;
}
// End

// -------------------------------------------------------
// HTML helper to send a response to the client
// -------------------------------------------------------

function sendResponse(res, html, cachedResult) {
 res.send(`<!DOCTYPE html>
		<html lang="en">
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>BachMatch - Scientific Tinder</title>
			<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mini.css/3.0.1/mini-default.min.css">
		</head>
		<body>
			<h1>Welcome to BachMatch</h1>
			<p>
			</p>
			${html}
			<hr>
			<h2>Information about the generated page</h4>
			<ul>
				<li>Server: ${os.hostname()}</li>
				<li>Date: ${new Date()}</li>
			</ul>
		</body>
	</html>
	`);
}

// -------------------------------------------------------
// Start page
// -------------------------------------------------------

// Get list of missions (from cache or db)
async function getExampleAbstracts() {
 return 0;
}

// Get popular missions (from db only)
async function getSuperVisors(maxCount) {
 return 0;
}

// Return HTML for start page
app.get("/", (req, res) => {
 const html = "<h1>Success!</h1>";
 sendResponse(res, html);
});

// -------------------------------------------------------
// Get a specific mission (from cache or DB)
// -------------------------------------------------------

async function getSingleAbstract(abstract_id) {
 return 0;
}

app.get("/examples/:abstract_id", (req, res) => {
 let abstract_id = req.params["abstract_id"];

 // Send the tracking message to Kafka
 sendTrackingMessage({
  abstract_id,
  timestamp: Math.floor(new Date() / 1000),
 })
  .then(() =>
   console.log(
    `Sent abstract=${abstract_id} to kafka topic=${options.kafkaTopicTracking}`
   )
  )
  .catch((e) => console.log("Error sending to kafka", e));

 // Send reply to browser
 // get a single abstract and show to user
});

async function getStuff() {
 const client = await weaviate.connectToCustom(weavOptions);
 console.log("connected to weaviate");
 client.collections.exists("scientific_supervisors").then(function (boolean) {
  if (boolean) {
   console.log("collection exists");
  } else {
   console.log("collection does not exists");
   createCollections(client);
  }
 });
 // if (!supes) {
 //  // createCollections(client);
 //  const rows = await readStreamCSV("supervisors_information.csv");
 //  console.log(rows);
 // } else {
 //  console.log(supes);
 // }
}

async function readStreamCSV(filename) {
 const data = [];
 fs
  .createReadStream(filename)
  .pipe(
   parse({
    delimiter: ",",
    columns: true,
    ltrim: true,
   })
  )
  .on("data", function (row) {
   data.push(row);
  })
  .on("error", function (error) {
   console.log(error.message);
  })
  .on("end", function () {
   console.log("parsed csv data:");
   console.log(data);
  });
 return data;
}

async function createCollections(client) {
 client.collections.create({
  name: "scientific_supervisors",
  properties: [
   { name: "supe_id", dataType: dataType.TEXT },
   { name: "fname", dataType: dataType.TEXT },
   { name: "lname", dataType: dataType.TEXT },
   { name: "statement", dataType: dataType.TEXT },
   { name: "expertise", dataType: dataType.TEXT },
   { name: "pre_cluster", dataType: dataType.INT },
  ],
 });
 client.collections.create({
  name: "example_abstract",
  properties: [
   { name: "abstract_id", dataType: dataType.TEXT },
   { name: "title", dataType: dataType.TEXT },
   { name: "abstract", dataType: dataType.TEXT },
   { name: "topic", dataType: dataType.TEXT },
   { name: "pre_cluster", dataType: dataType.INT },
  ],
 });

 client.collections.create({
  name: "user_abstract",
  properties: [
   { name: "abstract_id", dataType: dataType.TEXT },
   { name: "title", dataType: dataType.TEXT },
   { name: "abstract", dataType: dataType.TEXT },
   { name: "topic", dataType: dataType.TEXT },
  ],
 });
 return 0;
}

// -------------------------------------------------------
// Main method
// -------------------------------------------------------

app.listen(options.port, function () {
 console.log("Node app is running at (probably in kubernetes cluster)");
});

getStuff();
