const { fork } = require('child_process')

const sensor = fork('sensor.js')

sensor.on('message', (msg) => {
    console.log('Message from child', msg);
});

sensor.send({hello: 'world'});