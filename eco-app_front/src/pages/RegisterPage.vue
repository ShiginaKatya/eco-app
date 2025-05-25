<template>
  <div class="register_page">
    <header class="header">
      <p class="logo_text">ECO GREEN LIFE</p>
      <router-link class="eco-button" to="/">Назад</router-link>
    </header>
    <main class="main">
      <h2>Регистрация</h2>
      <form class="form" @submit.prevent="register">
        <label for="" class="form_label">Имя</label>
        <input v-model="username" type="text" class="form_input">
        <label for="" class="form_label">Email</label>
        <input  v-model="email" type="email" class="form_input" />
        <label for="" class="form_label">Пароль</label>
        <input v-model="password" type="password" class="form_input" />
        <label for="" class="form_label">Подтверждение пароля</label>
        <input v-model="password_confirm" type="password" class="form_input" />
        <p v-if="message">{{ message }}</p>
        <button class="eco-button" type="submit">Зарегистрироваться</button>
        <p>Есть аккаунт?</p>
        <router-link to="/login" class="eco-button">Войти в профиль</router-link>
      </form>
    </main>
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
      password: '',
      roles: roles,
      password_confirm: '',
      message: '',

    };
  },
  methods: {
    async register() {
      // let roleUrl = this.roles.find(role => role.id === this.role).url
      if (this.password === this.password_confirm){
        await 
          axios.post(`http://127.0.0.1:8000/api/users/`, {
            email: this.email,
            password: this.password,
            username: this.username,
            role: this.roles.find(role => role.title === 'Пользователь').url
          })
          .then((res) => {
            console.log(res.data)
          })
          .catch((err) => {
            console.log(err)
          })
      }
      else {
        this.message = 'пароль не совпадает'
      }
      
    }
  }
};
</script>

<style scoped>
.register_page{
  margin:  16px auto;
  max-width: 1200px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.header{
  display: grid;
  gap: 8px;
}
h2{
  text-align: center;
}
.main{
  margin: auto;
  gap: 16px;
}
.form{
  max-width: 400px;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  border: 1px solid grey;
  padding: 16px;
  border-radius: 8px;
}
.form .eco-button{
  margin: auto;
}
.form_input{
  height: 30px;
  font-family: inherit;
}


.form_label{
  font-size: 14px;
  color: grey;
}

</style>

