
<template>
  <div>
    <h2>Регистрация</h2>
    <form @submit.prevent="register">
      <p class="role_label">Выберите тип Пользователя</p>
      <label><input type="radio" class="role_radio" v-model="role" :value="1" required>Пользователь</label>
      <label><input type="radio" class="role_radio" v-model="role" :value="2" required>Организация</label>
      <label for="" class="username_label">Имя</label>
      <input v-model="username" type="text" class="username">
      <label for="" class="email_label">Email</label>
      <input  v-model="email" type="email"  />
      <label for="" class="password_label">Пароль</label>
      <input v-model="password" type="password" />
      <button  type="submit">Зарегистрироваться</button>
    </form>
  </div>
</template>

<script>
import { store } from '../store.js'
import axiosInstance, { API_URL } from '../http.js'
import { computed, onMounted } from 'vue'
import axios from 'axios'

const roles = computed(() => store.state.roles) 


export default {
  setup() {
    onMounted(() => {
      axios.get(`http://127.0.0.1:8000/api/roles/`)
        .then((res) => {
          store.commit('setRoles', res.data)
          console.log(res)
        })
        .catch((err) => {
          console.log(err)
        })
    })
},
  data() {
    return {
      email: '',
      username: '',
      role: '',
      password: '',
      roles: roles,

    };
  },
  methods: {
    async register() {
      // let roleUrl = this.roles.find(role => role.id === this.role).url
      await 
        axios.post(`http://127.0.0.1:8000/api/users/`, {
          email: this.email,
          password: this.password,
          username: this.username,
          role: this.roles.find(role => role.id === this.role).url
        })
        .then((res) => {
          console.log(res.data)
          
        })
        .catch((err) => {
          console.log(err)
        })
      await axiosInstance
        .post(`token/`, {
          email: this.email,
          password: this.password
          
        })
        .then((res) => {
          window.localStorage.setItem('access_token', res.data.access)
          window.localStorage.setItem('refresh_token', res.data.refresh)
          store.commit('setIsAuthenticated', Boolean(res.data.access))
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
          } else {
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
  }
};
</script>

