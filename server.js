const { fork } = require('child_process');

// get the arguments after "node server.js ..."
const args = process.argv.slice(2)

// the number of sensors is the first argument
const num_sensors = args[0]

let sensors = [];
sensors.length = num_sensors;

console.log('number of sensors', num_sensors);

for (let index = 0; index < num_sensors; index++) {
    sensors[index] = fork('sensor.js')
    
    sensors[index].send({number: index});

    sensors[index].on('message', (msg) => {
        console.log('Message from child ' + index, msg);
    });
}

