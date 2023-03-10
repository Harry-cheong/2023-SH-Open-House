const express = require('express'); 
const bodyParser = require('body-parser');
const fs = require('fs');
const app = express();
const port = 5001;

const clientID = "guiclient1"
const opposingClientID = "guiclient0"
const longestRecognisedClientID = "guiclient0"

let isRobotExecuting = false;
let isGUIExecuting = false;
let currentStatus = "Clear"

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static( __dirname + '/public' ));

const mqtt = require('mqtt')
const url = 'mqtt://58.182.191.109:1883'
const options = {
  // Clean session
  clean: true,
  connectTimeout: 1000,
  // Authentication
  clientId: clientID,
  username: 'algorithm',
  password: '12345'
}
const client = mqtt.connect(url, options)

function logEvent(eventTxt) {
    console.log(eventTxt);
    eventTxtArray = eventTxt.split(" ");
    padding = longestRecognisedClientID.length - eventTxtArray[0].length + 2
    for(var i = 0; i < padding; i++) {
        eventTxtArray[0] += " ";
    }
    var d = new Date(); 
    var datetime = 
    `${d.getDate().toString().padStart(2, '0')}${(d.getMonth()+1).toString().padStart(2, '0')}${d.getFullYear()}-${d.getHours().toString().padStart(2, '0')}${d.getMinutes().toString().padStart(2, '0')}${d.getSeconds().toString().padStart(2, '0')}`
    data = datetime + " " + eventTxtArray.join(" ") + "\n"
    fs.appendFile(`./logs-${clientID}.txt`, data, (err) => {
        if (err) throw err;
    })
}

client.on('connect', function () {
  logEvent(`[Local] ${clientID} connected to MQTT`)
  // Subscribe to a topic
  client.subscribe('Comms', function (err) {
    if (!err) {
        logEvent(`[Local] ${clientID} subscribed to 'Comms'`)
    }
  })
})

client.on('disconnect', function() {
    logEvent(`[Local] ${clientID} disconnected from MQTT`)
})

client.on('error', function(error){
    logEvent(`[Local] ${clientID} could not connect to MQTT. ${error}`);
});

function beginExecution(seq, res) {
    if (isRobotExecuting || isGUIExecuting) {
        currentStatus = "Failed"
        logEvent("[Local] Execution of code failed: Robot busy")
        res.status(200).send("Command failed");
    } else {
        isRobotExecuting = true;
        isGUIExecuting = true;
        currentStatus = "Running";
        logEvent("[Local] Execution of code started");
        res.status(200).send("Command succeeded");
        client.publish('Comms', `[${clientID}] Run ${seq}`)
    }
}

function interruptExecution(res) {
    if (!isGUIExecuting) {
        res.status(200).send("Command redundant")
    } else {
        res.status(200).send("Interrupting execution")
        logEvent("[Local] Execution of code interrupted")
        client.publish('Comms', `[${clientID}] Interrupt execution`)
        currentStatus = "Stopping"
    }
}

// Receive messages
client.on('message', function (topic, message) {
    var txt = message.toString()
    logEvent(txt)
    if (txt === "[Mazerunner] Status: Free") {
        isRobotExecuting = false;
        isGUIExecuting = false;
        currentStatus = "Clear";
    } else if (txt == "[Mazerunner] Received") {
        isRobotExecuting = true;
    } else if (txt.replace(`[${opposingClientID}] Run`) !== txt) {
        isRobotExecuting = true;
    }
})

app.get('/', (req, res) => {
    res.render('index.ejs', {status: currentStatus});
});

app.post('/formdata', (req, res) => {
    beginExecution(req.body.cmd, res);
});

app.post('/interruptexecution', (req, res) => {
    interruptExecution(res)
})

app.get('/runstatus', (req, res) => {
    res.send(currentStatus)
    if(currentStatus === "Failed") {
        currentStatus = "Clear";
    }
})

app.listen(port, () => {
    logEvent(`[Local] Node.JS running on port ${port}`)
});
