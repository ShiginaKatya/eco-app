<template>
  <div class="register_page">
    <h2>Регистрация</h2>
    <form class="form" @submit.prevent="register">
      <p class="form_label">Выберите тип Пользователя</p>
      <fieldset class="radio_group">
        <label class="group_label"><input type="radio" class="role_radio" v-model="role" :value="1" required>Пользователь</label>
        <label class="group_label"><input type="radio" class="role_radio" v-model="role" :value="2" required>Организация</label>
      </fieldset>
      <label for="" class="form_label">Имя</label>
      <input v-model="username" type="text" class="form_input">
      <label for="" class="form_label">Email</label>
      <input  v-model="email" type="email" class="form_input" />
      <label for="" class="form_label">Пароль</label>
      <input v-model="password" type="password" class="form_input" />
      <button class="eco-button" type="submit">Зарегистрироваться</button>
      <p>Есть аккаунт?</p>
      <router-link to="/login" class="eco-button">Войти в профиль</router-link>
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
       
    }
  }
};
</script>

<style scoped>
.register_page{
  margin: auto;
  max-width: 1200px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: center;
  align-items: center;
}
.form{
  display: flex;
  flex-direction: column;
  gap: 5px;
  border: 1px solid grey;
  padding: 20px;
  border-radius: 8px;
}
.form .eco-button{
  margin: auto;
}
.form_input{
  height: 30px;
  padding: 10px;
  margin-bottom: 10px;
  font-family: inherit;
}
.radio_group{
  border: none;
  display: flex;
  gap: 30px;
}
.group_label{
  display: flex;
  align-items: center;
  gap: 5px;
  justify-content: flex-start;
}
.form_label{
  font-size: 14px;
  color: grey;
}

</style>

