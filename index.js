import { createRouter, createWebHistory } from "vue-router";
import store from "../store";
import Game from "../views/Game.vue";
import Lobby from "../views/Lobby.vue";
import Login from "../views/Login.vue";
import MatchHistory from "../views/MatchHistory.vue";
import NewGame from "../views/NewGame.vue";
import Profile from "../views/Profile.vue";
import Register from "../views/Register.vue";
import ShowGames from "../views/ShowGames.vue";
import WaitingRoom from "../views/WaitingRoom.vue";

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    component: Login,
  },
  {
    path: "/lobby",
    component: Lobby,
  },
  {
    path: "/newgame",
    component: NewGame,
  },
  {
    path: "/profile",
    component: Profile,
  },
  {
    path: "/showgames",
    component: ShowGames,
  },
  {
    path: "/game",
    component: Game,
  },
  {
    path: "/register",
    component: Register,
  },
  {
    path: "/waitingroom",
    component: WaitingRoom,
  },
  {
    path: "/matchhistory",
    component: MatchHistory,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Setup authentication guard.
router.beforeEach((to, from, next) => {
  if (
    !(to.path === "/login" || to.path === "/register") &&
    !store.state.authenticated
  ) {
    console.info("Unauthenticated user. Redirecting to login page.");
    next("/login");
  } else {
    next();
  }
});

export default router;
