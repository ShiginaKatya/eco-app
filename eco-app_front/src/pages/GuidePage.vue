<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu :burgerMenu="openingMenu" @close="closeMenu()"></ProfileMenu>
    </aside>
    <main class="main">
      <section class="main_header"> 
        <h1 class="header_title">Руководства</h1>
      </section>
      <section class="main_sections">
        <div v-if="user.role?.title === 'Администратор'">
          <ul>
            <li v-for="guide in send_guides" :key="guide?.id">
              <p class="advice_title">{{advice.title}}</p>
              <p class="advice_title">{{advice.author.username}}</p>
              <p class="advice_description">{{advice.description}}</p>
              <button @click="postAdvice(advice.id)" class="eco-button">Опубликовать</button>
            </li>
          </ul>
        </div>
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
              <li class="guide" v-for="guide in guides" :key="guide.id">
                <img :src="guide.icon" alt="" class="advice_picture">
                <div class="advice_text">
                  <div class="guide_title">
                    <p>{{guide.title}}</p>
                    <button @click="addFavorite(guide.url)" class="guide_button" :style="favoriteStyle(guide.url)"></button>
                  </div>
                  <p class="advice_category">{{guide.category?.title}}</p>
                  <p class="advice_description">{{guide.annotation}}</p>
                  <button @click="showGuide(guide.url)" class="eco-button guide-button">Подробнее</button>
                  <DetailGuide v-if="guideUrl === guide.url" :guide="guide" @close="closeModal"></DetailGuide>
                </div>
              </li>
            </ul>
          </section>
          <div class="advice_add modal">
            <div class="modal_title">
              <p class="title">Поделитесь руководством на основе Ваших наблюдений</p>
            </div>
            <form class="modal_form" >
              <label class="modal_text" for="guide_title">Заголовок руководства</label>
              <input class="modal_input" v-model="guide_title">
              <label class="modal_text" for="guide_annotation">Важное</label>
              <textarea class="modal_input" v-model="guide_annotation"></textarea>
              <label class="modal_text" for="guide_text">Текст</label>
              <textarea class="modal_input" v-model="guide_text"></textarea>
              <button class="eco-button form-button" @click.prevent="sendGuide()">Отправить</button>
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
import DetailGuide from '../components/DetailGuide.vue';

const user = computed(() => store.state.user) 
const guides = computed(() => store.state.guides)
const send_guides = computed(() => store.state.send_guides)
const categories = computed(() => store.state.categories)
const favorites = computed(() => store.state.favorites)


export default {
    components: {
      ProfileMenu,
      DetailGuide
    },
    setup() {
      onMounted(async () => {
        await axiosInstance
          .get('/guides?is_posted=True')
          .then(res => {
            console.log(res.data)
            store.commit('setGuides', res.data)
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
        await axiosInstance
          .get('/guides?is_posted=False')
          .then(res => {
            console.log(res.data)
            store.commit('setSendGuides', res.data)
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
        guides: guides,
        send_guides: send_guides,
        guide_text: '',
        guide_annotation: '',
        guide_title: '',
        categories: categories,
        searchQuery: '',
        favorites: favorites,
        guideUrl: null,
      }
    },
    computed:{
     
    },
    methods: {
      async addFavorite(guideUrl){
        let favorite = this.favorites.find(favorite => favorite.guide?.url === guideUrl)
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
              guide: guideUrl,
              favorite_type: 'G',
              advice: null
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
        this.favoriteStyle(guideUrl)
      },
      async sendGuide(){
        await axiosInstance
          .post('guides/', {
            author: this.user.url,
            title: this.guide_title,
            annotation: this.guide_annotation,
            description: this.guide_description,
            is_posted: false
          })
      },
      async postGuide(guideId){
        await axiosInstance
          .patch(`guides/${guideId}/`, {
            is_posted: true
          })
      },
      async filterGuide(category){
        await axiosInstance
          .get('/guides/', {
            params: {
              category:  category!== "0" ? category : null
            }
          })
          .then((res) => {
            console.log(res.data)
            store.commit('setGuides', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
      },
      searchGuide(){
        if (this.searchQuery){
          axiosInstance
            .get(`/guides/search/`, {
              params: {
                q: this.searchQuery
              }
            })
            .then((res) => {
              console.log(res.data)
              store.commit('setGuides', res.data)
            })
            .catch((err) => {
              console.log(err)
            })
        }
      },
      favoriteStyle(guideUrl){
        if (this.favorites.find(favorite => favorite.guide?.url === guideUrl)){
          return {
            backgroundImage : "url('favorite_hover.svg')"
          }
        }
      },
      showGuide(guide){
        this.guideUrl = guide
      },
      closeModal() {
          this.guideUrl = null
      }
    }
}
</script>

<style scoped>
.guide_title{
  font-weight: 500;
  font-family: Golos Text, sans-serif;
  font-size: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}
.advice_description{
  font-size: 12px;
  color: black;
  height: auto;
  font-weight: 500;
}
.advice_category{
  font-size: 14px;
  color: #2E8B57;
}
.advice_picture{
  display: block;
  margin: 0 auto;
  width: 100%;
  border-radius: 4px;

}
.guide{
  padding: 16px;
  border: 1px solid lightgray;
  border-radius: 8px;
  gap: 16px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
}
@media screen and (max-width: 1200px) {
  .guide{
    grid-template-columns: 1fr;
  }
}
.guide_button{
  width: 24px;
  height: 24px ;
  border: none;
  background: transparent;
  background-image: url('heart.svg');
  background-position: center;
  background-size: cover;
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
  grid-template-columns: 1fr ;
  gap: 16px;
}
.section_advices{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.advice{
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: start;
  

}
.advice_text{
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;

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
  height: fit-content;
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
.guide-button{
  align-self: flex-end;
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
.form-button{
  margin: 0 auto;
}
.advices_search{
  display: flex;
  gap: 16px;
  align-items: center;
}

</style>