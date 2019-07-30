const express = require('express')
const axios = require('axios')
const app = express()
const nodes = [
  'http://localhost:3001',
  'http://localhost:3002',
  'http://localhost:3003',
  'http://localhost:3004',
  'http://localhost:3005',
]
const nodesProxy = [
  3001,
  3002,
  3003,
  3004,
  3005
]

const nodesComputation = [
  'http://localhost:5001',
  'http://localhost:5002',
  'http://localhost:5003',
  'http://localhost:5004',
  'http://localhost:5005',
]

const thisNode = 0
const port = nodesProxy[thisNode]
var leaderNode = -1

var randomIntervalElection = Math.floor(Math.random() * 10000) + 4000;
var randomIntervalSendBeat = Math.floor(Math.random() * 1000) + 2000;

var hashValue = 'AAAA'
var isThisNodeOk = true


function requestElection() {
  console.log('Request Election')
  var requestPoll = []

  for(var i=0; i< 5; i++){
    if(thisNode != i){
      requestPoll.push(
        axios.get(nodes[i]+'/election?node='+thisNode+'&hash='+hashValue)
      )
    }
  }

  Promise.all(requestPoll.map(p => p.catch(() => undefined)))
    .then((responses) => {
      var counter = 1
      responses.forEach(response => {
        if(response != undefined && response.data == '1'){
          counter = counter + 1
        }
      })

      if(counter >= 3){
        console.log('This node is a leader')
        leaderNode = thisNode
        functionInterval()

      }
    })
}

function requestBeat(){
  console.log('Give beat to node')

  var requestPoll = []

  for(var i=0; i< 5; i++){
    if(thisNode != i){
      requestPoll.push(
        axios.get(nodes[i]+'/leader?node='+thisNode+'&hash='+hashValue)
      )
    }
  }

  Promise.all(requestPoll.map(p => p.catch(() => undefined)))
    .then((responses) => {
      console.log('Send beat finish')
    })
}

function functionInterval(){
  console.log('Call Interval Function')
  if(isThisNodeOk){
    if(leaderNode == thisNode){
      requestBeat() 
    } else {
      requestElection()
    }
  }
}



var timerForRequestElection = setInterval(functionInterval, randomIntervalElection)

app.get('/leader', (req, res) => {
  clearInterval(timerForRequestElection)
  timerForRequestElection = setInterval(functionInterval, randomIntervalElection)
  leaderNode = req.query.node
  console.log('Get Leader Beat')

  if(req.query.hash == hashValue){
    isThisNodeOk = true
    res.send('1')
  }else{
    isThisNodeOk = false
    res.send('0')
  }

})

app.get('/election', (req, res) => {
  let node = req.query.node
  let hashValueElection = req.query.hash

  console.log('Node '+ node + ' is request for election')

  if(hashValueElection == hashValue) {
    console.log('Election Approve')
    res.send('1')
  }else{
    console.log('Election Approve')
    res.send('0')
  }

})

app.get('/get_leader', (req, res) => {
  if(leaderNode == -1){
    res.send(nodes[thisNode])
  } else {
    res.send(nodes[leaderNode])
  }
})


app.listen(port, () => console.log(`Example app listening on port ${port}!`))
