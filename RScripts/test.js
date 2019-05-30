const https = require('http');
const request = require('request');
const fs = require("fs");
const spawn = require("child_process").spawn;
var chancesLeft=0;
https.get('http://localhost:3000', (resp) => {

   let data = '';

    // A chunk of data has been recieved.
    resp.on('data', (chunk) => {
      data += chunk;
    });

  // The whole response has been received. Print out the result.
    resp.on('end', (req,res) => {
      data=JSON.parse(data);

      const pyProg= spawn('python3',["calculate.py",data.url,data.trials,data.sigma_cwnd,data.cwnd,data.rtt,data.emuDrop]);

      pyProg.stdout.on('data', function(data) {

        console.log(data.toString());

       });

      pyProg.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
      });

      pyProg.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        var text = fs.readFileSync("./RData/windows.csv","utf-8");
        var url = ((fs.readFileSync("./RData/current_url.txt","utf-8")).split('\n'))[0];
        var tmp = ((text.split("\n"))[0]).split(' ');
        var values = [];
        tmp.forEach( function(str){values.push(parseInt(str));});
        var postData ='';
        if(values[0]==0 && values[1]==0){
          postData = { json: {message_type:"Error",rtt:data.rtt,url:data.url,chancesLeft:data.chancesLeft-1 } };
        }
        else{
         postData = { json: { message_type:"Done" ,cwnd: values[1], sigma_cwnd: values[0],rtt:values[2],url:data.url } };
        }
        request.post(
          'http://localhost:3000',
          postData,
          function (error, response, body) {
            if (!error && response.statusCode == 200) {
                console.log(body);
            }
          }
         );

      });
    });

}).on("error", (err) => {
  console.log("Error: " + err.message);

});
