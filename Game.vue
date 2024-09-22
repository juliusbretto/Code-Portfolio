<template>
  <div class="container1">
    <h4 class="title">PLAYING AGAINST {{ opponent }}</h4>
    <hr class="my-2" />
    {{ msg }}
  </div>
  <br />
  <Transition name="modal">
    <div v-if="showPopup" class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="title">
            <slot name="header">{{ popuptext }}</slot>
          </div>

          <div class="modal-body">
            <slot name="body">{{ winner }} wins!</slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <button
                type="button"
                class="modal-default-button"
                @click="redirect('/lobby')"
              >
                OK
              </button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </Transition>
  <div class="container1">
    <div class="board">
      <div v-for="(row, rowIndex) in gameboard" :key="rowIndex">
        <div
          v-for="(piece, colIndex) in row"
          :key="colIndex"
          :class="{
            square: true,
            dark: isDarkSquare(rowIndex, colIndex),
            light: isLightSquare(rowIndex, colIndex),
            selected: isSelected(rowIndex, colIndex),
          }"
          @click="selectPiece(rowIndex, colIndex)"
          @keydown.enter="nothing()"
        >
          <img
            v-if="piece !== ''"
            :src="getPieceIcon(piece)"
            alt="Chess Piece"
          />
        </div>
      </div>
    </div>
  </div>
  <br />
  <div class="container1 fixed-height">
    <div v-if="msgAlert" :class="`message-game alert alert-danger`" fade show>
      {{ msgAlert }}
    </div>
  </div>
  <br />
  <button
    type="button"
    class="exit-button btn btn-light"
    @click="redirect('/lobby')"
  >
    EXIT GAME
  </button>
  <br />
</template>

<script>
export default {
  name: "GameView",
  data: () => ({
    gameboard: null,
    msg: "",
    turn: false,
    selected: null,
    black: false,
    opponent: "",
    msgAlert: "",
    matchId: "",
    winner: "",
    showPopup: false,
    popuptext: "",
  }),
  async mounted() {
    try {
      await fetch("/api/setupmatch", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      })
        .then((res) => res.json())
        .then(({ black, opponent, matchId }) => {
          this.black = black;
          this.opponent = opponent;
          this.matchId = matchId;
        });
    } catch (error) {
      console.error(error);
    }

    await this.updateMatch();

    const { socket } = this.$root;

    socket.on(`moved/${this.matchId}`, async () => {
      console.log("new move");
      await this.updateMatch();
    });

    socket.on(`win/${this.matchId}`, (winner) => {
      this.winner = winner;
      this.showPopup = true;
      if (winner === this.opponent) {
        this.popuptext = "GAME OVER";
      } else {
        this.popuptext = "CONGRATULATIONS!";
      }
    });

    socket.on(`exit/${this.matchId}`, (winner) => {
      this.winner = winner;
      this.showPopup = true;
      this.popuptext = `${this.opponent} LEFT THE GAME`;
    });
  },
  async beforeUnmount() {
    try {
      await fetch("/api/exitgame", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      }).then(async (res) => {
        if (res.status === 200) {
          this.$router
            .push("/waitingroom")
            .catch((e) => console.log(e.message));
        } else {
          this.msgAlert = "Something went wrong";
        }
      });
    } catch (error) {
      console.error(error);
    }
    this.redirect(this.$route.path);
  },
  methods: {
    redirect(target) {
      this.$router.push(target).catch((e) => console.log(e.message));
    },
    isDarkSquare(rowIndex, colIndex) {
      return (rowIndex + colIndex) % 2 === 0;
    },
    isLightSquare(rowIndex, colIndex) {
      return (rowIndex + colIndex) % 2 === 1;
    },
    isSelected(rowIndex, colIndex) {
      return (
        this.selected &&
        this.selected.row === rowIndex &&
        this.selected.col === colIndex
      );
    },
    async updateMatch() {
      try {
        await fetch("/api/match", {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        })
          .then((res) => res.json())
          .then(({ gameboard, msg, turn }) => {
            if (gameboard !== null) {
              this.gameboard = gameboard;
              this.msg = msg;
              this.turn = turn;
              this.msgAlert = "";
            }
          });
      } catch (error) {
        console.error(error);
      }
    },
    async selectPiece(rowIndex, colIndex) {
      const piece = this.gameboard[rowIndex][colIndex];
      if (this.selected === null) {
        if (
          this.turn &&
          piece !== "" &&
          ((!this.black && piece.toUpperCase() === piece) ||
            (this.black && piece.toLowerCase() === piece))
        ) {
          this.selected = { row: rowIndex, col: colIndex };
        }
      } else {
        try {
          await fetch("/api/movepiece", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              x1: this.selected.row,
              y1: this.selected.col,
              x2: rowIndex,
              y2: colIndex,
            }),
          })
            .then((res) => res.json())
            .then(({ moved, msg }) => {
              if (!moved) {
                this.msgAlert = msg;
              }
            });
        } catch (error) {
          console.error(error);
        }
        this.selected = null;
      }
    },
    nothing() {},
    getPieceIcon(piece) {
      switch (piece) {
        case "b":
          return "/Icons/Bishop-black.png";
        case "k":
          return "/Icons/King-black.png";
        case "p":
          return "/Icons/Pawn-black.png";
        case "r":
          return "/Icons/Tower-black.png";
        case "n":
          return "/Icons/Horse-black.png";
        case "q":
          return "/Icons/Queen-black.png";
        case "B":
          return "/Icons/Bishop-white.png";
        case "K":
          return "/Icons/King-white.png";
        case "P":
          return "/Icons/Pawn-white.png";
        case "R":
          return "/Icons/Tower-white.png";
        case "N":
          return "/Icons/Horse-white.png";
        case "Q":
          return "/Icons/Queen-white.png";
        default:
          return "";
      }
    },
  },
};
</script>

<style>
.container1 {
  border: 1px solid #ccc; /* Add border */
  border-radius: 10px; /* Add border radius */
  background-color: #fff; /* Set background color to white */
  padding: 20px; /* Add padding */
  max-width: 445px;
  width: 100%;
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}

.title {
  font-family: Garamond, serif;
  width: 100%;
  text-align: center;
  text-transform: uppercase;
}

.board {
  display: grid;
  grid-template-rows: repeat(8, 50px);
  grid-template-columns: repeat(8, 50px);
  grid-gap: 0; /* Remove the gap between grid items */
  background-color: white; /* Set background color to white */
}

.square {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50px;
  height: 50px;
}

.dark {
  background-color: #8b4513; /* Brown color for dark squares */
}

.light {
  background-color: #f5e5c5; /* Light color for light squares */
}

.selected {
  background-color: #e26666; /* Customize the color for the selected square */
}

.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgb(0 0 0 / 50%);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
  justify-content: center; /* Horizontally center the content */
  align-items: center;
}

.modal-container {
  width: 300px;
  margin: 0 auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgb(0 0 0 / 33%);
  transition: all 0.3s ease;
  font-family: Garamond, serif;
  text-align: center;
  text-transform: uppercase;
}

.modal-header {
  margin: 0 auto;
  text-align: center;
}

.modal-body {
  margin: 20px 0;
  text-align: center;
}

.modal-default-button {
  float: right;
  margin-left: auto;
  margin-right: auto;
  width: 100px;
}

.modal-enter-from {
  opacity: 0;
}

.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(1.1);
}

.exit-button {
  border: 1px solid #ccc;
  background-color: #ee6464;
  border-radius: 10px; /* Add border radius */
  padding: 20px; /* Add padding */
  width: 445px;
  text-align: center;
  display: block;
  margin: 10px auto 0;
}

.message-game {
  text-align: center;
  width: 100%;
  display: block;
  margin: auto;
}

.fixed-height {
  height: 100px;
}
</style>
