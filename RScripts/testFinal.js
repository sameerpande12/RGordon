const https = require('https');
const request = require('request');
const request_pn = require('request-promise-native');
const fs = require("fs");
const spawn = require("child_process").spawn;
var isFree = true;
var defaultEmu = 100000;
var threshold = 80;
const viewPoint = "Singapore";
var domain = 'http://172.26.191.175:4000';
var start = Date.now();
//fs.writeFile("time.txt","Starting at "+start,(err)=>{});

const evaluate = function(startRTT, endRTT, emuDrop, chances_left, trials, cwnd, sigma_cwnd, url, rnum, path, evaluate){
   //console.log("entering evaluate "+(rnum).toString+ " "+str(endRTT)+ " "(rnum<=endRTT));
  if(rnum<=endRTT) {
    console.log("Entering "+rnum);
    const pyProg= spawn('python3',["calculate.py",url,trials,sigma_cwnd,cwnd,rnum,emuDrop]);
    pyProg.stderr.on('data', (data) => {
      //console.log(`stderr: ${data}`);
    });
    pyProg.on('close', (code) => {
      console.log("calculate.py done for "+rnum);
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

        postData = { json: { cwnd: values[1].toString(), sigma_cwnd: values[0].toString(),last_rtt_done:values[2].toString(),url:url,emudrop:emuDrop.toString(),viewpoint:viewPoint } };
      }
      //fs.appendFile("time.txt","\n",(err)=>{});
      //fs.appendFile("time.txt",Date.now() - start,(err)=>{});

      console.log(postData.json);
      request.post(
        domain+path,
        postData,
        function (err, response, ack_body) {
          if(values[1]==0 || rnum==endRTT){
            isFree= true;
          }

          if (!err && response.statusCode == 200){
            console.log(ack_body);
          }else{
            console.log("some error");
          }
          //useloop = true;
          rnum++;
          if(rnum<=endRTT){
            evaluate();
          }
        }
      );
    }).on("error", (err) => {
      console.log("Error: " + err.message);
    });
  }
  else{
    console.log("One task done");
  }
};

var pingServer = function(){
  console.log("Every 2 seconds");
  if(isFree){
    isFree = false;
    var path = '';
    console.log("Asking for a job");
    request.post(domain+'/api/worker/job',{json:{viewpoint:viewPoint}} ,function(error,resp,body)  {
         if(typeof resp != 'undefined'){
                var body=resp.body;
                console.log(body);
                if(body.message == "JOB"){
                  var startRTT = parseInt(body.data[0].startRTT);
                  var endRTT = parseInt(body.data[0].endRTT);
                  var emuDrop = parseInt( body.data[0].start_emudrop);
                  var chances_left = parseInt(body.data[0].chances_left);
                  var trials = parseInt(body.data[0].trials);
                  var cwnd = parseInt(body.data[0].cwnd);
                  var sigma_cwnd = parseInt(body.data[0].sigma_cwnd);
                  var url = body.data[0].url;
                  var rnum = startRTT;
                  //var useloop = true;
                  console.log("python3 calculate.py"+url + " "+ trials+ " "+sigma_cwnd + " "+cwnd + " "+rnum +" "+ emuDrop);
                  evaluate(startRTT, endRTT, emuDrop, chances_left, trials, cwnd, sigma_cwnd, url, rnum, path, evaluate);
                }else{
                  console.log("no Job---no Job");
                  isFree = true;
                }
        }
        else{
          isFree = true;
        //  console.log("No repsonse");
        }
    }).on("error", (err) => {
     console.log("Error: " + err.message);

   });
  }
}
setInterval(pingServer,2000);
