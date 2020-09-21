var mysql = require('mysq');

//Guide for connecting Node.JS to SQL server found at https://ourcodeworld.com/articles/read/258/how-to-connect-to-a-mysql-database-with-node-js
//Creates connection to mysql database
var connection = mysql.createConnection({
    host     : 'remotemysql.com',
    user     : 't8UFMyPCs3',
    password : 'RZfgggcfAg',
    database : 't8UFMyPCs3'
});

//Checks for conection
connection.connection(function(err) {
    if(err) {
        console.log(err.code);
        console.log(err.fatal);
    }
});