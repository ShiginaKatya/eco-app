<template>
  <div class="page">
    <aside class="sidebar">
        <ProfileMenu></ProfileMenu>
    </aside>
    <main class="main">
      <div class="main_header">
        <h1 class="header_title">Прогресс</h1>
      </div>
      <section class="main_userinfo">
        <div class="userinfo_next-level">
          <apexchart class="next-level_chart" width="200" type="radialBar" height="200" :options="chartOptions" :series="series"></apexchart>
          <div class="next-level_text">
            <p class="next-level_points"><span>{{ userStats[0]?.points}}</span> /{{ userStats[0]?.next_level.min_points }}</p>
            <p class="next-level_description">до следующего уровня осталось совсем чуть-чуть</p>
          </div>
        </div>
        <ul class="userinfo_stat">
          <li class="stat" v-for="userStat in userStats" :key="userStat.id">
            <div class="stat_block">
              <p class="stat_info_text">Текущий уровень</p>
              <p class="stat_info">{{userStat.level.title}}</p>
            </div>
            <p class="stat_block stat_info_text"><span class="stat_info">{{userStat.all_achievements.length}}</span> количество наград</p>
          </li>
      </ul>
      </section>
      <section class="main_achievements">
        <p class="achievements_title">Cписок наград</p>
        <ul class="achievements_list">
          <li class="list_achievement"  v-for="user_achievement in userStats[0]?.all_achievements" :key="user_achievement.id">
            <img class="achievement_icon" :src="user_achievement.achievement.icon" alt="">
            <p class="achievement_title">{{ user_achievement.achievement.title }}</p>
          </li>
        </ul>
      </section> 
    </main>
  </div>
</template>
<script>
import ProfileMenu from '../components/ProfileMenu.vue'
import {store} from '../store.js'
import { onMounted, computed, ref } from 'vue';
import axiosInstance from '../http.js'
import axios from 'axios'

const user = computed(() => store.state.user) 
const userStats = computed(() => store.state.userstat)

export default {
    components: {
      ProfileMenu,
    },
    setup() {
      const series = ref([])
      const labels = ref([])
      onMounted(async () => {

        // if (Object.keys(user.value).length === 0) {
        //   console.log(window.localStorage.getItem('userId'))
        //   await axiosInstance
        //     .get(`users/${window.localStorage.getItem('userId')}/`)
        //     .then((res) => {
        //       console.log(res.data)
        //       store.commit('setUser', res.data)
        //     })
        //     .catch((err) => {
        //       console.log(err)
        
        //     })   
        // }
        await axiosInstance
          .get('/userstats/')
          .then(res => {
            console.log(res.data[0])
            series.value = [((res.data[0].points/res.data[0].next_level.min_points)*100).toFixed()]
            store.commit('setUserStat', res.data)
           
          })
          .catch((err) => {
            console.log(err)
          }) 
      })
      return {
        series,
      }
    },
    data() {
      return {
        user: user,
        userStats: userStats,
        next_level: '',
        chartOptions: {
            width: '100px',
            colors: ['#C5FDC5'],
            labels: ['Пройдено'],
            stroke: {
              lineCap: "round",},
            plotOptions: {
            radialBar: {
              hollow: {
                margin: 2,
                size: "65%"
              },
            
              dataLabels: {
                name: {
                fontSize: '14px',
                fontFamily: 'Raleway, sans-serif',
                color: 'gray',
                style: {
                  whiteSpace: 'pre-line', 
                },
              },
                value: {
                  fontSize: '18px', 
                  fontFamily: 'Golos Text, sans-serif',
                  color: 'black',
                  fontWeight: '500'
                },
              }
            }
          },
          },
          
          
        
        
      }
    },
    methods: {

    }
}
</script>

<style scoped>
.apexcharts-xaxis-label, 
.apexcharts-yaxis-label, 
.apexcharts-title {
    font-family: 'Raleway', sans-serif !important; /* Используйте ваш шрифт */
}
.main_userinfo{
  display: flex;
  justify-content: flex-start;
  gap: 20px;
  align-items: center;
  padding: 10px;
}
.userinfo_next-level{
  display: flex;
  gap: 2px;
  border: 1px solid lightgray;
  padding: 8px;
  border-radius: 8px;
  width: 350px;
  align-items: center;
}
.next-level_text{
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.next-level_points{
  font-size: 16px;
  font-weight: 500;
  color: gray;
  font-family: Golos Text, sans-serif;
}
.next-level_points span{
  color: black;
  font-size: 24px;
}
.next-level_description{
  color: gray;
  font-size: 14px;
}
.stat_block{
  display: flex;
  flex-direction: column;
  gap: 6px;
  border: 1px solid lightgray;
  padding: 16px;
  border-radius: 8px;
}
.stat_block p span{
  font-weight: bolder; 
}
.main_achievements{
  margin: 10px;
  border: 1px solid lightgray;
  border-radius: 8px;
}
.achievements_title{
  font-size: 16px;
  font-family: Golos Text, sans-serif;
  font-weight: 500;
  margin: 10px;
}
.achievements_list{
  display: flex;
  gap: 10px;
  justify-content: flex-start;
  flex-wrap: wrap;
  align-items: center;
  padding: 10px;
}
.achievement_title{
  font-size: 14px;
  text-align: center;
  margin: auto;
  max-width: 90px;
}
.achievement_icon{
  display: block;
  margin: auto;
  width: 40px;
}
.list_achievement{
  border: 1px solid gray;
  border-radius: 10px;
  padding: 10px;
}
.stat_info_text{
  font-size: 14px;
  color: gray;

}
.stat_info{
  font-size: 16px;
  font-family: Golos Text, sans-serif;
  font-weight: 500;
  color: black;
}
.stat{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 10px;
}
</style>