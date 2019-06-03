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
     request.post('http://localhost:3000/api/worker/job',{json:{viewpoint:viewPoint}} ,function(error,resp,body)  {

        let data = '';
         resp.on('data', (chunk) => {
           data += chunk;
         });
         resp.on('end', (req,res) => {
               data=JSON.parse(data);
               if(data.message == "JOB"){
                 var startRTT = parseInt(data.startRTT);
                 var endRTT = parseInt(data.endRTT);
                 var emuDrop = parseInt( data.start_emudrop);
                 var chances_left = parseInt(data.chances_left);
                 var trials = parseInt(data.trials);
                 var cwnd = parseInt(data.cwnd);
                 var sigma_cwnd = parseInt(data.sigma_cwnd);
                 var url = data.url;
                 for(rnum=startRTT;(rnum<=endRTT)&&(!isFree);rnum++){
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
                            postData = { json: {last_error:"error",last_rtt_done:rnum.toString(),url:url,chances_left:(chances_left-1).toString(),viewpoint:viewPoint } };
                            path = '/api/worker/updateError';

                       }
                       else if(values[1]==0){

                            postData = { json: {last_rtt_done:rnum.toString(),url:url,viewpoint:viewPoint} };
                            path = '/api/worker/complete';
                       }
                       else{
                             path = '/api/worker/update';

                             if(emuDrop==defaultEmu){
                               if(values[1]>threshold){
                                 emuDrop = sigma_cwnd;//last sigma_cwnd before updating
                               }
                             }
                             cwnd = values[1];//update cwnd and sigma_cwnd
                             sigma_cwnd = values[0];

                            postData = { json: { cwnd: values[1].toString(), sigma_cwnd: values[0].toString(),last_rtt_done:values[2].toString(),url:url,emuDrop:emuDrop.toString(),viewpoint:viewPoint } };
                       }
                       console.log(postData);
                       request.post(
                                 'http://localhost:3000'+path,
                                 postData,
                                 function (err, response, ack_body) {
                                   if (!err && response.statusCode == 200) {
                                       console.log(ack_body);

                                   }
                                 }
                        );
                        if(values[1]==0){//i.e either complete or error
                          isFree=true;

                        }

                     });
                }

                 isFree=true;
              }
          });

     }).on("error", (err) => {
       console.log("Error: " + err.message);
        isFree=true;
     });


   }

}
setInterval(pingServer,2000);
