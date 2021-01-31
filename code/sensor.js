const mysql = require('mysql');
const { database } = require('./config');

process.on('message', (msg) => {
    console.log('Message from parent:', msg)
    id = msg["number"]
    temp_threshold = msg["temperature"]
  });

const cfg = require("./config")

const db_connection = mysql.createConnection({
    user: cfg.database.user,
    host: cfg.database.host,
    password:cfg.database.password,
    database: cfg.database.database
});

db_connection.connect((err) => {
    if (err) {
        console.log('Error connecting to database: ' + err );
        return
    }
    console.log('Sensor-' + id + ' connected to database')
})

let id = 0
let temp_threshold = 0

let counter = 0;

let alarm_count = 0
let error_count = 0

// These events happen once every ten seconds since interval is in milliseconds
setInterval(() => {
    // Theses values should be within [-2, 2)
    let temp_offset = (Math.random() * 4) - 2
    let temp_measurement = temp_threshold + temp_offset

    // should be within 0-9
    let random_event = Math.floor(Math.random() * 10)

    if (random_event == 0)
    {
        // temperature spike occured
        
        // should be between [1,8)
        spike = (Math.random() * 7.0) + 1.0

        let spike_direction = Math.floor(Math.random() * 2)

        if (spike_direction > 0)
        temp_measurement += spike
        else
        temp_measurement -= spike
        
        if (Math.abs(temp_measurement - temp_threshold) > 5)
            alarm_count += 1
    }
    else if(random_event == 9)
    {
        // no temperature available
        temp_measurement = 999
        error_count += 1
    }

    var insert_into_db = "INSERT INTO sensors (sensorId, timestamp, temperature, alarm_count, error_count) VALUES ?";
    
    let date = (new Date()).toLocaleString("en-US")

    var values = [
        [id, date, temp_measurement, alarm_count, error_count]
    ];
    db_connection.query(insert_into_db, [values], function (err, result) {
        if (err) console.log(err);
        // console.log("Number of records insert: " + result.affectedRows);
    })
    process.send({ id_num: id, date: date,  temp: temp_measurement, alarms: alarm_count, errors: error_count });
}, 10000);
