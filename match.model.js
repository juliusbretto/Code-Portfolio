import Chess from "./chess.model.js";

class Match {
  constructor(id, player, colour) {
    this.id = id;
    this.player1 = player;
    this.player2 = null;
    this.colour = colour;
    this.game = null;
  }

  /**
   * Add the second player to the match.
   * @returns  {void}
   */
  joinMatch(player) {
    if (this.player2 === null) {
      this.player2 = player;
      this.game = new Chess(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
        false,
        this.player1.getName(),
        this.player2.getName(),
        this.colour
      );
      return true;
    }

    return false;
  }

  getTurn(id) {
    if (
      (this.player1.getId() === id && !this.colour) ||
      (this.player2.getId() === id && this.colour)
    ) {
      return !this.game.getTurn();
    }

    return this.game.getTurn();
  }

  getOpponent(id) {
    if (this.player1.getId() === id) {
      if (this.player2) {
        return this.player2.getName();
      }
      return "";
    }

    return this.player1.getName();
  }

  getColour(id) {
    if (this.player1.getId() === id) {
      return this.colour;
    }

    return !this.colour;
  }

  getMsg() {
    return this.game.getMsg();
  }

  getWin() {
    return this.game.getWin();
  }

  move(x1, y1, x2, y2) {
    return this.game.move(x1, y1, x2, y2);
  }

  getGameboard() {
    return this.game.getGameboard();
  }

  getFen() {
    return this.game.gameboardToFen();
  }

  getWinner() {
    return this.game.getWinner();
  }

  getLoser() {
    return this.game.getLoser();
  }

  isStarted() {
    return this.player2 !== null;
  }

  getGameColour() {
    return this.colour;
  }

  getGameTurn() {
    return this.game.getTurn();
  }

  getHost() {
    return this.player1.getName();
  }

  getId() {
    return this.id;
  }

  isPlayer(id) {
    if (
      this.player1.getId() === id ||
      (this.player2 && this.player2.getId() === id)
    ) {
      return true;
    }
    return false;
  }

  player1Id() {
    return this.player1.getId();
  }

  player2Id() {
    if (this.player2) {
      return this.player2.getId();
    }
    return null;
  }

  setMsg(msg) {
    this.game.setMsg(msg);
  }

  setData(player2, fen, turn) {
    this.player2 = player2;
    this.game = new Chess(
      fen,
      turn,
      this.player1.getName(),
      this.player2.getName(),
      this.colour
    );
  }
}
export default Match;
