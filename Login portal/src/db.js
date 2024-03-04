import sqlite3 from "sqlite3";
import { open } from "sqlite";
import { resolvePath } from "./util.js";

sqlite3.verbose();

// Open and initialize the database
const db = await open({
  filename: resolvePath("db.sqlite"),
  driver: sqlite3.Database,
});

await db.run("DROP TABLE IF EXISTS userinfo");
await db.run("CREATE TABLE userinfo (username TEXT NOT NULL, password TEXT NOT NULL)");

export default db;
