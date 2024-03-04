import { Router } from "express";
import { readFile, resolvePath } from "../util.js";
import sessionManager from "../sessionManager.js";

const privateRouter = Router();

privateRouter.get("/", async (req, res) => {
  console.log("/PROFILE GET REQUEST");
  const id = req.headers.cookie.split("=")[1];
  const username = sessionManager.findUsername(id);
  console.log("Number of sessions associated with this username: " + sessionManager.getNbrOfSessions(username));
  

  let htmlDoc = (
    await readFile(resolvePath("templates", "profile.html"))
  ).replace("$username$", username);

  //if there is one or less current sessions, the logout link is hidden
  if (sessionManager.getNbrOfSessions(username) > 1) {
	    htmlDoc = htmlDoc.replace("d-none", "");
	  }
  
  res.status(200).send(htmlDoc);
});

//sets up a route handler for HTTP GET requests targeting /endOtherSessions endpoint
//it ends all of the sessions for the session associated with the "id", and sends an 
//empty response back to the client to acknowledge that the request has been handled successfully
privateRouter.get("/endOtherSessions", (req, res) => {
	const id = req.headers.cookie.split("=")[1];
	sessionManager.deleteOtherSessions(id); 
	res.send();
});

export default {
  privateRouter,
};
