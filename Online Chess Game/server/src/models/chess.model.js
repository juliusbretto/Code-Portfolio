import Bishop from "./Pieces/bishop.model.js";
import King from "./Pieces/king.model.js";
import Knight from "./Pieces/knight.model.js";
import Pawn from "./Pieces/pawn.model.js";
import Queen from "./Pieces/queen.model.js";
import Rook from "./Pieces/rook.model.js";

class Chess {
  constructor(fenString, turn, player1, player2, colour) {
    this.gameboard = Chess.fenToGameboard(fenString);
    this.turn = turn;
    this.win = false;
    this.winner = "";
    this.loser = "";
    this.player1 = player1;
    this.player2 = player2;
    if (colour) {
      this.player1 = player2;
      this.player2 = player1;
    }
    this.msg = this.getMsgTurn(this.turn);
  }

  move(x1, y1, x2, y2) {
    const piece = this.gameboard[x1][y1];
    if (piece !== "") {
      if (
        (this.turn && piece === piece.toLowerCase()) ||
        (!this.turn && piece === piece.toUpperCase())
      ) {
        if (
          (this.turn &&
            this.gameboard[x2][y2] === this.gameboard[x2][y2].toUpperCase()) ||
          (!this.turn &&
            this.gameboard[x2][y2] === this.gameboard[x2][y2].toLowerCase())
        ) {
          if (!this.blocked(x1, y1, x2, y2)) {
            if (this.moveable(x1, y1, x2, y2)) {
              if (
                (this.turn && this.gameboard[x2][y2] === "K") ||
                (!this.turn && this.gameboard[x2][y2] === "k")
              ) {
                this.win = true;
                if (this.turn) {
                  this.loser = this.player1;
                  this.winner = this.player2;
                } else {
                  this.winner = this.player1;
                  this.loser = this.player2;
                }
              }
              this.gameboard[x2][y2] = this.gameboard[x1][y1];
              this.gameboard[x1][y1] = "";
              this.turn = !this.turn;
              this.msg = this.getMsgTurn(this.turn);
              return true;
            }

            this.msg = "Not a legal move";
            return false;
          }
          this.msg = "Blocked by other piece";
          return false;
        }

        this.msg = "Occupied spot";
        return false;
      }

      this.msg = "Opponents piece";
      return false;
    }

    this.msg = "Empty square";
    return false;
  }

  getMsg() {
    return this.msg;
  }

  setMsg(msg) {
    this.msg = msg;
  }

  getWin() {
    return this.win;
  }

  getTurn() {
    return this.turn;
  }

  getGameboard() {
    return this.gameboard;
  }

  getWinner() {
    return this.winner;
  }

  getLoser() {
    return this.loser;
  }

  getMsgTurn(turn) {
    if (turn) {
      return `It's ${this.player2}'s turn`;
    }
    return `It's ${this.player1}'s turn`;
  }

  moveable(x1, y1, x2, y2) {
    const piece = this.gameboard[x1][y1].toUpperCase();
    const attack = this.gameboard[x2][y2] !== "";

    switch (piece) {
      case "B":
        return Bishop.move(x1, y1, x2, y2);
      case "K":
        return King.move(x1, y1, x2, y2);
      case "P":
        return Pawn.move(x1, y1, x2, y2, this.turn, attack);
      case "R":
        return Rook.move(x1, y1, x2, y2);
      case "N":
        return Knight.move(x1, y1, x2, y2);
      case "Q":
        return Queen.move(x1, y1, x2, y2);
      default:
        return false;
    }
  }

  blocked(y1, x1, y2, x2) {
    const incrX = Math.sign(x2 - x1);
    const incrY = Math.sign(y2 - y1);

    if (x1 === x2 || y1 === y2 || Math.abs(x1 - x2) === Math.abs(y1 - y2)) {
      let limit = Math.abs(x1 - x2);
      if (incrX === 0) {
        limit = Math.abs(y1 - y2);
      }
      for (let i = 1; i < limit; i += 1) {
        if (this.gameboard[y1 + i * incrY][x1 + i * incrX] !== "") {
          return true;
        }
      }
    }
    return false;
  }

  static fenToGameboard(fenString) {
    const matrix = [];
    const rows = fenString.split("/");

    rows.forEach((row) => {
      const newRow = [];

      row.split("").forEach((char) => {
        if (char >= "0" && char <= "9") {
          for (let i = 0; i < parseInt(char, 10); i += 1) {
            newRow.push("");
          }
        } else {
          newRow.push(char);
        }
      });
      matrix.push(newRow);
    });
    return matrix;
  }

  gameboardToFen() {
    const fen = [];
    for (let i = 0; i < this.gameboard.length; i += 1) {
      let emptyCount = 0;
      let fenRow = "";
      for (let j = 0; j < this.gameboard[i].length; j += 1) {
        if (this.gameboard[i][j] === "") {
          emptyCount += 1;
          if (j === this.gameboard[i].length - 1) {
            fenRow += emptyCount;
          }
        } else {
          if (emptyCount > 0) {
            fenRow += emptyCount;
            emptyCount = 0;
          }
          fenRow += this.gameboard[i][j];
        }
      }
      fen.push(fenRow);
    }
    return fen.join("/");
  }
}
export default Chess;
