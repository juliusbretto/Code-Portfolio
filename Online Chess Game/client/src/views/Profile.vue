<template>
  <div class="container">
    <b-card class="text-center" bg-variant="light">
      <div class="card-header">
        <h4 class="title">MY PROFILE - {{ name }}</h4>
        <hr class="my-2" />
      </div>
      <div class="card-body">
        <br />
        <table>
          <tr>
            <th><strong>Game Status</strong></th>
            <th><strong>Number of times</strong></th>
          </tr>
          <tr>
            <td>Win</td>
            <td>{{ wins }}</td>
          </tr>
          <tr>
            <td>Loss</td>
            <td>{{ losses }}</td>
          </tr>
          <tr>
            <td><strong>Total Games</strong></td>
            <td>
              <strong>{{ total }}</strong>
            </td>
          </tr>
        </table>
      </div>
    </b-card>
    <br />
  </div>
</template>

<script>
export default {
  name: "ProfileView",
  components: {},
  data: () => ({
    name: "",
    wins: null,
    total: null,
    losses: null,
  }),
  async mounted() {
    try {
      await fetch("/api/profile", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      })
        .then((res) => res.json())
        .then(({ name, wins, losses, total }) => {
          this.name = name;
          this.wins = wins;
          this.losses = losses;
          this.total = total;
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

table,
th,
td {
  border: 1px solid;
}

table {
  width: 75%;
  margin: 0 auto;
}
</style>
