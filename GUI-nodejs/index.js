const express = require('express'); 
const bodyParser = require('body-parser');
const fs = require('fs');
const app = express();
const port = 5001;

let isRobotInFreeState = true;
let isGUIExecutionQueued = false;
let actions = [];
let currentExecutionStep = 0;
let currentStatus = "Clear"
let isAwaitingTermination = false;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static( __dirname + '/public' ));

const mqtt = require('mqtt')
const url = 'mqtt://58.182.191.109:1883'
const options = {
  // Clean session
  clean: true,
  connectTimeout: 4000,
  // Authentication
  clientId: 'nodejs-client',
  username: 'algorithm',
  password: '12345',
}
const client = mqtt.connect(url, options)

function logEvent(eventTxt) {
    console.log(eventTxt);
    eventTxtArray = eventTxt.split(" ");
    padding = "[nodejs-client]".length - eventTxtArray[0].length
    for(var i = 0; i < padding; i++) {
        eventTxtArray[0] += " ";
    }
    fs.writeFile('./logs.txt', data, (err) => {
        if (err) throw err;
    })
}

client.on('connect', function () {
  console.log('[Local] nodejs-client connected to MQTT')
  // Subscribe to a topic
  client.subscribe('Comms', function (err) {
    if (!err) {
        console.log("[Local] nodejs-client subscribed to 'Comms'")
    }
  })
})

client.on('disconnect', function() {
    console.log('[Local] nodejs-client disconnected from MQTT')
})

client.on('disconnected', function() {
    console.log('[Local] nodejs-client disconnected from MQTT')
})

client.on('error', function(error){
    console.log("[Local] nodejs-client could not connect to MQTT. Error: " + error);
});

function beginExecution(seq, res) {
    if (!isRobotInFreeState) {
        res.redirect(301, `http://localhost:${port}/`);
        currentStatus = "Failed"
        console.log("[Local] Execution of code failed: Robot busy")
    } else {
        currentExecutionStep = 0
        isGUIExecutionQueued = true;
        actions = seq.split('-');
        res.redirect(301, `http://localhost:${port}/`);
        currentStatus = "Running"
        console.log("[Local] Execution of code started")
        sendCommand()
    }
}

function sendCommand() {
    client.publish('Comms', `[nodejs-client] Run ${actions[currentExecutionStep]}`)
    if (currentExecutionStep === actions.length-1) {
        isGUIExecutionQueued = false
        isAwaitingTermination = true
    }
}

// Receive messages
client.on('message', function (topic, message) {
    var txt = message.toString()
    console.log(txt)
    if (txt === "[Mazerunner] Status: Free") {
        isRobotInFreeState = true
        if (isGUIExecutionQueued) {sendCommand();}
        else if (isAwaitingTermination) {
            isAwaitingTermination = false;
            currentStatus = "Clear";
            console.log("[Local] Execution of code ended")
        }
    } else if (txt === "[Mazerunner] Status: Occupied") {
        isRobotInFreeState = false;
    } else if (txt == "[Mazerunner] Command Received. Running...") {
        currentExecutionStep += 1;
    }
})

app.get('/', (req, res) => {
    res.render('index.ejs', {status: currentStatus});
    if (currentStatus == "Failed") {
        currentStatus = "Clear";
    }
});

app.post('/formdata', (req, res) => {
    beginExecution(req.body.name, res);
});

app.listen(port, () => {
    console.log(`[Local] Node.JS running on port ${port}`); 
});
