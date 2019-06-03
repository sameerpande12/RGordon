const https = require('http');
const request = require('request');
const fs = require("fs");
const spawn = require("child_process").spawn;
var isFree = true;
var defaultEmu = 100000;
var threshold = 80;
const viewPoint = "Singapore";

var pingServer = function(){
   if(isFree){
     isFree = false;
     var path = '';
     request.post('http://localhost:3000/api/worker/job',{json:{viewpoint:viewPoint}} ,function(error,resp,body) => {

        let data = '';
         resp.on('data', (chunk) => {
           data += chunk;
         });
         resp.on('end', (req,res) => {

           data=JSON.parse(data);
           if(data.message == "JOB"){
             var startRTT = int(data.startRTT);
             var endRTT = int(data.endRTT);
             var url = data.url;
             var emuDrop = data.start_emudrop;
             var chances_left = data.chances_left;
             var trials = data.trials;
             var cwnd = data.cwnd;
             var sigma_cwnd = data.sigma_cwnd;
             for(rnum=startRTT;rnum<=endRTT;rnum++){
                 const pyProg= spawn('python3',["calculate.py",url,trials,sigma_cwnd,cwnd,rnum,emuDrop]);

                 pyProg.stdout.on('data', function(data) {

                   console.log(data.toString());

                  });

                 pyProg.stderr.on('data', (data) => {
                   console.log(`stderr: ${data}`);
                 });

                 pyProg.on('close', (code) => {
                   console.log(`child process exited with code ${code}`);
                   var text = fs.readFileSync("./RData/windows.csv","utf-8");

                   var tmp = ((text.split("\n"))[0]).split(' ');
                   var values = [];
                   tmp.forEach( function(str){values.push(parseInt(str));});
                   var postData ='';
                   if(values[0]==0 && values[1]==0){
                     postData = { json: {message_type:"Error",rtt:rnum,url:url,chancesLeft:chancesLeft-1,viewpoint:viewPoint } };
                     path = '/api/worker/updateError';
                     
                   }
                   else if(values[1]==0){

                     postData = { json: {message_type:"Complete",rtt:rnum,url:url,viewpoint:viewPoint} };
                     path = '/api/worker/complete';
                   }
                   else{
                     path = '/api/worker/update';
                     var emuDrop = data.emuDrop;
                     if(emuDrop==defaultEmu){
                       if(values[1]>threshold){
                         emuDrop = sigma_cwnd;
                       }
                     }
                     cwnd = values[1];
                     sigma_cwnd = values[0];

                    postData = { json: { message_type:"Done" ,cwnd: values[1], sigma_cwnd: values[0],rtt:values[2],url:data.url,emuDrop:emuDrop,viewpoint:viewPoint } };
                   }
                   console.log(postData);
                   request.post(
                     'http://localhost:3000'+path,
                     postData,
                     function (err, response, ack_body) {
                       if (!err && response.statusCode == 200) {
                           console.log(ack_body);
                           isFree= true;
                       }
                     }
                    );

                 });
              }
            }
           });

     }).on("error", (err) => {
       console.log("Error: " + err.message);
        isFree=true;
     });


   }

}
setInterval(pingServer,2000);
