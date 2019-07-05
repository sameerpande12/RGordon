var express = require('express');
var app = express();
var logger = require('morgan');
var fs = require('fs');
// app.use(logger('dev'));
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

var sigma_cwnd=[0,0,0,0,0]
var cwnd = [0,0,0,0,0]
var emuDrop=[100000,100000,100000,100000,100000]
var rtt = [1,1,1,1,1]
var numRTTs=[5,50,5,50,5]
var assigned = [false,false,false,false,false]
var trials = [10,10,10,10,10,10]
var chancesLeft=[5,5,5,5,5]
var mtu = [100,100,100,100,100]
var url = [
"http://microsoftonline.com",
"http://yts.am",
//"https://download1892.mediafire.com/p99uu2k135hg/trfwrzkc3211b71/Hrvrd+-+French+Girls.mp3",
//"https://cz.pornhub.com/view_video.php?viewkey=ph5c5227d1350e6",
//"https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/%3Fgws_rd%3Dssl",
"https://www.reddit.com/r/AskReddit/comments/brlti4/reddit_what_are_some_underrated_apps/",
"https://www.youtube.com/",
"https://ja-jp.facebook.com/",
"https://twitter.com/hashtag/ArtistToFollow?src=hash"
]

var batchSize=1
// var sigma_cwnd1 = 0;
// var cwnd1 = 0;
// var emuDrop1 = 100000;
// var rtt1 = 1;
// var assigned1 = false;
// var trials1 = 10;
// var chancesLeft1 = 5;
// // var url1 = "https://www.reddit.com/r/AskReddit/comments/brlti4/reddit_what_are_some_underrated_apps/";
// // var url1="http://caprica.d2.comp.nus.edu.sg/test.txt";
// // var url1 = 'https://dll.z1.fm/music/9/b9/chotkij_paca_-_taksist_(zf.fm).mp3?download=force';
// var url1 = 'https://nl.xhamster.com/users/oceanbreeze833';
//
//
// var sigma_cwnd2 = 0;
// var cwnd2 = 0;
// var emuDrop2 = 100000;
// var rtt2 = 0;
// var assigned2 = false;
// var trials2 = 10;
// var chancesLeft2 = 5;
// var url2 ="https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/%3Fgws_rd%3Dssl";
//
// var sigma_cwnd3 = 0;
// var cwnd3 = 0;
// var emuDrop3 = 100000;
// var rtt3 = 0;
// var assigned3 = false;
// var trials3 = 10;
// var chancesLeft3 = 5;
// // var url3 = "https://www.reddit.com/r/AskReddit/comments/brlti4/reddit_what_are_some_underrated_apps/";
// var url3="https://hao.360.cn/";
//
//
// var sigma_cwnd4 = 0;
// var cwnd4 = 0;
// var emuDrop4 = 100000;
// var rtt4 = 0;
// var assigned4 = false;
// var trials4 = 10;
// var chancesLeft4 = 5;
// // var url3 = "https://www.reddit.com/r/AskReddit/comments/brlti4/reddit_what_are_some_underrated_apps/";
// var url4="http://iptorrents.com";
//
//
// var sigma_cwnd5 = 0;
// var cwnd5 = 0;
// var emuDrop5 = 100000;
// var rtt5 = 0;
// var assigned5 = false;
// var trials5 = 10;
// var chancesLeft5 = 5;
// var url5="https://hao.360.cn/";



app.post('/api/worker/job',function(req,res){
  // console.log("Sending job-----------------------------------------------------------------------");
  res.json({
    message:'JOB',
    //url:"www.google.co.in/search?q=Valdemar+Poulsen&sa=X&hl=en&tbm=isch&source=iu&ictx=1&fir=AkQRON4e7zgjWM%253A%252Ch3kyesQBUnEicM%252C_&usg=AI4_-kSPFA-FLXL_4qaZP2B7aL3UDKH2Ew&ved=2ahUKEwjRgfT4tereAhXCb30KHQL9DEgQ_h0wEnoECAYQCA#imgrc=_",
    data:[{
    url:url[0],
    viewpoint:req.body.viewpoint,
    sigma_cwnd:sigma_cwnd[0].toString(),
    cwnd:cwnd[0].toString(),
    startRTT:rtt[0].toString(),
    endRTT:(rtt[0]+numRTTs[0]-1).toString(),
    trials:trials[0].toString(),
    start_emudrop:emuDrop[0].toString(),
    chances_left:chancesLeft[0].toString(),
    mtu:mtu[0].toString()
    }
  /*  ,
        {
       url:url[1],
       viewpoint:req.body.viewpoint,
       sigma_cwnd:sigma_cwnd[1].toString(),
       cwnd:cwnd[1].toString(),
       startRTT:rtt[1].toString(),
       endRTT:(rtt[1]+numRTTs[1]-1).toString(),
       trials:trials[1].toString(),
       start_emudrop:emuDrop[1].toString(),
       chances_left:chancesLeft[1].toString(),
	mtu:mtu[1].toString()
        }
      ,
      {
      url:url[2],
      viewpoint:req.body.viewpoint,
      sigma_cwnd:sigma_cwnd[2].toString(),
      cwnd:cwnd[2].toString(),
      startRTT:rtt[2].toString(),
      endRTT:(rtt[2]+numRTTs[2]-1).toString(),
      trials:trials[2].toString(),
      start_emudrop:emuDrop[2].toString(),
      chances_left:chancesLeft[2].toString(),
      mtu:mtu[2].toString()
      },
      {
      url:url[3],
      viewpoint:req.body.viewpoint,
      sigma_cwnd:sigma_cwnd[3].toString(),
      cwnd:cwnd[3].toString(),
      startRTT:rtt[3].toString(),
      endRTT:(rtt[3]+numRTTs[3]-1).toString(),
      trials:trials[3].toString(),
      start_emudrop:emuDrop[3].toString(),
      chances_left:chancesLeft[3].toString(),
      mtu:mtu[3].toString()
      },
      {
      url:url[4],
      viewpoint:req.body.viewpoint,
      sigma_cwnd:sigma_cwnd[4].toString(),
      cwnd:cwnd[4].toString(),
      startRTT:rtt[4].toString(),
      endRTT:(rtt[4]+numRTTs[4]-1).toString(),
      trials:trials[4].toString(),
      start_emudrop:emuDrop[4].toString(),
      chances_left:chancesLeft[4].toString(),
      mtu:mtu[4].toString()
    }*/
   ]
  });


  res.end();

   // console.log("Sending: "+ sigma_cwnd1+" "+cwnd1+" "+"emu "+emuDrop1+" chances: "+chancesLeft1);
})


app.post('/api/worker/update',function(req,res){
  console.log("received update");
  // console.log(req.body);
  index=0
  for ( index = 0;index< batchSize;index++){
    if(req.body.url == url[index]){
      break;
    }
  }
  console.log(index)
  // console.log(req.body.url)


    if(req.body.cwnd > 80 && !assigned[index]){
        emuDrop[index] = sigma_cwnd[index];
        assigned[index] = true;
    }
      sigma_cwnd[index] = req.body.sigma_cwnd;
      cwnd[index] = req.body.cwnd;
      trials[index]=req.body.max_trials;
      console.log(req.body.sigma_cwnd+" "+req.body.cwnd+" "+rtt[index]);
      rtt[index] = rtt[index]+1;
      //chancesLeft1 = 5;


    res.status(200);
    res.json({fname:"Data updated successfully"});
    res.end();
})

app.post('/api/worker/updateError',function(req,res){
  console.log("received error");
  // console.log(req.body);
  index=0
  for ( index = 0;index< batchSize;index++){
    if(req.body.url == url[index]){
      break;
    }
  }
  console.log(index)
     chancesLeft[index] = parseInt(req.body.chances_left);

     if(chancesLeft[index] < 1){
       sigma_cwnd[index] = 0;
       cwnd[index] = 0;
       rtt[index]= 1;
       chancesLeft[index] = 5;
       emuDrop[index] = 100000;
       assigned[index] = false;

     }


      res.status(200);
      res.json({fname:"updated error"});
      res.end();
})


app.post('/api/worker/complete',function(req,res){
  console.log("received-> COMPLETE");
  // console.log(req.body);
  index=0
  for ( index = 0;index< batchSize;index++){
    if(req.body.url == url[index]){
      break;
    }
  }
  console.log(index)


   sigma_cwnd[index] = 0;
   cwnd[index] = 0;
   rtt[index]= 1;
   chancesLeft[index] = 5;
   emuDrop[index] = 100000;
   assigned[index] = false;
    res.status(200);
    res.json({fname:"One communitcation done"});
    res.end();


})


module.exports = app;
