var express = require('express');
var app = express();
//var logger = require('morgan');
//app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

var sigma_cwnd = 0;
var cwnd = 0;
var rtt = 1;
var trials = 15;
var chancesLeft = 5;
var emuDrop = -1;

app.get('/',function(req,res){
  res.json({
    fname:'Calculate',
    url:'www.twitter.com',
    sigma_cwnd:sigma_cwnd,
    cwnd:cwnd,
    rtt:rtt,
    trials:trials,
    emuDrop:emuDrop,
    chancesLeft:chancesLeft
  });

})


app.post('/',function(req,res){
  console.log(req.body);

  if(req.body.cwnd > 80){
    emuDrop = sigma_cwnd;
  }
  sigma_cwnd = req.body.sigma_cwnd;
  cwnd = req.body.cwnd;
  rtt = rtt+1;
  res.status(200);
  res.json({fname:"Done"});
  res.end();
})


module.exports = app;
