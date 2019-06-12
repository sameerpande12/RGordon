var express = require('express');
var app = express();
var logger = require('morgan');
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));


/*
var sigma_cwnd = 3040;
var cwnd = 71;
var emuDrop = 167;
var rtt = 1;
var assigned = true;
*/

/*
var sigma_cwnd1 = 5551;
var cwnd1 = 15;
var emuDrop1 = 99;
var rtt1 = 73;
var assigned1 = true;
var trials1 = 10;
var chancesLeft1 = 5;
var url1 = "https://www.youtube.com";
*/

var sigma_cwnd1 = 0;
var cwnd1 = 0;
var emuDrop1 = 100000;
var rtt1 = 0;
var assigned1 = false;
var trials1 = 1;
var chancesLeft1 = 5;
var url1 ="https://www.google.com";

var sigma_cwnd2 = 0;
var cwnd2 = 0;
var emuDrop2 = 100000;
var rtt2 = 0;
var assigned2 = false;
var trials2 = 1;
var chancesLeft2 = 5;
var url2 = "https://www.reddit.com/r/AskReddit/comments/brlti4/reddit_what_are_some_underrated_apps/";

app.post('/api/worker/job',function(req,res){
  console.log("Sending job-----------------------------------------------------------------------");
  res.json({
    message:'JOB',
    //url:"www.google.co.in/search?q=Valdemar+Poulsen&sa=X&hl=en&tbm=isch&source=iu&ictx=1&fir=AkQRON4e7zgjWM%253A%252Ch3kyesQBUnEicM%252C_&usg=AI4_-kSPFA-FLXL_4qaZP2B7aL3UDKH2Ew&ved=2ahUKEwjRgfT4tereAhXCb30KHQL9DEgQ_h0wEnoECAYQCA#imgrc=_",
    data:[{
      //url:" https://www.google.com.ph/search?q=Valdemar+Poulsen&sa=X&hl=en&tbm=isch&source=iu&ictx=1&fir=AkQRON4e7zgjWM%253A%252Ch3kyesQBUnEicM%252C_&usg=AI4_-kSPFA-FLXL_4qaZP2B7aL3UDKH2Ew&ved=2ahUKEwjRgfT4tereAhXCb30KHQL9DEgQ_h0wEnoECAYQCA&gws_rd=ssl",
      //url:"https://sg.yahoo.com/?p=us",
    url:url1,
    viewpoint:req.body.viewpoint,
    sigma_cwnd:sigma_cwnd1.toString(),
    cwnd:cwnd1.toString(),
    startRTT:rtt1.toString(),
    endRTT:(rtt1+1).toString(),
    trials:trials1.toString(),
    start_emudrop:emuDrop1.toString(),
    chances_left:chancesLeft1.toString()
   },{
    //url:" https://www.google.com.ph/search?q=Valdemar+Poulsen&sa=X&hl=en&tbm=isch&source=iu&ictx=1&fir=AkQRON4e7zgjWM%253A%252Ch3kyesQBUnEicM%252C_&usg=AI4_-kSPFA-FLXL_4qaZP2B7aL3UDKH2Ew&ved=2ahUKEwjRgfT4tereAhXCb30KHQL9DEgQ_h0wEnoECAYQCA&gws_rd=ssl",
    //url:"https://sg.yahoo.com/?p=us",
  url:url2,
  viewpoint:req.body.viewpoint,
  sigma_cwnd:sigma_cwnd2.toString(),
  cwnd:cwnd2.toString(),
  startRTT:rtt2.toString(),
  endRTT:(rtt2+1).toString(),
  trials:trials2.toString(),
  start_emudrop:emuDrop2.toString(),
  chances_left:chancesLeft2.toString()
  }
   ]
  });


  res.end();

   console.log("Sending: "+ sigma_cwnd1+" "+cwnd1+" "+"emu "+emuDrop1+" chances: "+chancesLeft1);
})


app.post('/api/worker/update',function(req,res){
  console.log("received");
  console.log(req.body);
  if(req.body.url==url1){
        if(req.body.cwnd > 80 && !assigned1){
            emuDrop1 = sigma_cwnd1;
            assigned1 = true;
        }
          sigma_cwnd1 = req.body.sigma_cwnd;
          cwnd1 = req.body.cwnd;
          rtt1 = rtt1+1;
          //chancesLeft1 = 5;
    }
    else {
      if(req.body.cwnd > 80 && !assigned1){
          emuDrop2 = sigma_cwnd2;
          assigned2 = true;
      }
        sigma_cwnd2 = req.body.sigma_cwnd;
        cwnd2 = req.body.cwnd;
        rtt2 = rtt2+1;
        //chancesLeft2 = 5;

    }
    res.status(200);
    res.json({fname:"Data updated successfully"});
    res.end();
})

app.post('/api/worker/updateError',function(req,res){
  console.log("received");
  console.log(req.body);
     chancesLeft1 = parseInt(req.body.chances_left);
     if(req.body.url == url1){
         if(chancesLeft1 < 1){
           sigma_cwnd1 = 0;
           cwnd1 = 0;
           rtt1= 1;
           chancesLeft1 = 5;
           emu1 = 100000;
           assigned1 = false;

         }
       }
       else{
         if(chancesLeft2 < 1){
           sigma_cwnd2 = 0;
           cwnd2 = 0;
           rtt2= 1;  if(req.body.cwnd > 80 && !assigned1){
            emuDrop1 = sigma_cwnd1;
            assigned1 = true;
        }
          sigma_cwnd1 = req.body.sigma_cwnd;
          cwnd1 = req.body.cwnd;
          rtt1 = rtt1+1;
          chancesLeft1 = 5;
           chancesLeft2 = 5;
           emuDrop2 = 100000;
           assigned2 = false;

         }

       }

      res.status(200);
      res.json({fname:"updated error"});
      res.end();
})


app.post('/api/worker/complete',function(req,res){
  console.log("received-> COMPLETE");
  console.log(req.body);
   if(req.body.url == url1){
       sigma_cwnd1 = 0;
       cwnd1 = 0;
       rtt1= 1;
       chancesLeft1 = 5;
       emuDrop1 = 100000;
       assigned1 = false;
        res.status(200);
        res.json({fname:"One communitcation done"});
        res.end();
    }
    else{
      sigma_cwnd2 = 0;
      cwnd2 = 0;
      rtt2= 1;
      chancesLeft2 = 5;
      emuDrop2 = 100000;
      assigned2 = false;
       res.status(200);
       res.json({fname:"One communitcation done"});
       res.end();
    }
})


module.exports = app;
