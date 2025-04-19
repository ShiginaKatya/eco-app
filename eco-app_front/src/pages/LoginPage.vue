<template>
  <div class="login_page">
    <h2>Вход в профиль</h2>
    <form class="form" @submit.prevent ="login">
      <label for="" class="form_label">Email</label>
      <input  v-model="email" type="email" class="form_input"  />
      <label for="" class="form_label">Пароль</label>
      <input v-model="password" type="password" class="form_input" />
      <button class="eco-button"  type="submit">Войти</button>
    </form>
  </div>
</template>

<script>
import { store } from '../store.js'
import axiosInstance from '../http.js'


export default {
  data() {
    return {
      email: '',
      password: '',
      // users: store.state.users,
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
          console.log(window.localStorage.getItem('userId'))
          if (window.localStorage.getItem('error')) {
            window.location.href = '/'
            return
          }
          console.log(user.role.title)
          window.location.href = 'profile'
      
        })
        .catch((err) => {
          console.log(err)
        })
    }
  },
}
</script>

<style scoped>
.login_page{
  margin: auto;
  max-width: 1200px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: center;
  align-items: center;
  padding-top: 100px;
}
.form{
  display: flex;
  flex-direction: column;
  gap: 5px;
  border: 1px solid grey;
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;

}
.form .eco-button{
  margin: auto;
}
.form_input{
  height: 30px;
  margin-bottom: 10px;
  padding: 6px;
  font-family: inherit;
}
.form_label{
  font-size: 14px;
  color: grey;
}

</style>
