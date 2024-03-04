import sessionManager from "../sessionManager.js";

const requireAuth = (req, res, next) => {
//Om man försöker accessa profilsidan/logout, men antingen ej har en cookie, eller om cookien är "fake"/ej giltig längre
  if (req.path === "/" || req.path === "/logout") {
	  if (!req.headers.cookie) {
		  console.log("Profile error: not currently logged in.")
		  res.redirect(`/login?error=You are not currently logged in.`);
	  } 
	  
	  else if (!sessionManager.findSessionById(req.headers.cookie.split("=")[1])) {
		  res.redirect(`/login`);
	  } else {
	  		next();
	  	}
  
  } else {
	  next();
  }
};

export default requireAuth;
