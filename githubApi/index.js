var request = require('request');

var options = {
  url: 'https://api.github.com/repos/smff/haklelon2017/merges',
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'token 19b339e826c6268e03365c0d4e7b8fd3cf50d9e3',
    'User-Agent': 'Awesome-Octocat-App',
  }
};

request(options, callback);

function callback(error, response, body) {
  console.log(response);
  console.log(body);
}
