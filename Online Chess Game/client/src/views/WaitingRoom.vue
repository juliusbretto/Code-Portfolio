<template>
  <div class="container">
    <b-card class="text-center" bg-variant="light">
      <div class="card-header">
        <h4 class="title">WAITING FOR OTHER PLAYER TO JOIN</h4>
        <hr class="my-2" />
      </div>
      <div class="card-body">
        <div v-if="msg" :class="`message alert alert-danger w-50`" fade show>
          {{ msg }}
        </div>
        <br />
        <div class="loader"></div>
        <br />
        <button
          type="button"
          class="cancel-button btn btn-light"
          @click="redirect('/lobby')"
        >
          Cancel Game
        </button>
      </div>
    </b-card>
    <br />
  </div>
</template>

<script>
export default {
  name: "WaitingRoom",
  components: {},
  data: () => ({
    msg: "",
    matchId: "",
  }),
  async mounted() {
    try {
      await fetch("/api/getmatchid", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      })
        .then((res) => res.json())
        .then(({ matchId }) => {
          this.matchId = matchId;
        });
    } catch (error) {
      console.error(error);
    }

    const { socket } = this.$root;

    socket.on(`startmatch/${this.matchId}`, () => {
      this.$router.push("/game").catch((e) => console.log(e.message));
    });
  },
  async beforeUnmount() {
    if (this.$route.path !== "/game") {
      await this.cancel();
    }
    this.redirect(this.$route.path);
  },
  methods: {
    redirect(target) {
      this.$router.push(target).catch((e) => console.log(e.message));
    },
    async cancel() {
      try {
        await fetch("/api/deletematch", {
          method: "GET",
          headers: { "Content-Type": "application/json" },
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

.title {
  font-family: Garamond, serif;
  width: 100%;
  text-align: center;
  text-transform: uppercase;
}

.cancel-button {
  width: 50%;
  margin-top: 1rem;
  margin-right: 10px;
  margin-left: 10px;
  background-color: #ee6464;
}

/* HTML: <div class="loader"></div> */
.loader {
  width: 100px;
  aspect-ratio: 2;

  --g: no-repeat radial-gradient(circle closest-side, #e3d3d3 90%, #0000);

  background: var(--g) 0% 50%, var(--g) 50% 50%, var(--g) 100% 50%;
  background-size: calc(100% / 3) 50%;
  animation: l3 2s infinite linear;
  margin: 0 auto; /* Center horizontally */
}

@keyframes l3 {
  20% {
    background-position: 0% 0%, 50% 50%, 100% 50%;
  }

  40% {
    background-position: 0% 100%, 50% 0%, 100% 50%;
  }

  60% {
    background-position: 0% 50%, 50% 100%, 100% 0%;
  }

  80% {
    background-position: 0% 50%, 50% 50%, 100% 100%;
  }
}
</style>
