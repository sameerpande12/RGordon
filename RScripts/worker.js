const https = require('https');
const request = require('request');
const request_pn = require('request-promise-native');
const fs = require("fs");
const spawn = require("child_process").spawn;

var isFree = true;
var defaultEmu = 100000;
var threshold = 80;
const viewPoint = "Singapore";
var domain = 'http://137.132.83.199:4000';;//hydra
// var domain = 'http://localhost:3000';
// var domain='http://172.26.191.175:4000';//atishya-pc
var start = Date.now();

var pingServer = function(){
  //console.log("Every 2 seconds");
  try{
          if(isFree){
            isFree = false;
            var path = '';
            console.log("Asking for a job");
            request.post(domain+'/api/worker/job',{json:{viewpoint:viewPoint}} ,function(error,resp,body)  {
                 if(typeof resp != 'undefined'){
                        var body=resp.body;
                        console.log(body);
                        if(body.message == "JOB"){
                          jsonData= JSON.stringify(body);
                          fs.writeFile("jobs.json",jsonData,function(err){
                            if(err){
                              console.log(err);
                            }
                          });
                          const work = spawn('python3',["work.py","jobs.json",domain]);
                          work.stderr.setEncoding('utf8');
                          work.stderr.on("data",recvData=>{
                            console.log("stderr: ", recvData);
                          });
                          work.on("data",recvData=>{
                            console.log(recvData);
                          });
                          work.on('close',(code)=>{
                            isFree=true;
                            console.log("making is free true  123123");
                          });
                        }
                        else{
                          console.log("no Job---no Job");
                          console.log("Making isFree true 2");
                          isFree = true;
                        }
                }
                else{
                  console.log("Making isFree true 3");
                  isFree = true;
                //  console.log("No repsonse");
                }
            }).on("error", (err) => {
              isFree = true;
              console.log("Making isFree true 4");
             console.log("Error: " + err.message);

           });
          }
    }
    catch(err){
      console.log("Making isFree true 5");
      isFree = true;
      console.log(err);
    }
}
setInterval(pingServer,2000);
