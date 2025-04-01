<template>
    <div class="page">
        <aside class="sidebar">
            <ProfileMenu></ProfileMenu>
        </aside>
        <main class="main">
            <ul>
              <li v-for="userStat in userStats" :key="userStat.id">
                  <p>{{userStat.user.username}}</p>
                  <p>{{userStat.points}}</p>
                  <p>{{userStat.completed_plans}}</p>
                  <p></p>
                  <ul>
                    <li v-for="user_achievement in userStat.all_achievements" :key="user_achievement.id">
                      {{user_achievement.achievement.title}}
                    </li>
                  </ul>
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
const userStats = computed(() => store.state.userstat)

export default {
    components: {
      ProfileMenu,
    },
    setup() {
      onMounted(async () => {
        if (Object.keys(user.value).length === 0) {
          console.log(window.localStorage.getItem('userId'))
          await axiosInstance
            .get(`users/${window.localStorage.getItem('userId')}/`)
            .then((res) => {
              console.log(res.data)
              store.commit('setUser', res.data)
            })
            .catch((err) => {
              console.log(err)
        
            })   
        }
        await axiosInstance
          .get('/userstats/')
          .then(res => {
            console.log(res.data)

            store.commit('setUserStat', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
      })
    },
    data() {
      return {
        user: user,
        userStats: userStats,
      }
    },
    computed:{
      
    },
    methods: {
      
    }
}
</script>

<style scoped>
.page{
  display: flex;
}
.sidebar{
  width: fit-content;
}
.main{
  min-width: 320px;
  margin: 10px;
  max-width: 100vw;
}
</style>