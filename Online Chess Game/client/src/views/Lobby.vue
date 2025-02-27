<template>
  <div class="container">
    <b-card class="text-center" bg-variant="light">
      <div class="card-header">
        <h4 class="title">WELCOME {{ name }}</h4>
        <hr class="my-2" />
      </div>
      <div class="card-body">
        <button
          class="button btn btn-light mt-4 w-50"
          type="button"
          @click="redirect('/newgame')"
        >
          Create New Game
        </button>
        <br />
        <button
          class="button btn btn-light mt-4 w-50"
          type="button"
          @click="redirect('/showgames')"
        >
          Join Game
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
    name: "",
  }),
  async mounted() {
    try {
      await fetch("/api/lobby", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      })
        .then((res) => res.json())
        .then(({ name }) => {
          this.name = name;
        });
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    redirect(target) {
      this.$router.push(target).catch((e) => console.log(e.message));
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
</style>
