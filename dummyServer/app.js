var express = require('express');
var app = express();
//var logger = require('morgan');
//app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

var sigma_cwnd = 1437;
var cwnd = 103;
var emuDrop = 96;
var rtt = 27;
var assigned = true;

/*
var sigma_cwnd = 0;
var cwnd = 0;
var emuDrop = 100000;
var rtt = 1;
var assigned = false;
*/
var trials = 10;
var chancesLeft = 5;

app.get('/',function(req,res){
  res.json({
    fname:'Calculate',
    url:'www.youtube.com',
    sigma_cwnd:sigma_cwnd,
    cwnd:cwnd,
    rtt:rtt,
    trials:trials,
    emuDrop:emuDrop,
    chancesLeft:chancesLeft
  });
   console.log("Sending: "+ sigma_cwnd+" "+cwnd+" "+"emu "+emuDrop+" chances: "+chancesLeft);
})


app.post('/',function(req,res){
  console.log("received");
  console.log(req.body);

  var mtype = req.body.message_type;
  if(mtype == "Done"){

        if(req.body.cwnd > 80 && !assigned){
          emuDrop = sigma_cwnd;
          assigned = true;
        }
        sigma_cwnd = req.body.sigma_cwnd;
        cwnd = req.body.cwnd;
        rtt = rtt+1;
        chancesLeft = 5;
   }
   else if(mtype == "Error"){

     chancesLeft = req.body.chancesLeft;
     if(chancesLeft < 1){
       sigma_cwnd = 0;
       cwnd = 0;
       rtt= 1;
       chancesLeft = 5;
       emu = 100000;
       assigned = false;

     }

   }
   else if(mtype == "Complete"){
     sigma_cwnd = 0;
     cwnd = 0;
     rtt= 1;
     chancesLeft = 5;
     emu = 100000;
     assigned = false;


   }


      res.status(200);
      res.json({fname:"One communitcation done"});
      res.end();
})


module.exports = app;
