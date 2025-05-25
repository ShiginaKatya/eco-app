import { createStore } from 'vuex'
import axiosInstance from './http'

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
      advices: [],
      events: [],
      favorites: [],
      personal_advices: [],
      send_advices: [],
      categories: [],
      groups: [],
      favorites: [],
      guides: [],
      send_guides: [],
      send_organizations: [],
      tasks: [],
      week_challenge: [],
      favorite_guides: [],
      favorite_advices: []

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
    },
    setAdvices(state, advices) {
      state.advices = advices
    },
    setEvents(state, events) {
      state.events = events
    },
    setFavorites(state, favorites) {
      state.favorites = favorites
    },
    setPersonalAdvices(state, personal_advices) {
      state.personal_advices = personal_advices
    },
    setSendAdvices(state, send_advices) {
      state.send_advices = send_advices
    },
    setCategories(state, categories) {
      state.categories = categories
    },
    setGroups(state, groups) {
      state.groups = groups
    },
    setFavorites(state, favorites) {
      state.favorites = favorites
    },
    setSendGuides(state, send_guides) {
      state.send_guides = send_guides
    },
    setGuides(state, guides) {
      state.guides = guides
    },
    setSendOrganizations(state, send_organizations) {
      state.send_organizations = send_organizations
    },
    setTasks(state, tasks) {
      state.tasks = tasks
    },
    setWeekChallenge(state, week_challenge) {
      state.week_challenge = week_challenge
    },
    setFavoriteAdvices(state, favorite_advices) {
      state.favorite_advices = favorite_advices
    },
    setFavoriteGuides(state, favorite_guides) {
      state.favorite_guides = favorite_guides
    },

},
  actions: {
    async loadUser({commit}){
      await axiosInstance
        .get(`users/${window.localStorage.getItem('userId')}`)
        .then(res => {
          commit('setUser', res.data); 
          console.log(res.data)
        })
        .catch((err) => {
          console.log(err)
        })
    }
  }
}
)
