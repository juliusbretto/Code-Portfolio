<template>
  <div class="container">
    <b-card class="text-center" bg-variant="light">
      <div class="card-header">
        <h4 class="title">PLEASE SIGN UP</h4>
        <hr class="my-2" />
      </div>

      <div class="card-body">
        <div class="row">
          <form @submit.prevent="register()">
            <div
              v-if="$store.getters.authMessage"
              :class="`message alert ${$store.getters.authMessageVariant} w-50`"
              fade
              show
            >
              {{ $store.getters.authMessage }}
            </div>
            <p>
              <label for="username"></label>
              <input
                id="username"
                v-model="username"
                class="w-50 mt-4"
                type="text"
                placeholder="Username"
                required
              />
            </p>
            <p>
              <label for="password"></label>
              <input
                id="password"
                v-model="password"
                class="w-50"
                type="password"
                placeholder="Password"
                required
              />
            </p>
            <p>
              <label for="confirm"></label>
              <input
                id="confirm"
                v-model="confirm"
                class="w-50"
                type="password"
                placeholder="Confirm"
                required
              />
            </p>
            <button class="btn btn-light mt-4 w-50" type="submit">
              Register
            </button>
          </form>
          <form>
            <button
              class="btn btn-light mt-4 w-50"
              type="button"
              @click="redirect('/login')"
            >
              Sign in
            </button>
          </form>
        </div>
      </div>
    </b-card>
  </div>
</template>

<script>
import xss from "xss";

export default {
  name: "RegisterView",
  components: {},
  data: () => ({
    username: "",
    password: "",
    confirm: "",
  }),
  methods: {
    redirect(target) {
      this.$router.push(target).catch((e) => console.log(e.message));
    },
    async register() {
      const { commit } = this.$store;
      const { push } = this.$router;

      const sanitizedUsername = xss(this.username);
      const sanitizedPassword = xss(this.password);
      const sanitizedConfirm = xss(this.confirm);

      if (
        !(
          sanitizedPassword < 3 ||
          sanitizedUsername.length < 3 ||
          !/\d/.test(sanitizedUsername) ||
          !/\d/.test(sanitizedPassword) ||
          !/[a-zA-Z]/.test(sanitizedUsername) ||
          !/[a-zA-Z]/.test(sanitizedPassword)
        )
      ) {
        await fetch("/api/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: sanitizedUsername,
            password: sanitizedPassword,
            confirm: sanitizedConfirm,
          }),
        })
          .then((res) => res.json())
          .then(({ authenticated, msg }) => {
            if (authenticated === true) {
              commit("setAuthenticated", {
                user: sanitizedUsername,
                authenticated: true,
              });
              push("/lobby");
            } else {
              commit("setAuthMessage", {
                message: msg,
                variant: "alert-danger",
              });
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      } else {
        commit("setAuthMessage", {
          message: "The username or password doesn't meet the requirements",
          variant: "alert-danger",
        });
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
  width: 100%;
  text-align: center;
}

.title {
  font-family: Garamond, serif;
}

.message {
  margin: 0 auto;
}
</style>
