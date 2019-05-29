const https = require('http');
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
      const pyProg= spawn('python3',["calculate.py","www.youtube.com","10"]);
      
      pyProg.stdout.on('data', function(data) {

        console.log(data.toString());
        
       });

      pyProg.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
      });
      
      pyProg.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
      });
    });

}).on("error", (err) => {
  console.log("Error: " + err.message);
 
});