const { fork } = require('child_process')

var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "sensor",
  password: "balderdash"
});

con.connect(function(err) {
    if (err) {
        console.log(err);
        return;
    }
    console.log("Connected!");

    var sql = "CREATE DATABASE IF NOT EXISTS sensor_db";
    con.query(sql, function (err, result) {
        if (err) throw err;
        console.log("Database created!");
    });

    con.changeUser({
        database: 'sensor_db'
    }, (err) => {
        if (err) {
            console.log('Error in changing database ', err);
            return;
        }
    });

    var sql = "DROP TABLE IF EXISTS sensors";
    con.query(sql, function (err, result) {
        if (err) throw err;
        console.log("Table deleted");
    });

    var sql = "CREATE TABLE sensors (id INT AUTO_INCREMENT PRIMARY KEY, sensorId INTEGER(255), temperature DOUBLE(5,3))";
    con.query(sql, function (err, result) {
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

