import betterLogging from "better-logging";
import cookie from "cookie";
import cookieParser from "cookie-parser";
import express from "express";
import expressSession from "express-session";
import socketIOSession from "express-socket.io-session";
import fs from "fs";
import helmet from "helmet";
import { createServer } from "https";
import { Server } from "socket.io";
import auth from "./controllers/auth.controller.js";
import match from "./controllers/match.controller.js";
import profile from "./controllers/profile.controller.js";
import model from "./model.js";
import { resolvePath } from "./util.js";

const port = 8989;
const app = express();

const privateKey = fs.readFileSync(
  "/Users/juliusbretto/Desktop/Skola/KTH/3/Internetprogrammering/juliuseb-norahu-project/cert/private.key",
  "utf8"
);
const certificate = fs.readFileSync(
  "/Users/juliusbretto/Desktop/Skola/KTH/3/Internetprogrammering/juliuseb-norahu-project/cert/certificate.crt",
  "utf8"
);
const credentials = { key: privateKey, cert: certificate };

const server = createServer(credentials, app);
const io = new Server(server);

const { Theme } = betterLogging;
betterLogging(console, {
  color: Theme.green,
});

// Enable debug output
console.logLevel = 4;

// Register a custom middleware for logging incoming requests
app.use(
  betterLogging.expressMiddleware(console, {
    ip: { show: true, color: Theme.green.base },
    method: { show: true, color: Theme.green.base },
    header: { show: false },
    path: { show: true },
    body: { show: true },
  })
);

// Use Helmet!
app.use(helmet());

// Configure session management
const sessionConf = expressSession({
  secret: "Super secret! Shh! Do not tell anyone...",
  resave: true,
  saveUninitialized: true,
});

app.use(sessionConf);
io.use(
  socketIOSession(sessionConf, {
    autoSave: true,
    saveUninitialized: true,
  })
);

// Use cookie-parser middleware
app.use(cookieParser());

// Serve static files
app.use(express.static(resolvePath("client", "dist")));

// Register middlewares that parse the body of the request, available under req.body property
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Bind REST controllers to /api/*
app.use("/api", auth.router);
app.use("/api", auth.requireAuth, profile.router);
app.use("/api", auth.requireAuth, match.router);

// Initialize a model
model.init(io);
await model.setupUsers();
await model.setupMatches();

// Handle socket.io connections
io.on("connection", (socket) => {
  const { session } = socket.handshake;
  session.socketID = socket.id;

  const cookieHeader = socket.handshake.headers.cookie;
  const { sessionCookie } = cookie.parse(cookieHeader);
  if (sessionCookie) {
    model.connected(sessionCookie);
  }

  session.save((err) => {
    if (err) console.error(err);
    else console.debug(`Saved socketID: ${session.socketID}`);
  });
});

server.listen(port, () => {
  console.log(`Listening on https://localhost:${port}/`);
});
