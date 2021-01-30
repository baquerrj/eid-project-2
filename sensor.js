let id = 0
let temp_threshold = 0

process.on('message', (msg) => {
    console.log('Message from parent:', msg)
    id = msg["number"]
    temp_threshold = msg["temperature"]
  });

let counter = 0;

setInterval(() => {
process.send({ counter: counter++, id_num: id, temp: temp_threshold });
}, 1000);