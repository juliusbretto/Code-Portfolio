import { Router } from "express";
import db from "../db.js";
import sessionManager from "../sessionManager.js";
import { readFile, resolvePath } from "../util.js";
import bcrypt from "bcrypt";

const publicRouter = Router();
const privateRouter = Router();

///GET REQUESTS /LOGIN
publicRouter.get("/login", async (req, res) => {
  console.log("/LOGIN GET REQUEST");
  console.log(req.body);
  if (req.headers.cookie && sessionManager.findSessionById(req.headers.cookie.split("=")[1])) {
	  console.log("Account already logged in, switching to profile..");
	  res.redirect("/");
	  
  } else {
	  const htmlDoc = await readFile(resolvePath("public", "login.html"));
	  res.status(200).send(htmlDoc);
	}
});


///POST REQUESTS /LOGIN
publicRouter.post("/login", async (req, res) => {
	console.log("/LOGIN POST REQUEST");
	console.log(req.body);
	const {username, password} = req.body;
	
	const user = await db.get("SELECT password FROM userinfo WHERE username = (?)", username);
	if (user && bcrypt.compareSync(password, user.password)) { //om användaren existerar i db
		console.log(`Login successful! Welcome ${user.username}`);
		const session = sessionManager.createNewSession(username);
		res.cookie("session-id", session.id).redirect("/");
	} else {
		console.log(`Login error! The username ${username} does not exist or the password is incorrect.`);
		res.redirect(`/login?error=The username ${username} does not exist or the password is incorrect.`);
	}
});


privateRouter.post("/logout", (req, res) => {
  console.log("/LOGOUT POST REQUEST");
  const id = req.headers.cookie.split("=")[1];
  const username = sessionManager.findUsername(id);
  sessionManager.deleteSession(id);
  res.clearCookie("session-id");
  res.redirect(`/login?success=${username} successfully logged out.`);
  console.log("Logged out.");
});

export default {
  publicRouter,
  privateRouter,
};
