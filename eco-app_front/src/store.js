import { createStore } from 'vuex'

export const store = createStore({
  state() {
    return {
      isAuthenticated: Boolean(window.localStorage.getItem('refresh_token')),
      users: [],
      user: {},
      roles: [],
      plans: [],
      habits: [],
      plan: {},
      achievement: {},
      challenges: [],
      userchallenge: {},
      userchallenges: [],
      userstat: {},

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
    setPlans(state, plans) {
      state.plans = plans
    },
    setHabits(state, habits) {
      state.habits = habits
    },
    setPlan(state, plan) {
      state.plan = plan
    },
    setAchievement(state, achievement) {
      state.achievement = achievement
    },
    setChallenges(state, challenges) {
      state.challenges = challenges
    },
    setUserChallenge(state, userchallenge) {
      state.userchallenge = userchallenge
    },
    setUserChallenges(state, userchallenges) {
      state.userchallenges = userchallenges
    },
    setUserStat(state, userstat) {
      state.userstat = userstat
    }

}
}
)
