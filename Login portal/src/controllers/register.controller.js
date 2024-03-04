import { Router } from "express";
import db from "../db.js";
import { readFile, resolvePath } from "../util.js";
import sessionManager from "../sessionManager.js";
import bcrypt from "bcrypt";

const publicRouter = Router();

//The router handles GET requests
publicRouter.get("/register", async (req, res) => {
  console.log("/REGISTER GET REQUEST");
  //Om redan inloggad, profile sidan
  if (req.headers.cookie && sessionManager.findSessionById(req.headers.cookie.split("=")[1])) {
	 res.redirect("/");
} else {
    console.log(req.body);
    const htmlDoc = await readFile(resolvePath("public", "register.html"));
    res.status(200).send(htmlDoc);
  }
});

//Handles the POST request, when we register a new user
publicRouter.post("/register", async (req, res) => {
  const {username, password, confirm} = req.body;
  console.log(req.body);
  
  const userRow = await db.get("SELECT * FROM userinfo WHERE username = (?)", username); //plockar fram raden för "username"
  if (!userRow) { //om den är undefined, dvs tom dvs användarnamnet ej finns, ska man kunna registrera ny användare
	  if (username.length >= 3 && password.length >= 3 && /\d/.test(username) && /\d/.test(password) && /[a-zA-Z]/.test(username) && /[a-zA-Z]/.test(password)) { //om användarnamn/lösenord uppfyller kraven
		  if (password === confirm) { //om lösenorden stämmer överens
			  const hashSaltPassword = bcrypt.hashSync(password, 10);
			  await db.run("INSERT INTO userinfo VALUES (?,?)", [username, hashSaltPassword]);
			  console.log(`Successfully added user: ${username}`);
			  const session = sessionManager.createNewSession(username);
			  res.cookie("session-id", session.id).redirect("/"); //redirect to profile
		  } else { //om lösenorden ej stämmer överens
			  console.log("The passwords do not match.");
		      res.redirect("/register?error=Confirm password must be the same as the password!");
		    }
	  } else { //om lösenord/användarnamn är <3 eller ej innehåller siffror/bokstäver
		  console.log(`That password or username does not meet the requirements. Both the username and password need to be at least three characters long and include at least one number and one character.`);
		  res.redirect(`/register?error=That password or username does not meet the requirements. Both the username and password need to be at least three characters long and include at least one number and one character.`);  
	  }
  } else { //om användaren finns
	  console.log(`The username ${username} is already in use. Please select a different username.`);
	  res.redirect(`/register?error=The username ${username} is already in use. Please select a different username.`);
  }
});

export default {
  publicRouter,
};
