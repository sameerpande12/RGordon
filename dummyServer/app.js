var express = require('express');
var app = express();
var logger = require('morgan');
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
/*
var sigma_cwnd = 1437;
var cwnd = 103;
var emuDrop = 96;
var rtt = 27;
var assigned = true;
*/

var sigma_cwnd = 0;
var cwnd = 0;
var emuDrop = 100000;
var rtt = 1;
var assigned = false;

var trials = 10;
var chancesLeft = 5;

app.post('/api/worker/job',function(req,res){
  res.json({
    message:'JOB',
    //url:"www.google.co.in/search?q=Valdemar+Poulsen&sa=X&hl=en&tbm=isch&source=iu&ictx=1&fir=AkQRON4e7zgjWM%253A%252Ch3kyesQBUnEicM%252C_&usg=AI4_-kSPFA-FLXL_4qaZP2B7aL3UDKH2Ew&ved=2ahUKEwjRgfT4tereAhXCb30KHQL9DEgQ_h0wEnoECAYQCA#imgrc=_",
    url:"www.pandesameer.com",
    viewpoint:req.body.viewpoint,
    sigma_cwnd:sigma_cwnd.toString(),
    cwnd:cwnd.toString(),
    startRTT:rtt.toString(),
    endRTT:(rtt+3).toString(),
    trials:trials.toString(),
    start_emudrop:emuDrop.toString(),
    chances_left:chancesLeft.toString()
  });


  res.end();

   console.log("Sending: "+ sigma_cwnd+" "+cwnd+" "+"emu "+emuDrop+" chances: "+chancesLeft);
})


app.post('/api/worker/update',function(req,res){
  console.log("received");
  console.log(req.body);
  if(req.body.cwnd > 80 && !assigned){
      emuDrop = sigma_cwnd;
      assigned = true;
  }
    sigma_cwnd = req.body.sigma_cwnd;
    cwnd = req.body.cwnd;
    rtt = rtt+1;
    chancesLeft = 5;
    res.status(200);
    res.json({fname:"Data updated successfully"});
    res.end();
})

app.post('/api/worker/updateError',function(req,res){
  console.log("received");
  console.log(req.body);
     chancesLeft = parseInt(req.body.chancesLeft);
     if(chancesLeft < 1){
       sigma_cwnd = 0;
       cwnd = 0;
       rtt= 1;
       chancesLeft = 5;
       emu = 100000;
       assigned = false;

     }

      res.status(200);
      res.json({fname:"updated error"});
      res.end();
})


app.post('/api/worker/complete',function(req,res){
  console.log("received");
  console.log(req.body);
     sigma_cwnd = 0;
     cwnd = 0;
     rtt= 1;
     chancesLeft = 5;
     emu = 100000;
     assigned = false;
      res.status(200);
      res.json({fname:"One communitcation done"});
      res.end();
})


module.exports = app;
