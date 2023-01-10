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
let isExecutionStopping = false;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static( __dirname + '/public' ));

const mqtt = require('mqtt')
const url = 'mqtt://58.182.191.109:1883'
const options = {
  // Clean session
  clean: true,
  connectTimeout: 1000,
  // Authentication
  clientId: 'nodejs-client',
  username: 'algorithm',
  password: '12345'
}
const client = mqtt.connect(url, options)

function logEvent(eventTxt) {
    console.log(eventTxt);
    eventTxtArray = eventTxt.split(" ");
    padding = "[nodejs-client]".length - eventTxtArray[0].length
    for(var i = 0; i < padding; i++) {
        eventTxtArray[0] += " ";
    }
    var d = new Date(); 
    var datetime = 
    `${d.getDate().toString().padStart(2, '0')}${(d.getMonth()+1).toString().padStart(2, '0')}${d.getFullYear()}-${d.getHours().toString().padStart(2, '0')}${d.getMinutes().toString().padStart(2, '0')}${d.getSeconds().toString().padStart(2, '0')}`
    data = datetime + " " + eventTxtArray.join(" ") + "\n"
    fs.appendFile('./logs.txt', data, (err) => {
        if (err) throw err;
    })
}

client.on('connect', function () {
  logEvent('[Local] nodejs-client connected to MQTT')
  // Subscribe to a topic
  client.subscribe('Comms', function (err) {
    if (!err) {
        logEvent("[Local] nodejs-client subscribed to 'Comms'")
    }
  })
})

client.on('disconnect', function() {
    logEvent('[Local] nodejs-client disconnected from MQTT')
})

client.on('error', function(error){
    logEvent("[Local] nodejs-client could not connect to MQTT. " + error);
});

function beginExecution(seq, res) {
    if (!isRobotInFreeState || isGUIExecutionQueued) {
        logEvent("[Local] Execution of code failed: Robot busy")
        res.status(500).send("Command failed");
    } else {
        currentExecutionStep = 0
        isGUIExecutionQueued = true;
        actions = seq.split('-');
        currentStatus = "Running"
        logEvent("[Local] Execution of code started")
        res.status(200).send("Command succeeded");
        sendCommand()
    }
}

function interruptExecution(res) {
    if (!isGUIExecutionQueued && isRobotInFreeState) {
        res.status(200).send("Command redundant")
    } else {
        res.status(200).send("Interrupting execution")
        logEvent("[Local] Execution of code interrupted")
        client.publish('Comms', `[nodejs-client] Interrupt execution`)
        currentStatus = "Stopping"
        isExecutionStopping = true
        if (isRobotInFreeState) {
            currentStatus = "Clear"
            isGUIExecutionQueued = false
            isExecutionStopping = false
        }
    }
}

function sendCommand() {
    if (currentExecutionStep === actions.length) {
        isGUIExecutionQueued = false;
        currentStatus = "Clear";
        logEvent("[Local] Execution of code ended")
    } else if (!isExecutionStopping) {
        client.publish('Comms', `[nodejs-client] Run ${actions[currentExecutionStep]}`)
        isRobotInFreeState = false;
    }
}

// Receive messages
client.on('message', function (topic, message) {
    var txt = message.toString()
    logEvent(txt)
    if (txt === "[Mazerunner] Status: Free") {
        isRobotInFreeState = true
        if (isExecutionStopping) {
            isGUIExecutionQueued = false
            isExecutionStopping = false
            currentStatus = "Clear"
        } else if (isGUIExecutionQueued) {
            sendCommand();
        }
        
    } else if (txt === "[Mazerunner] Status: Occupied") {
        isRobotInFreeState = false;
    } else if (txt == "[Mazerunner] Command Received. Running...") {
        isRobotInFreeState = false;
        currentExecutionStep += 1;
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
    if (currentStatus == "Failed") {
        currentStatus = "Clear";
    }
})

app.listen(port, () => {
    logEvent(`[Local] Node.JS running on port ${port}`)
});
