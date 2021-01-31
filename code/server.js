const { fork } = require('child_process')

var mysql = require('mysql');

const cfg = require("./config")

const db_connection = mysql.createConnection({
    host: cfg.database.host,
    user: cfg.database.user,
    password:cfg.database.password,
});

db_connection.connect(function(err) {
    if (err) {
        console.log(err);
        return;
    }
    console.log("Connected!");

    const create_db = "CREATE DATABASE IF NOT EXISTS sensor_db";

    db_connection.query(create_db, function (err, result) {
        if (err) throw err;
        console.log("Database created!");
    });

    db_connection.changeUser({
        database: 'sensor_db'
    }, (err) => {
        if (err) {
            console.log('Error in changing database ', err);
            return;
        }
    });

    const clear_db_table = "DROP TABLE IF EXISTS sensors";
    db_connection.query(clear_db_table, function (err, result) {
        if (err) throw err;
        console.log("Table deleted");
    });

    var sql = "CREATE TABLE sensors (id INT AUTO_INCREMENT PRIMARY KEY, sensorId INTEGER(255), timestamp TEXT, temperature REAL, alarm_count INTEGER, error_count INTEGER)";
    db_connection.query(sql, function (err, result) {
        if (err) throw err;
        console.log("Table created");
    });

});

// get the arguments after "node server.js ..."
const args = process.argv.slice(2)

// the number of sensors is the first argument
const num_sensors = args[0]

// Initialize array for sensors
let sensors = [];
sensors.length = num_sensors

console.log('number of sensors', num_sensors)

// temperature to vary thresholds around
const temp_threshold = 40.0

for (let index = 0; index < num_sensors; index++) {
    sensors[index] = fork('sensor.js')

    let sensor_temp = temp_threshold

    // value of offset should be 0 or 1 since random returns
    // between [0,1)
    let sensor_offset = Math.floor(Math.random() * 2)

    if (sensor_offset > 0)
        sensor_temp += 5.0
    else
        sensor_temp -= 5.0

    // pass configuration to the forked sensor process to initialize
    sensors[index].send({number: index, temperature: sensor_temp})

    sensors[index].on('message', (msg) => {
        console.log('Message from child ' + index, msg)
    });
}

