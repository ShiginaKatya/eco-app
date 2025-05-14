<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu :burgerMenu="openingMenu" @close="closeMenu()"></ProfileMenu>
    </aside>
    <main class="main">
      <section class="main_header"> 
        <h1 class="header_title">Cоветы</h1>
      </section>
      <section class="main_sections">
        <button v-if="user.role?.title === 'Администратор'" class="eco-button" @click="showAddModal()">Добавить совет</button>
        <AddAdvice v-if="adviceModal" @close="closeModal()"></AddAdvice>
        <section class="send_advices" v-if="user.role?.title === 'Администратор'">
          <p class="advice_title personal">Заявки от пользователей</p>
          <ul class="send_list">
            <li class="send_advice" v-for="advice in send_advices" :key="advice?.id">
              <p class="advice_title">{{advice.title}}</p>
              <p class="advice_title">{{advice.author?.username}}</p>
              <p class="advice_description">{{advice.description}}</p>
              <button @click="showChangeModal(advice.url)" class="eco-button">Просмотреть</button>
              <AddAdvice v-if="adviceUrl === advice.url" :advice="advice" @close="closeModal()"></AddAdvice>
            </li>
          </ul>
        </section>
        <p v-if="user.role?.title !== 'Администратор'" class="advice_title personal">Стоит обратить внимание</p>
        <ul v-if="user.role?.title !== 'Администратор'" class="personal">
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
        <section class="section_advices">
          <section class="advices_all">
            <div class="advices_search">
              <input placeholder="Поиск" type="text" class="modal_input" v-model="searchQuery">
              <button class="eco-button" @click="searchAdvice()">Найти</button>
            </div>
            <ul class="advice_filters">
              <li>
                <button @click="filterAdvice('')" class="eco-button filters">Все</button>
              </li>
              <li v-for="category in categories" :key="category.id">
                <button @click="filterAdvice(category.id)" class="eco-button filters">{{ category.title }}</button>
              </li>
            </ul>
            <ul class="advice_list">
              <li class="advice" v-for="advice in advices" :key="advice.id">
                <button @click="addFavorite(advice.url)" class="advice_button" :style="favoriteStyle(advice.url)"></button>
                <img :src="advice.icon" alt="" class="advice_picture">
                <div class="advice_text">
                  <p class="advice_title">{{advice.title}}</p>
                  <p class="advice_category">{{advice.category?.title}}</p>
                  <p class="advice_description">{{advice.description}}</p>
                  <div v-if="user.role?.title === 'Администратор'" class="button_group">
                    <button class="eco-button" @click="showChangeModal(advice.url)">Изменить</button>
                    <AddAdvice v-if="adviceUrl === advice.url" :advice="advice" @close="closeModal()"></AddAdvice>
                    <button class="eco-button" @click="deleteAdvice(advice.url)">Удалить</button>
                  </div>
                </div>
              </li>
            </ul>
          </section>
          <div v-if="user.role?.title !== 'Администратор'" class="advice_add modal">
            <div class="modal_title">
              <p class="title">Поделитесь своим советом</p>
            </div>
            <form class="modal_form" >
              <label class="modal_text" for="title">Совет</label>
              <input class="modal_input" v-model="advice_text">
              <label class="modal_text" for="description">Описание</label>
              <textarea class="modal_input" v-model="description"></textarea>
              <button class="eco-button form-button" @click.prevent="sendAdvice()">Отправить</button>
            </form>
          </div>
        </section>
      </section>
    </main>
  </div>
</template>

<script>
import ProfileMenu from '../components/ProfileMenu.vue'
import {store} from '../store.js'
import { onMounted, computed } from 'vue';
import axiosInstance from '../http.js'
import axios from 'axios'
import AddAdvice from '../components/AddAdvice.vue';

const user = computed(() => store.state.user) 
const advices = computed(() => store.state.advices)
const personal_advices = computed(() => store.state.personal_advices)
const send_advices = computed(() => store.state.send_advices)
const categories = computed(() => store.state.categories)
const favorites = computed(() => store.state.favorites)


export default {
    components: {
      ProfileMenu,
      AddAdvice
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
          .get('/categories')
          .then(res => {
            console.log(res.data)
            store.commit('setCategories', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
        // await axiosInstance
        //   .get('/advices/personal_vector')
        //   .then(res => {
        //     console.log(res.data)
        //     store.commit('setPersonalAdvices', res.data)
        //   })
        //   .catch((err) => {
        //     console.log(err)
        //   })
        await axiosInstance
          .get('/advices?is_posted=False')
          .then(res => {
            console.log(res.data)
            store.commit('setSendAdvices', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
        await axiosInstance
          .get('/favorites')
          .then(res => {
            console.log(res.data)
            store.commit('setFavorites', res.data)
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
        description: '',
        categories: categories,
        searchQuery: '',
        favorites: favorites,
        adviceModal: false,
        adviceUrl: null
      }
    },
    computed:{
     
    },
    methods: {
      showAddModal(){
        this.adviceModal = true
      },
      showChangeModal(advice){
        this.adviceUrl = advice
      },
      closeModal(){
        this.adviceUrl = null,
        this.adviceModal = false
      },
      async addFavorite(adviceUrl){
        let favorite = this.favorites.find(favorite => favorite.advice.url === adviceUrl)
        if (favorite){
          await axiosInstance
            .delete(`/favorites/${favorite.id}/`)
            .then((res) => {
              console.log(res.data)
            })
            .catch((err) => {
              console.log(err)
            })
        }
        else{
          await axiosInstance
            .post('favorites/', {
              user: this.user.url,
              advice: adviceUrl,
              favorite_type: 'A',
              guide: null
            })
            .then((res) => {
              console.log(res.data)
            })
            .catch((err) => {
              console.log(err)
            })
          
        }
        await axiosInstance
          .get('/favorites')
          .then(res => {
            console.log(res.data)
            store.commit('setFavorites', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
        this.favoriteStyle(adviceUrl)
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
      },
      async filterAdvice(category){
        await axiosInstance
          .get('/advices/', {
            params: {
              category:  category!== "0" ? category : null
            }
          })
          .then((res) => {
            console.log(res.data)
            store.commit('setAdvices', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
      },
      searchAdvice(){
        if (this.searchQuery){
          axiosInstance
            .get(`/advices/search/`, {
              params: {
                q: this.searchQuery
              }
            })
            .then((res) => {
              console.log(res.data)
              store.commit('setAdvices', res.data)
            })
            .catch((err) => {
              console.log(err)
            })
        }
      },
      favoriteStyle(adviceUrl){
        if (this.favorites.find(favorite => favorite.advice?.url === adviceUrl)){
          return {
            backgroundImage : "url('favorite_hover.svg')"
          }
        }
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
  font-size: 12px;
  color: gray;
  height: auto;
}
.advice_category{
  font-size: 14px;
  color: #2E8B57;
}
.advice_picture{
  width: 48px;
  height: 48px;
  display: block;
  margin: 0 auto;

}
.advice{
  padding: 16px;
  border: 1px solid lightgray;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.advice_button{
  width: 24px;
  height: 24px ;
  border: none;
  background: transparent;
  background-image: url('heart.svg');
  background-position: center;
  background-size: cover;
  align-self: flex-end;
}
.advice_button:hover{
  background-image: url('favorite_hover.svg');
}
.advice_button:disabled{
  background-image: url('favorite_hover.svg');
}
.advice_list{
  /* max-width: fit-content; */
  display: grid;
  grid-template-columns: 1fr 1fr ;
  gap: 16px;
}
.section_advices{
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}


.personal .advice{
  background-color: #C5FDC5;
}
.personal .advice .advice_description{
  color: black;

}
.personal{
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}
.advice_add{
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  border: 1px solid lightgray;
  border-radius: 8px;
  height: fit-content;

}
.advice_filters{
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.advices_all{
  display: grid;
  gap: 16px;
  grid-column: span 2;
}

.modal_form{
  display: flex;
  flex-direction: column;
  gap: 8px;
  justify-content: center;
}
.modal_input{
  width: 100%;
  font-size: 14px;
  font-family: Raleway, sans-serif;
  border-radius: 4px;
  border: 1px solid lightgray;
  padding: 8px;
  padding: 8px 16px;
}
.modal_input-multi{
  color: black;
  font-size: 14px;
}
.title{
  font-size: 16px;
  font-weight: 500;
  font-family: Golos Text, sans-serif;
}

.modal_text{
  font-size: 12px;
  color: grey;
  font-weight: 500;
}
.filters{
  color: #2E8B57;
  background-color: white;
  border: 1px solid #2E8B57;
  font-weight: 500;
}
.filters:hover, .filters:focus{
  background-color: #C5FDC5;
  color: black;

}
.send_advices{
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.send_list{
  display: grid;
  gap: 16px;
}
.send_advice{
  display: flex;
  gap: 16px;
}
.form-button{
  margin: 0 auto;
}
.advices_search{
  display: flex;
  gap: 16px;
  align-items: center;
}
@media screen and (max-width: 1024px) {
  .section_advices{
    grid-template-columns: repeat(2, 1fr);
  }
  .advice_list{
    grid-template-columns: 1fr;
  }
  .advices_all{
    grid-column: span 1;
  }
  
}

</style>