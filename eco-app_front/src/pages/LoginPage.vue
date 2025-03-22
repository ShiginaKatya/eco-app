<template>
  <div>
    <h2>Вход</h2>
    <form @submit.prevent ="login">
      <label for="" class="email_label">Email</label>
      <input  v-model="email" type="email"  />
      <label for="" class="password_label">Пароль</label>
      <input v-model="password" type="password" />
      <button  type="submit">Войти</button>
    </form>
  </div>
</template>
<script>
import { store } from '../store.js'
import axiosInstance, { API_URL } from '../http.js'
import axios from 'axios'
import { onMounted, computed } from 'vue';

export default {
  data() {
    return {
      email: '',
      password: '',
      users: store.state.users,
      step: 1,
    }
  },
  methods: {
    async login() {
      await axiosInstance
        .post(`token/`, {
          email: this.email,
          password: this.password
          
        })
        .then((res) => {
          console.log(1111111)
          window.localStorage.setItem('access_token', res.data.access)
          window.localStorage.setItem('refresh_token', res.data.refresh)
          store.commit('setIsAuthenticated', Boolean(res.data.access))
          console.log('ffjfejj')
        })
        .catch((err) => {
          console.log(err)
        })
      await axiosInstance
        .get('users/')
        .then((res) => {
          let users = res.data
          let user = users.find(user => user.email === this.email)
          window.localStorage.setItem('userId', user.id)
          if (window.localStorage.getItem('error')) {
            window.location.href = '/'
            return
          }
          console.log(user.role.title)
          if (user.role.title === 'Пользователь' ) {
            console.log(user.role.title)
            window.location.href = 'profile'
            return
          }
        })
        .catch((err) => {
          console.log(err)
        })
        .finally(() => {

        })
    }
  },
}
</script>