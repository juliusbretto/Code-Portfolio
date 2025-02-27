<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">CHESS</a>
    <button
      class="navbar-toggler mx-2 mb-2"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarNav"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div id="navbarNav" class="collapse navbar-collapse mx-2">
      <ul class="navbar-nav">
        <li class="nav-item dropdown">
          <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown"
            >MY PAGES</a
          >
          <div class="dropdown-menu">
            <a href="#" class="dropdown-item" @click="redirect('/profile')"
              >PROFILE</a
            >
            <a href="#" class="dropdown-item" @click="redirect('/matchhistory')"
              >MATCH HISTORY</a
            >
            <a
              href="#"
              class="dropdown-item"
              :disabled="!$store.getters.isAuthenticated"
              @click="logout()"
              >SIGN OUT</a
            >
          </div>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#" @click="redirect('/lobby')">GAMES</a>
        </li>
      </ul>
    </div>
  </nav>
  <section class="container-fluid py-4">
    <router-view />
  </section>
</template>

<script>
// @ is an alias to /src
import "bootstrap";
import io from "socket.io-client";

export default {
  name: "App",
  components: {},
  data: () => ({
    socket: io(/* socket.io options */).connect(),
  }),
  computed: {
    authenticated() {
      return this.$store.getters.isAuthenticated;
    },
  },
  watch: {
    authenticated: {
      handler(value) {
        if (value === false) {
          clearInterval(this.interval);
          this.removelisteners(this.regActivity);
        }
        if (value === true) {
          this.setlisteners(this.regActivity);
          this.interval = setInterval(async () => {
            await this.sendActivityUpdate();
          }, 1000);
        }
      },
    },
  },
  methods: {
    redirect(target) {
      const { commit } = this.$store;
      commit("setAuthMessage", {
        message: null,
        variant: "alert alert-success",
      });
      commit("setBookingMessage", { message: null, variant: "alert-danger" });
      this.$router.push(target).catch((e) => console.log(e.message));
    },
    async logout() {
      const { commit, getters } = this.$store;
      if (getters.isAuthenticated) {
        try {
          await fetch("/api/logout", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
          });
        } catch (error) {
          console.error(error);
        }
        commit("setAuthenticated", { user: null, authenticated: false });
        commit("setAuthMessage", {
          message: "Signed out successfully",
          variant: "alert alert-success",
        });
        this.$router.push("/login");
      }
    },
    setlisteners(f) {
      document.addEventListener("mousemove", f);
      document.addEventListener("keydown", f);
      document.addEventListener("click", f);
    },
    removelisteners(f) {
      document.removeEventListener("keydown", f);
      document.removeEventListener("mousemove", f);
      document.removeEventListener("click", f);
    },
    regActivity() {
      this.active = true;
    },
    async sendActivityUpdate() {
      await fetch("/api/activityupdate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ active: this.active }),
      }).then((res) => {
        if (res.status === 200) {
          this.active = false;
        } else {
          this.forceLogout();
        }
      });
    },
    forceLogout() {
      clearInterval(this.interval);
      this.removelisteners(this.regActivity);
      const { commit, getters } = this.$store;
      if (getters.isAuthenticated) {
        commit("setAuthenticated", { user: null, authenticated: false });
        commit("setAuthMessage", {
          message: "Signed out because of inactivity",
          variant: "alert alert-info",
        });
        this.$router.push("/login");
      }
    },
  },
};
</script>

<style>
@import url("bootstrap/dist/css/bootstrap.css");

html,
body {
  background-color: #edb9ca;
  font-family: Garamond, serif;
}

.navbar-brand {
  padding-left: 20px;
}

.nav-link {
  padding-left: 20px;
}
</style>
