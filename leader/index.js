const express = require('express')
const axios = require('axios')
const app = express()
const port = 3000

const node = [
  'http://localhost:5001',
  'http://localhost:5002',
  'http://localhost:5003',
  'http://localhost:5004',
  'http://localhost:5005'
]

app.get('/', (req, res) => res.send('Hello World!'))

app.get('/trx', (req, res) => {
  console.log(req.query.sender_n)
  var counter = 0

  Promise.all([
    axios.post(node[0] + '/trx', {
      sender_n: req.query.sender_n,
      sender_e: req.query.sender_e,
      sender_d: req.query.sender_d,
      receiver_n: req.query.receiver_n,
      receiver_e: req.query.receiver_e,
    }),
    axios.post(node[1] + '/trx', {
      sender_n: req.query.sender_n,
      sender_e: req.query.sender_e,
      sender_d: req.query.sender_d,
      receiver_n: req.query.receiver_n,
      receiver_e: req.query.receiver_e,
    }),
    axios.post(node[2] + '/trx', {
      sender_n: req.query.sender_n,
      sender_e: req.query.sender_e,
      sender_d: req.query.sender_d,
      receiver_n: req.query.receiver_n,
      receiver_e: req.query.receiver_e,
    }),
    axios.post(node[3] + '/trx', {
      sender_n: req.query.sender_n,
      sender_e: req.query.sender_e,
      sender_d: req.query.sender_d,
      receiver_n: req.query.receiver_n,
      receiver_e: req.query.receiver_e,
    }),
    axios.post(node[4] + '/trx', {
      sender_n: req.query.sender_n,
      sender_e: req.query.sender_e,
      sender_d: req.query.sender_d,
      receiver_n: req.query.receiver_n,
      receiver_e: req.query.receiver_e,
    }),
  ])
    .then(function (responses) {
      var i = 1;
      responses.forEach(response => {
        if(response.data == "0") {
          console.log("Node "+ i + "menyatakan vote tidak valid.")
        } else {
          console.log("Node "+ i + "menyatakan vote valid.")
          counter = counter + 1
        }
        i = i + 1
      });
      if(counter >= 3) {
        res.send('Vote Valid')
      } else {
        res.send('Vote Tidak Valid')
      }
    })
    .catch(function (error) {
      console.log(error);
      res.send('Vote Tidak Valid')
    });

})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))
