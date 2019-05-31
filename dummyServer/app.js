var express = require('express');
var app = express();
//var logger = require('morgan');
//app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

var sigma_cwnd = 1011;
var cwnd = 3;
var rtt = 18;
var trials = 15;
var chancesLeft = 5;
var emuDrop = 109;
var assigned = true;

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
  /*if(req.message_type == "Done"){
      if(req.body.cwnd > 80 && !assigned){
        emuDrop = sigma_cwnd;
        assigned = true;
      }
      sigma_cwnd = req.body.sigma_cwnd;
      cwnd = req.body.cwnd;
      rtt = rtt+1;
  }
  else if(req.message_type == "Complete"){
      sigma_cwnd = 0;
      cwnd = 0;
      rtt = 1;
      chancesLeft = 5;
      emuDrop = 10000;

  }
  else if(req.message_type == "Error"){
    if(req.chancesLeft <=0){
      sigma_cwnd = 0;
      cwnd = 0;
      rtt = 1;
      chancesLeft = 5;
      emuDrop = 10000;
    }
    else{
       chancesLeft = req.chancesLeft;
    }
  }*/
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
