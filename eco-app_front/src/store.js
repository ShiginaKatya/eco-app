import { createStore } from 'vuex'

export const store = createStore({
  state() {
    return {
      isAuthenticated: Boolean(window.localStorage.getItem('refresh_token')),
      users: [],
      user: {},
      roles: [],
    }
  },
  getters: {
   
  },
  mutations: {
    setIsAuthenticated(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated
    },
    setUsers(state, usersList) {
      state.users = usersList
    },
    setUser(state, user) {
        state.user = user
      },
    setRoles(state, roles) {
        state.roles = roles
      },
}
}
)
