<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu></ProfileMenu>
    </aside>
    <main class="main">
      <div class="main_header"> 
        <h1 class="header_title">Cоветы</h1>
      </div>
      <form>
        <input type="text" placeholder="совет" v-model="advice_text">
        <input type="text" placeholder="описание" v-model="description">
        <button class="eco-button" @click.prevent="sendAdvice()" >Отправить</button>
      </form>
      <div v-if="user.role?.title === 'Администратор'">
        <ul>
          <li v-for="advice in send_advices" :key="advice?.id">
            <p class="advice_title">{{advice.title}}</p>
            <p class="advice_title">{{advice.author.username}}</p>
            <p class="advice_description">{{advice.description}}</p>
            <button @click="postAdvice(advice.id)" class="eco-button">Опубликовать</button>
          </li>
        </ul>
      </div>
      <p class="advice_title personal">Персональные советы</p>
      <ul class="advice_list  personal">
        <li class="advice" v-for="advice in personal_advices" :key="advice?.id">
          <button @click="addFavorite(advice.url)" class="advice_button"></button>
          <img :src="advice.icon" alt="" class="advice_picture">
          <div class="advice_text">
            <p class="advice_title">{{advice.title}}</p>
            <p class="advice_category">{{advice.category?.title}}</p>
            <p class="advice_description">{{advice.description}}</p>
          </div>
        </li>
      </ul>
      <ul class="advice_list">
        <li class="advice" v-for="advice in advices" :key="advice.id">
          <button @click="addFavorite(advice.url)" class="advice_button"></button>
          <img :src="advice.icon" alt="" class="advice_picture">
          <div class="advice_text">
            <p class="advice_title">{{advice.title}}</p>
            <p class="advice_category">{{advice.category?.title}}</p>
            <p class="advice_description">{{advice.description}}</p>
          </div>
        </li>
      </ul>
    </main>
  </div>
</template>

<script>
import ProfileMenu from '../components/ProfileMenu.vue'
import {store} from '../store.js'
import { onMounted, computed } from 'vue';
import axiosInstance from '../http.js'
import axios from 'axios'

const user = computed(() => store.state.user) 
const advices = computed(() => store.state.advices)
const personal_advices = computed(() => store.state.personal_advices)
const send_advices = computed(() => store.state.send_advices)


export default {
    components: {
      ProfileMenu,
    },
    setup() {
      onMounted(async () => {
        await axiosInstance
          .get('/advices?is_posted=True')
          .then(res => {
            console.log(res.data)
            store.commit('setAdvices', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
        await axiosInstance
          .get('/advices/personal')
          .then(res => {
            console.log(res.data)
            store.commit('setPersonalAdvices', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
        await axiosInstance
          .get('/advices?is_posted=False')
          .then(res => {
            console.log(res.data)
            store.commit('setSendAdvices', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
        
      })
    },
    data() {
      return {
        user: user,
        advices: advices,
        personal_advices: personal_advices,
        send_advices: send_advices,
        advice_text: '',
        description: ''
      }
    },
    computed:{
     
    },
    methods: {
      addFavorite(adviceUrl){
        axiosInstance
          .post('favorites/', {
            user: this.user.url,
            advice: adviceUrl,
            favorite_type: 'A'
          })
          .then((res) => {
            console.log(res.data)
          })
          .catch((err) => {
            console.log(err)
          })
        
      },
      async sendAdvice(){
        await axiosInstance
          .post('advices/', {
            author: this.user.url,
            title: this.advice_text,
            description: this.description,
            is_posted: false
          })
      },
      async postAdvice(adviceId){
        await axiosInstance
          .patch(`advices/${adviceId}/`, {
            is_posted: true
          })
      }
    }
}
</script>

<style scoped>
.advice_title{
  font-weight: 500;
  font-family: Golos Text, sans-serif;
  font-size: 16px;
}
.advice_description{
  font-size: 14px;
  color: gray;
}
.advice_category{
  font-size: 14px;
  color: #2E8B57;
}
.advice_picture{
  width: 270px;
  height: auto;

}
.advice{
  width: 300px;
  padding: 16px;
  border: 1px solid lightgray;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.advice_button{
  width: 24px;
  height: 24px ;
  border: none;
  background: transparent;
  background-image: url('favorite_hover.svg');
  background-position: center;
  background-size: cover;
  align-self: flex-end;
}
.advice_button:disabled{
  background-image: url('favorite.svg');
}
.advice_list{
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;
  margin-bottom: 10px;
  padding: 10px;
}
.personal {
  padding: 10px;
}
.personal .advice{
  border: 1px solid #2E8B57;
}
</style>