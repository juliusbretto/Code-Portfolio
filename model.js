import bcrypt from "bcrypt";
import { v4 as uuidv4 } from "uuid";
import db from "./db.js";
import Match from "./models/match.model.js";
import User from "./models/user.model.js";

class Model {
  constructor() {
    this.users = {};
    this.matches = {};
    this.timers = {};
    this.io = undefined;
    this.unconnected = {};
  }

  /**
   * Initialize the model after its creation.
   * @param {SocketIO.Server} io - The socket.io server instance.
   * @returns {void}
   */
  init(io) {
    this.io = io;
  }

  /**
   * Create an user with the given name.
   * @param {String} username - The username of the user.
   * @param {String} password - The typed in password when trying to login.
   */
  async createUser(username, password) {
    let id = null;
    const user = await db.get(
      "SELECT * FROM userinfo WHERE username = (?)",
      username
    );
    if (user && (await bcrypt.compare(password, user.password))) {
      id = uuidv4();
      await db.run("INSERT INTO sessions (username, id) VALUES (?,?)", [
        username,
        id,
      ]);
      this.users[id] = new User(username, id);
      this.timers[id] = setTimeout(() => {
        this.forceLogout(id);
      }, 30000);
    }
    return id;
  }

  async getStats(id) {
    const username = this.users[id].getName();
    const user = await db.get(
      "SELECT * FROM userinfo WHERE username = (?)",
      username
    );
    if (user) {
      return [user.wins, user.losses, user.total];
    }
    return null;
  }

  /**
   * Return the user object with the matching id.
   * @param {String} id - An unique identifier for the user session.
   * @returns {User}
   */
  findUserById(id) {
    return this.users[id];
  }

  /**
   * Deletes the user object with the matching id.
   * @param {String} id - An unique identifier for the user session.
   * @returns {void}
   */
  async deleteUserById(id) {
    clearTimeout(this.timers[id]);
    await db.run("DELETE FROM sessions WHERE id = ?", [id]);
    delete this.timers[id];
    delete this.users[id];
  }

  /**
   * Inserts a new user with the given name and password to the datbase.
   * @param {String} username - The username of the user.
   * @param {String} password - The typed in password when trying to register.
   */
  async registerUser(username, password) {
    const hashedPassword = await bcrypt.hash(password, 10);
    await db.run("INSERT INTO userinfo (username, password) VALUES (?,?)", [
      username,
      hashedPassword,
    ]);
    const id = uuidv4();
    await db.run("INSERT INTO sessions (username, id) VALUES (?,?)", [
      username,
      id,
    ]);
    this.users[id] = new User(username, id);
    this.timers[id] = setTimeout(() => {
      this.forceLogout(id);
    }, 30000);
    return id;
  }

  activityUpdate(active, id) {
    if (this.users[id]) {
      if (active) {
        clearTimeout(this.timers[id]);
        this.timers[id] = setTimeout(() => {
          this.forceLogout(id);
        }, 30000);
      }
      return true;
    }
    return false;
  }

  /**
   * Create an user with the given name.
   * @param {String} id - The cookie session id of the user.
   */
  async createMatch(id, colour) {
    const user = this.users[id];
    let matchId = null;
    if (user) {
      matchId = uuidv4();
      let nbrColour = 0;
      if (colour) {
        nbrColour = 1;
      }
      await db.run(
        "INSERT INTO matches (id, playerOne, playerOneId, colour) VALUES (?,?,?,?)",
        [matchId, user.getName(), id, nbrColour]
      );
      this.matches[matchId] = new Match(matchId, user, colour);
    }
    return matchId;
  }

  /**
   * Joins player to match by id.
   * @returns {boolean}
   */
  async joinMatch(matchId, id) {
    const player = this.users[id];
    if (player) {
      const joined = this.matches[matchId].joinMatch(player);
      if (joined) {
        await db.run(
          "UPDATE matches SET playerTwo = ?, playerTwoId=?, fen = ? WHERE id = ?",
          player.getName(),
          id,
          "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
          matchId
        );
      }
      return joined;
    }
    return false;
  }

  /**
   * Moves piece to coordinates in match by id.
   * @returns {boolean}
   */
  async move(matchId, x1, y1, x2, y2) {
    if (
      this.matches[matchId] &&
      !this.unconnected[this.matches[matchId].player1Id()] &&
      !this.unconnected[this.matches[matchId].player2Id()]
    ) {
      const moved = this.matches[matchId].move(x1, y1, x2, y2);
      if (moved) {
        let turn = 0;
        if (this.matches[matchId].getGameTurn()) {
          turn = 1;
        }
        await db.run(
          "UPDATE matches SET fen = ?, turn = ? WHERE id = ?",
          this.matches[matchId].getFen(),
          turn,
          matchId
        );
      }
      return moved;
    }
    this.matches[matchId].setMsg("Server has lost connection");
    return false;
  }

  getMsg(matchId) {
    let msg = "";
    if (this.matches[matchId]) {
      msg = this.matches[matchId].getMsg();
    }
    return msg;
  }

  getTurn(matchId, id) {
    if (this.matches[matchId]) {
      return this.matches[matchId].getTurn(id);
    }
    return null;
  }

  getGameboard(matchId) {
    if (this.matches[matchId]) {
      return this.matches[matchId].getGameboard();
    }
    return null;
  }

  getColour(matchId, id) {
    if (this.matches[matchId]) {
      return this.matches[matchId].getColour(id);
    }
    return null;
  }

  getOpponent(matchId, id) {
    if (this.matches[matchId]) {
      return this.matches[matchId].getOpponent(id);
    }
    return null;
  }

  static async updateStats(winner, loser) {
    await db.run(
      "UPDATE userinfo SET wins = wins + 1, total = total + 1 WHERE username = ?",
      [winner]
    );
    await db.run(
      "UPDATE userinfo SET losses = losses + 1, total = total + 1 WHERE username = ?",
      [loser]
    );
  }

  async checkWin(matchId) {
    const win = this.matches[matchId].getWin();
    if (win) {
      const winner = this.matches[matchId].getWinner();
      const loser = this.matches[matchId].getLoser();
      await Model.updateStats(winner, loser);
      await db.run(
        "UPDATE matches SET winner = ? WHERE id = ?",
        winner,
        matchId
      );
      delete this.matches[matchId];
    }
    return win;
  }

  /**
   * Return all the matches.
   * @returns {Match []}
   */
  getMatches() {
    const freeMatches = [];
    Object.keys(this.matches).forEach((key) => {
      const match = this.matches[key];
      if (!match.isStarted()) {
        const matchData = [
          match.getGameColour(),
          match.getHost(),
          match.getId(),
        ];
        freeMatches.push(matchData);
      }
    });
    return freeMatches;
  }

  /**
   * Deletes the match object with the matching id.
   * @param {String} id - An unique identifier for the match session.
   * @returns {void}
   */
  async deleteMatchById(matchId, id) {
    if (this.matches[matchId]) {
      if (this.matches[matchId].isStarted()) {
        await Model.updateStats(
          this.getOpponent(matchId, id),
          this.findUserById(id).getName()
        );
        await db.run(
          "UPDATE matches SET winner = ? WHERE id = ?",
          this.getOpponent(matchId, id),
          matchId
        );
      } else {
        await db.run("DELETE FROM matches WHERE id = ?", [matchId]);
      }
      delete this.matches[matchId];
    }
  }

  /**
   * Gets the match object with the matching id.
   * @param {String} id - An unique identifier for the match session.
   * @returns {Match}
   */
  getMatchById(id) {
    return this.matches[id];
  }

  async getUserMatches(id) {
    const player = this.users[id];
    const userMatches = [];
    if (player) {
      await db.each(
        "SELECT * FROM matches WHERE playerOne = ? OR playerTwo = ?",
        [player.getName(), player.getName()],
        (err, row) => {
          const matchData = [
            row.playerOne,
            row.playerTwo,
            row.colour,
            row.winner,
          ];
          userMatches.push(matchData);
        }
      );
    }
    return userMatches;
  }

  async setupUsers() {
    await db.each("SELECT * FROM sessions", [], (err, row) => {
      this.users[row.id] = new User(row.username, row.id);
      this.timers[row.id] = setTimeout(() => {
        this.forceLogout(row.id);
      }, 30000);
      this.unconnected[row.id] = true;
      console.log(`row user: ${row.username} row id: ${row.id}`);
    });
  }

  async setupMatches() {
    await db.each(
      "SELECT * FROM matches WHERE winner IS NULL",
      [],
      (err, row) => {
        const player1 = this.users[row.playerOneId];
        let colour = false;
        if (row.colour === 1) {
          colour = true;
        }
        const match = new Match(row.id, player1, colour);
        if (row.playerTwoId) {
          let turn = false;
          if (row.turn === 1) {
            turn = true;
          }
          const player2 = this.users[row.playerTwoId];
          match.setData(player2, row.fen, turn);
        }
        this.matches[row.id] = match;
      }
    );
  }

  async forceLogout(id) {
    Object.keys(this.matches).forEach(async (key) => {
      const match = this.matches[key];
      if (match.isPlayer(id)) {
        const started = match.isStarted();
        const matchId = match.getId();
        const opponent = match.getOpponent(id);
        await this.deleteMatchById(matchId, id);

        if (started) {
          this.broadcast(`exit/${matchId}`, opponent);
        } else {
          this.broadcast("cancelmatch", matchId);
        }
      }
    });
    await this.deleteUserById(id);
  }

  connected(sessionCookie) {
    if (sessionCookie in this.unconnected) {
      delete this.unconnected[sessionCookie];
      console.log(`connected ${sessionCookie}`);
    }
  }

  broadcast(msgType, message) {
    this.io.emit(msgType, message);
  }

  emitToId(msgType, socketId) {
    this.io.to(socketId).emit(msgType);
  }
}

export default new Model();
