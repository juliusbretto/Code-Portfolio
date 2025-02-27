import { createStore } from "vuex";

export default createStore({
  state: {
    message: null,
    messageVariant: "alert-danger",
    authenticated: false,
    user: null,
  },
  getters: {
    authMessage(state) {
      return state.message;
    },
    authMessageVariant(state) {
      return state.messageVariant;
    },
    isAuthenticated(state) {
      return state.authenticated;
    },
    username(state) {
      return state.user;
    },
  },
  mutations: {
    setAuthenticated(state, { user, authenticated }) {
      state.authenticated = authenticated;
      state.user = user;
    },
    setAuthMessage(state, { message, variant }) {
      state.message = message;
      state.messageVariant = variant;
    },
  },
  actions: {},
  modules: {},
});
