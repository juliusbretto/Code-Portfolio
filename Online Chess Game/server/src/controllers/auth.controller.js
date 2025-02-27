import { Router } from "express";
import xss from "xss"; // Import the "xss" module
import db from "../db.js";
import model from "../model.js";

const router = Router();

/**
 * API (see the route handlers below) should combine uniquely identifiable resources (paths)
 * with the appropriate HTTP request methods (GET, POST, PUT, DELETE and more) to manipulate them.
 *
 * GET     /rooms                       =>  get all rooms
 * GET     /rooms/{name}/messages       =>  get all messages in a room with the given name
 * POST    /rooms/{name}/messages       =>  create a new message in a room with the given name
 * PUT     /rooms/{name}/messages/{id}  =>  update a message with the given id in a room with the given name
 * DELETE  /rooms/{name}/messages/{id}  =>  delete a message with the given id in a room with the given name
 * etc.
 */

/**
 * requireAuth is a middleware function that limit access to an endpoint to authenticated users.
 * @param {Request} req
 * @param {Response} res
 * @param {Function} next
 * @returns {void}
 */
const requireAuth = (req, res, next) => {
  // Use an unique session identifier to access information about the user making the request
  const id = req.cookies.sessionCookie;

  if (!model.findUserById(id)) {
    // Choose the appropriate HTTP response status code and send an HTTP response, if any, back to the client
    res.status(401).end();
    return;
  }
  next();
};

router.get("/authenticated", async (req, res) => {
  const id = req.cookies.sessionCookie;
  if (model.findUserById(id)) {
    res.status(200).end();
  } else {
    res.status(401).end();
  }
});

router.post("/login", async (req, res) => {
  // Check how to access data being sent as a path, query, header and cookie parameter or in the HTTP request body
  const { username, password } = req.body;

  const sanitizedUsername = xss(username);
  const sanitizedPassword = xss(password);
  console.log(`rensat ${sanitizedUsername}`);
  console.log(`rensat ${sanitizedPassword}`);
  const html = xss('<script>alert("xss");</script>');
  console.log(html);

  if (
    !(
      sanitizedPassword.length < 3 ||
      sanitizedUsername.length < 3 ||
      !/\d/.test(sanitizedUsername) ||
      !/\d/.test(sanitizedPassword) ||
      !/[a-zA-Z]/.test(sanitizedUsername) ||
      !/[a-zA-Z]/.test(sanitizedPassword)
    )
  ) {
    // Create a new user with the given name and associate it with the currently active session
    const id = await model.createUser(sanitizedUsername, sanitizedPassword);
    if (id) {
      res.cookie("sessionCookie", id).status(200).json({ authenticated: true });
    } else {
      res.status(401).json({ authenticated: false });
    }
  } else {
    res.status(401).json({ authenticated: false });
  }
});

router.post("/register", async (req, res) => {
  // Check how to access data being sent as a path, query, header and cookie parameter or in the HTTP request body
  const { username, password, confirm } = req.body;

  const sanitizedUsername = xss(username);
  const sanitizedPassword = xss(password);
  const sanitizedConfirm = xss(confirm);

  const user = await db.get(
    "SELECT * FROM userinfo WHERE username = (?)",
    sanitizedUsername
  );

  if (!user) {
    if (
      sanitizedUsername.length >= 3 &&
      sanitizedPassword.length >= 3 &&
      /\d/.test(sanitizedUsername) &&
      /\d/.test(sanitizedPassword) &&
      /[a-zA-Z]/.test(sanitizedUsername) &&
      /[a-zA-Z]/.test(sanitizedPassword)
    ) {
      if (sanitizedPassword === sanitizedConfirm) {
        // Create a new user with the given name and associate it with the currently active session
        const id = await model.registerUser(
          sanitizedUsername,
          sanitizedPassword
        );
        if (id) {
          res
            .cookie("sessionCookie", id)
            .status(200)
            .json({ authenticated: true, msg: "Successful" });
        } else {
          res
            .status(401)
            .json({ authenticated: false, msg: "Something went wrong" });
        }
      } else {
        res.status(401).json({
          authenticated: false,
          msg: "Confirm password must be the same as the password",
        });
      }
    } else {
      res.status(401).json({
        authenticated: false,
        msg: "The username or password doesn't meet the requirements",
      });
    }
  } else {
    res.status(401).json({
      authenticated: false,
      msg: `The username ${sanitizedUsername} is already in use. Please select a different username`,
    });
  }
});

export default { router, requireAuth };
