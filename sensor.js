let id = 0
let temp_threshold = 0

process.on('message', (msg) => {
    console.log('Message from parent:', msg)
    id = msg["number"]
    temp_threshold = msg["temperature"]
  });

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
    }
    else if(random_event == 9)
    {
        // no temperature available
        temp_measurement = 999
    }

    process.send({ counter: counter++, id_num: id, temp: temp_measurement });
}, 1000);