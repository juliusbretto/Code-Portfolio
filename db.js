import { open } from "sqlite";
import sqlite3 from "sqlite3";
import { resolvePath } from "./util.js";

sqlite3.verbose();

// Open and initialize the database
const db = await open({
  filename: resolvePath("db.sqlite"),
  driver: sqlite3.Database,
});

//await db.run("DROP TABLE IF EXISTS userinfo");
await db.run(
  "CREATE TABLE IF NOT EXISTS userinfo(username TEXT NOT NULL, password TEXT NOT NULL, wins INTEGER DEFAULT 0, losses INTEGER DEFAULT 0, total INTEGER DEFAULT 0)"
);

//await db.run("DROP TABLE IF EXISTS matches");
await db.run(
  "CREATE TABLE IF NOT EXISTS matches(id TEXT NOT NULL, playerOne TEXT NOT NULL, playerOneId TEXT NOT NULL, playerTwo TEXT, playerTwoId TEXT, colour BOOLEAN DEFAULT 0, fen TEXT, turn BOOLEAN DEFAULT 0, winner TEXT)"
);

//await db.run("DROP TABLE IF EXISTS sessions");
await db.run(
  "CREATE TABLE IF NOT EXISTS sessions(username TEXT NOT NULL, id TEXT NOT NULL)"
);

export default db;
