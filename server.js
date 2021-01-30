const { fork } = require('child_process');

// get the arguments after "node server.js ..."
const args = process.argv.slice(2)

// the number of sensors is the first argument
const num_sensors = args[0]

let sensors = [];
sensors.length = num_sensors

console.log('number of sensors', num_sensors)

const temp_threshold = 40.0

for (let index = 0; index < num_sensors; index++) {
    sensors[index] = fork('sensor.js')
    
    let sensor_temp = temp_threshold

    sensors[index].send({number: index, temperature: sensor_temp})

    sensors[index].on('message', (msg) => {
        console.log('Message from child ' + index, msg)
    });
}

