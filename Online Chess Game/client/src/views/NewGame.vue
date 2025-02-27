<template>
  <div class="container">
    <b-card class="text-center" bg-variant="light">
      <div class="card-header">
        <h4 class="title">CREATE NEW GAME</h4>
        <hr class="my-2" />
      </div>
      <div class="card-body">
        <div v-if="msg" :class="`message alert alert-danger w-50`" fade show>
          {{ msg }}
        </div>
        <div class="switch-container">
          <label for="player-color" class="switch-label"
            >Pick your player colour:</label
          >
          <label class="switch">
            <input type="checkbox" @click="toggleCheckbox" />
            <div class="slider round"></div>
          </label>
        </div>
        <button
          type="button"
          class="create-button btn btn-light"
          @click="createGame()"
        >
          Create Game
        </button>
        <br />
        <button
          type="button"
          class="cancel-button btn btn-light"
          @click="cancel()"
        >
          Cancel
        </button>
      </div>
    </b-card>
    <br />
  </div>
</template>

<script>
export default {
  name: "LobbyView",
  components: {},
  data: () => ({
    msg: "",
    checkbox: false,
  }),
  methods: {
    async createGame() {
      try {
        await fetch("/api/newmatch", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            colour: this.checkbox,
          }),
        }).then(async (res) => {
          if (res.status === 200) {
            this.$router
              .push("/waitingroom")
              .catch((e) => console.log(e.message));
          } else {
            this.msg = "Something went wrong";
          }
        });
      } catch (error) {
        console.error(error);
      }
    },
    cancel() {
      this.$router.push("/lobby").catch((e) => console.log(e.message));
    },
    toggleCheckbox() {
      this.checkbox = !this.checkbox;
    },
  },
};
</script>

<style>
.container {
  border: 1px solid #ccc; /* Add border */
  border-radius: 10px; /* Add border radius */
  background-color: #fff; /* Set background color to white */
  padding: 20px; /* Add padding */
  max-width: 500px;
  justify-content: center; /* Center-align items horizontally */
  align-items: center; /* Center-align items vertically */
}

.custom-card {
  font-family: Garamond, serif;
  width: 100%;
  text-align: center;
  text-transform: uppercase;
  justify-content: center; /* Center-align items horizontally */
  align-items: center; /* Center-align items vertically */
}

.title {
  font-family: Garamond, serif;
  width: 100%;
  text-align: center;
  text-transform: uppercase;
}

.create-button {
  width: 50%;
  margin-top: 1rem;
  margin-right: 10px;
  margin-left: 10px;
  background-color: #d4bc87;
}

.cancel-button {
  width: 50%;
  margin-top: 1rem;
  margin-right: 10px;
  margin-left: 10px;
  background-color: #ee6464;
}

.switch {
  position: relative;
  display: inline-block;
  width: 230px;
  height: 34px;
}

.switch input {
  display: none;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ececec;
  transition: 0.4s;
}

.slider::before {
  position: absolute;
  content: "♕";
  text-align: center;
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.4s;
}

input:checked + .slider {
  background-color: #101010;
}

input:focus + .slider {
  box-shadow: 0 0 1px #101010;
}

input:checked + .slider::before {
  content: "♛";
  transform: translateX(195px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round::before {
  border-radius: 50%;
}

.switch-label {
  margin-right: 65px;
}

.switch-container {
  display: flex;
  width: 100%;
  flex-direction: column; /* Set flex direction to column */
  align-items: center; /* Align items to the center horizontally */
  justify-content: center; /* Center-align items vertically */
}
</style>
