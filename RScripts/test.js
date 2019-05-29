const https = require('http');
const request = require('request');

const spawn = require("child_process").spawn;
https.get('http://localhost:3000', (resp) => {

   let data = '';

    // A chunk of data has been recieved.
    resp.on('data', (chunk) => {
      data += chunk;
    });

  // The whole response has been received. Print out the result.
    resp.on('end', (req,res) => {
      data=JSON.parse(data);
      const pyProg= spawn('python3',["calculate.py",data.url,data.trials,data.sigma_cwnd,data.cwnd,data.rtt]);

      pyProg.stdout.on('data', function(data) {

        console.log(data.toString());

       });

      pyProg.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
      });

      pyProg.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        request.post(
          'http://localhost:3000',
          { json: { name: 'ironman' } },
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
