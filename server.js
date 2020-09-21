'use strict';

const express = require('express');

//Setting up the port and host
const PORT = 4000;
const HOST = '0.0.0.0';

//server app directions
const app = express();

//Home Screen
app.get('/', (req, res) => {
  res.send('Replace with home screen');
});
app.get('/home', (req, res) => {
  res.send('Replace with home screen');
});

//Login page
app.get('/login', (req, res) => {
  res.send('Replace with login screen');
});
//Registration Page
app.get('/register', (req, res) => {
  res.send('Replace with registration screen');
});



//Listenting on port 4000
app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);

