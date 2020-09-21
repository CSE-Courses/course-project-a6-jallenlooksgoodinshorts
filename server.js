'use strict';

const express = require('express');

//Setting up the port and host
const PORT = 4000;
const HOST = '0.0.0.0';

//server app directions
const app = express();
app.get('/test1', (req, res) => {
  res.send('Pass test 1');
});

//Listenting on port 4000
app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);

app.get('/', (req, res) => {
  res.send('Replace with home screen');
});


app.get('/home', (req, res) => {
  res.send('Replace with home screen');
});

app.get('/login', (req, res) => {
  res.send('Replace with login screen');
});

app.get('/register', (req, res) => {
  res.send('Replace with registration screen');
});

