const express = require('express');
const app = express();
const fs = require('fs');
const bodyParser = require('body-parser');

const auth = {
  login: 'yo',
  password: 'sup',
};

const dbFile = __dirname + '/config.txt';

app.set('views', __dirname);
app.set('view engine', 'pug');
app.use(express.static(__dirname + '/static'));

app.use(bodyParser.urlencoded());
app.use(bodyParser.json());

app.get('/', (req, res) => {
  fs.readFile(dbFile, (err, data) => {
    if (err) {
      throw err;
    }
    res.render('index', { config: data });
  });
});

app.post('/', (req, res) => {
  let config = req.body.config;
  if (req.body.login !== auth.login && req.body.password !== auth.password) {
    res.render('index', { error: true, config: config });
  } else {
    fs.writeFile(dbFile, config, (err) => {
      if (err) {
        throw err;
      }
      res.render('index', { config: config });
    });

  }
});

app.listen(3000);
