<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu></ProfileMenu>
    </aside>
    <main class="main">
      <section class="main_header">
        <img src="/profile_image.svg" alt="avatar" class="profile_image">
        <ul class="header_info">
          <li class="info_item">{{ user.username }}</li>
          <li class="info_item-l">{{ userStats[0]?.level.title }}</li>
        </ul>
        <button class="eco-button">Пройти анкетирование</button>
      </section>
      <section class="main_actions">
        <div class="actions_plan">
          <p class="latest_type">план</p>
          <p class="latest_title">{{ plans[0]?.goal }}</p>
          <p class="latest_progress">Прогресс: {{ challengeProcent(plans[0]?.habits) }} %</p>
        </div>
        <ul class="actions_challenges">
          <li v-for="challenge in userchallenges" :key="challenge.id" class="challenges_latest">
            <p class="latest_type">челлендж</p>
            <p class="latest_title">{{ challenge.challenge.title }}</p>
            <p class="latest_progress">Прогресс: {{ challengeProcent(challenge.tasks) }} %</p>
          </li>
        </ul>
      </section>
      <section class="main_favorites">
        <p>Последние изменения в Избранном</p>
        <ul class="favorites_list">
          <li v-for="favorite in favorites" :key="favorite.id" class="list_latest">
            <p class="latest_title">{{ favorite.advice.title }}</p>
            <p class="latest_type">{{ favorite.advice.description }}</p>
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

const user = computed(() => store.state.user) 
const userchallenges = computed(() => store.state.userchallenges)
const plans = computed(() => store.state.plans)
const userStats = computed(() => store.state.userstat)
const favorites = computed(() => store.state.favorites)


export default {
    components: {
      ProfileMenu,
    },
    setup() {
      onMounted(async () => {
        await axiosInstance
          .get('/userplans/latest')
          .then(res => {
            console.log(res.data)
            store.commit('setPlans', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        await axiosInstance
          .get('/userchallenges/latest')
          .then(res => {
            console.log(res.data)
            store.commit('setUserChallenges', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        await axiosInstance
          .get('/userstats/')
          .then(res => {
            console.log(res.data)
            store.commit('setUserStat', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        await axiosInstance
          .get('/favorites/latest')
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
        userchallenges: userchallenges,
        plans: plans,
        userStats: userStats,
        favorites: favorites,
    
      }
    },
    computed:{
      
    },
    methods: {
      challengeProcent(tasks){
        if (tasks){
          let t = 0
          let f = 0
          tasks.map(task =>{
            if (task.status){
              t = t + 1
            }
            f = f + 1
          })
          return (t/f*100).toFixed()
        }
        else{
          return null
        }
      }
       
    }
}
</script>

<style scoped>
/* .page{
  display: flex;
}
.sidebar{
  width: fit-content;
}
.main{
  min-width: 320px;
  width: calc(100vw - 300px);
} */
.main_header{
  display: flex;
  gap: 20px;
  margin: 10px 0;
  padding: 20px;
  align-items: center;
  justify-items: center;
}
.profile_image{
  width: 80px;
  border: 1px solid gray;
  padding: 50px;
  border-radius: 50%;
  background-color: grey;
}
.main_actions{
  display: flex;
  gap: 20px;
  max-width: 1000px;
  padding: 10px;
}
.actions_challenges{
  display: flex;
  flex-direction: column;
  gap: 20px;

}
.actions_plan{
  min-width: 300px;
  max-width: 500px;
  border: 1px solid gray;
  border-radius: 8px;
  height: 300px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.challenges_latest{
  min-width: 300px;
  max-width: 500px;
  border: 1px solid gray;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  gap: 10px;
  flex-direction: column;
  justify-content: space-between;

}
.latest_title{
  font-weight: 500;
  width: 200px;
  font-size: 16px;
  font-family: 'Golos Text', sans-serif;
}
.latest_type{
  font-size: 14px;
  color: grey;
}
.main_favorites{
  padding: 20px;
}
.favorites_list{
  display: flex;
  gap: 20px;
  margin: 10px 0;
}
.list_latest{
  width: 300px;
  padding: 10px;
  border: 1px solid gray;
  border-radius: 8px;

}
.info_item{
  font-size: 16px;
  font-weight: 500;
  font-family: Golos Text, sans-serif;
}
.info_item-l{
  font-size: 14px;
  color: gray
}

</style>