import fs from "fs";
import http from "http";

const requestHandler = (req, res) => {
	if (req.method === "GET") {
		console.log("GET-request")
	  if (req.url === "/chomp.css") {
	    fs.readFile("./chomp.css", (err, data) => {
	      res.writeHead(200, { "Content-Type": "text/css" });
	      res.end(data);
	      console.log("Ny request: /chomp.css");
	    });
	  } else if (req.url === "/chomp.js") {
	    fs.readFile("./chomp.js", (err, data) => {
	      res.writeHead(200, { "Content-Type": "text/javascript" });
	      res.end(data);
	      console.log("Ny request: /chomp.js");
	    });
	  } else if (req.url === "/") {
	    fs.readFile("./chomp.html", (err, data) => {
	      res.writeHead(200, { "Content-Type": "text/html" });
	      res.end(data);
	      console.log("Ny request: /chomp.html");
	    });
	  }
	}
};

const server = http.createServer(requestHandler);
const port = 1234;

server.listen(port, (err) => {
  if (err) {
    console.log("Error starting server", err);
  } else {
    console.log(`Server is listening on port ${port}`);
  }
});
