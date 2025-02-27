<template>
  <div class="container">
    <b-card class="text-center" bg-variant="light">
      <div class="card-header">
        <h4 class="title">MATCH HISTORY - {{ name }}</h4>
        <hr class="my-2" />
      </div>
      <div class="card-body">
        <br />
        <table>
          <tr>
            <th><strong>Played Against</strong></th>
            <th><strong>As Colour</strong></th>
            <th><strong>Winner</strong></th>
          </tr>
          <tr v-for="(match, index) in matches" :key="index">
            <td>{{ getOpponent(match[0], match[1]) }}</td>
            <td>{{ getColour(match[1], match[2]) }}</td>
            <td>{{ match[3] }}</td>
          </tr>
        </table>
      </div>
    </b-card>
    <br />
  </div>
</template>

<script>
export default {
  name: "MatchHistory",
  components: {},
  data: () => ({
    name: "",
    matches: null,
  }),
  async mounted() {
    try {
      await fetch("/api/matchhistory", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      })
        .then((res) => res.json())
        .then(({ matches, name }) => {
          this.matches = matches;
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
    getOpponent(name1, name2) {
      if (name1 === this.name) {
        return name2;
      }
      return name1;
    },
    getColour(name2, colour) {
      let gameColour = false;
      if (colour === 1) {
        gameColour = true;
      }

      if (name2 === this.name) {
        gameColour = !gameColour;
      }

      if (gameColour) {
        return "Black";
      }
      return "White";
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
