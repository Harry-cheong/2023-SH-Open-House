# 2023 SH Open House [STEAM Collective Tech Wing] : Maze Runner

Participants are given a fixed amount of time to complete the objectives of a maze

# Repo Structure

## 1 : GUI

A custom webpage for users to program the robot using blocks

### Setup instructions

1. Install npm and nodejs on your computer
2. With `.../gui-nodejs` as your working directory, run `npm install` in the terminal
3. Edit the `clientID` and `opposingClientID` in the `index.js` file such that both GUIs have different client names.
4. Run `node index.js` in the terminal. (Warning: this command should only be run while the mazerunner robot is in a `free` state)
5. Open `http://localhost:5001` on your browser (preferably Chrome or Firefox, fullscreen if possible)
6. In the event the GUI becomes stuck in a running/stopping state, you may shut off and restart the server (see step 3).

## 2 : Mazerobot

A custom program that automates programming on pybricks to execute files on spike prime

## Dependencies

1. `Selenium`
2. `pyautogui`
3. `paho-mqtt`

## 3 : MQTT Server

A program to start MQTT server to sync GUIs and mazerobot
