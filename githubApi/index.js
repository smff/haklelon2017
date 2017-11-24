const axios = require('axios');
const moment = require('moment');

axios.post(
  'https://api.github.com/repos/smff/haklelon2017/merges',
  {
    base: 'master',
    head: 'dev',
    commit_message: 'hello from ninel ' + moment().toISOString(),
  },
  {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'token abd061e1067ad3876091424fd17cecffd4c3f90c',
      'User-Agent': 'Awesome-Octocat-App',
    },
  }
)
  .then(() => console.log('ok'))
  .catch(() => console.log('error'));
