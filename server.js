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