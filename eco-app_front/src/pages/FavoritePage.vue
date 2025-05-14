<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu :burgerMenu="openingMenu" @close="closeMenu()"></ProfileMenu>
    </aside>
    <main class="main">
      <section class="main_header"> 
        <h1 class="header_title">Избранное</h1>
      </section>
      <section class="main_sections">
        <p class="advice_title">Советы</p>
        <ul class="advice_list">
          <li class="advice" v-for="advice in advices" :key="advice.id">
            <button @click="addFavorite(advice.advice.url)" class="advice_button"></button>
            <img :src="advice.advice.icon" alt="" class="advice_picture">
            <div class="advice_text">
              <p class="advice_title">{{advice.advice.title}}</p>
              <p class="advice_category">{{advice.advice.category?.title}}</p>
              <p class="advice_description">{{advice.advice.description}}</p>
            </div>
          </li>
        </ul>
        <p class="advice_title">Руководства</p>
        <ul class="guide_list">
          <li class="guide" v-for="guide in guides" :key="guide.id">
            <!-- <button @click="addFavorite(guide.url)" class="advice_button" :style="favoriteStyle(guide.url)"></button> -->
            <img :src="guide.guide.icon" alt="" class="guide_picture">
            <div class="advice_text">
              <p class="advice_title">{{guide.guide.title}}</p>
              <p class="advice_category">{{guide.guide.category?.title}}</p>
              <p class="guide_description">{{guide.guide.annotation}}</p>
              <button @click="showGuide(guide.guide.url)" class="eco-button guide-button">Подробнее</button>
              <DetailGuide v-if="guideUrl === guide.guide.url" :guide="guide.guide" @close="closeModal"></DetailGuide>
            </div>
          </li>
        </ul>
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
// const guides = computed(() => store.state.guides)
// const advices = computed(() => store.state.advices)
const favorites = computed(() => store.state.favorites)


export default {
    components: {
      ProfileMenu,
      DetailGuide
    },
    setup() {
      onMounted(async () => {
        await axiosInstance
          .get('/favorites/advices')
          .then(res => {
            console.log(res.data)
            store.commit('setAdvices', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
        await axiosInstance
          .get('/favorites/guides')
          .then(res => {
            console.log(res.data)
            store.commit('setGuides', res.data)
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
        favorites: favorites,
        advices: advices,
        guideUrl: null,
      }
    },
    computed:{
     
    },
    methods: {
      async addFavorite(guideUrl){
        let favorite = this.favorites.find(favorite => favorite.guide.url === guideUrl)
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
  background-image: url('favorite_hover.svg');
  background-position: center;
  background-size: cover;
  align-self: flex-end;
}
.advice_button:hover{
  background-image: url('heart.svg');
}
.advice_button:disabled{
  background-image: url('favorite_hover.svg');
}
.advice_list{
  /* max-width: fit-content; */
  display: grid;
  grid-template-columns: 1fr 1fr 1fr ;
  gap: 16px;
}
.guide_list{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.guide_picture{
  display: block;
  margin: 0 auto;
  width: 100%;
  border-radius: 4px;

}
.guide_description{
  font-size: 12px;
  color: black;
  height: auto;
  font-weight: 500;
}

.guide{
  border: 1px solid lightgray;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: start;
  gap: 16px;
  border-radius: 8px;
  padding: 16px;
}
.advice_text{
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;

}
.guide-button{
  align-self: flex-end;
}
</style>