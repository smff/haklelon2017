const express = require('express');
const app = express();
const bodyParser = require('body-parser');

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }));

// parse application/json
app.use(bodyParser.json());

const auth = {
  username: 'yo',
  password: 'sup',
};

app.get('/', (req, res) => {
  res.send('Hello, Ninel!');
});

app.post('/', (req, res) => {
  res.send(
    (
      auth.username === req.body.username && auth.password === req.body.password
    ) ? auth : {}
  );
});

app.listen(3000);
