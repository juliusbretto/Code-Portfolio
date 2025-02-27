<template>
  <div class="container">
    <b-card class="text-center" bg-variant="light">
      <div class="card-header">
        <h4 class="title">GAMES</h4>
        <hr class="my-2" />
      </div>
      <div class="card-body">
        <div class="min-height">
          <div v-for="(match, index) in matches" :key="index">
            <button
              v-if="match[0]"
              class="button btn btn-light mt-4 w-50 btn-white"
              type="button"
              @click="join(match)"
            >
              <h1>♞</h1>
              @{{ match[1] }} <br />
              JOIN GAME
            </button>
            <button
              v-if="!match[0]"
              class="button btn btn-light mt-4 w-50 btn-black"
              type="button"
              @click="join(match)"
            >
              <h1>♞</h1>
              @{{ match[1] }} <br />
              JOIN GAME
            </button>
          </div>
        </div>
        <button
          type="button"
          class="cancel-button btn btn-light"
          @click="redirect('/lobby')"
        >
          GO BACK
        </button>
      </div>
    </b-card>
    <br />
  </div>
</template>

<script>
export default {
  name: "ShowGames",
  components: {},
  data: () => ({
    matches: [],
    msg: "",
  }),
  async mounted() {
    try {
      await fetch("/api/matches", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      })
        .then((res) => res.json())
        .then(({ matches }) => {
          this.matches = matches;
        });
    } catch (error) {
      console.error(error);
    }

    const { socket } = this.$root;

    socket.on("newmatch", (newMatch) => {
      this.matches.push(newMatch);
    });

    socket.on("joined", (matchId) => {
      const index = this.matches.findIndex((match) => match[2] === matchId);
      this.matches.splice(index, 1);
    });

    socket.on("cancelmatch", (matchId) => {
      const index = this.matches.findIndex((match) => match[2] === matchId);
      this.matches.splice(index, 1);
    });
  },
  methods: {
    redirect(target) {
      this.$router.push(target).catch((e) => console.log(e.message));
    },
    async join(match) {
      try {
        await fetch("/api/joinmatch", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            matchId: match[2],
          }),
        }).then(async (res) => {
          if (res.status === 200) {
            this.$router.push("/game").catch((e) => console.log(e.message));
          } else {
            this.msg = "Something went wrong";
          }
        });
      } catch (error) {
        console.error(error);
      }
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
}

.custom-card {
  font-family: Garamond, serif;
  width: 100%;
  text-align: center;
  text-transform: uppercase;
}

.title {
  font-family: Garamond, serif;
  width: 100%;
  text-align: center;
  text-transform: uppercase;
}

.button {
  width: 50%;
  margin-top: 1rem;
  background-color: #eeeae5;
  border-radius: 10px;
}

.sticky {
  position: sticky;
  bottom: 30px;
}

.btn-white {
  background-color: #eeeae5;
  color: #333;
}

.min-height {
  min-height: 150px;
}

.btn-black {
  background-color: #333; /* Or any dark color */
  color: #eeeae5;
}
</style>
