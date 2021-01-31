var fs = require('fs')

const parsed_config = JSON.parse(fs.readFileSync('./config.json', 'UTF-8'))

exports.db_config = parsed_config