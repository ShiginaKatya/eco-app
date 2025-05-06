<template>
  <div class="page">
    <aside class="sidebar">
        <ProfileMenu></ProfileMenu>
    </aside>
    <main class="main">
      <section class="main_header">
        <h1 class="header_title">Прогресс</h1>
      </section>
      <section class="main_sections">
        <section class="main_userinfo">
          <div class="userinfo_next-level">
            <apexchart class="next-level_chart" width="200" type="radialBar" height="200" :options="chartOptions" :series="series"></apexchart>
            <div class="next-level_text">
              <p class="next-level_points"><span>{{ userStats[0]?.points}}</span> /{{ userStats[0]?.next_level.min_points }}</p>
              <p class="next-level_description">до следующего уровня осталось совсем чуть-чуть</p>
            </div>
          </div>
          <div class="stat" v-for="userStat in userStats" :key="userStat.id">
            <div class="stat_block">
              <p class="stat_info_text">Текущий уровень</p>
              <p class="stat_info">{{userStat.level.title}}</p>
            </div>
            <p class="stat_block stat_info_text"><span class="stat_info">{{userStat.achievements_count}}</span> количество наград</p>
          </div>
        </section>
        <section class="main_achievements">
          <p class="achievements_title">Cписок наград</p>
          <ul class="achievements_list">
            <li class="list_achievement"  v-for="user_achievement in userStats[0]?.all_achievements" :key="user_achievement.id">
              <img class="achievement_icon" :src="user_achievement.achievement.icon" alt="">
              <p class="achievement_title">{{ user_achievement.achievement.title }}</p>
              <p class="achievement_count">{{ user_achievement.count }}</p>
            </li>
          </ul>
        </section>
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
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;

  justify-content: flex-start;
  gap: 16px;
  align-items: stretch;
}
.userinfo_next-level{
  display: flex;
  gap: 4px;
  border: 1px solid lightgray;
  padding: 8px;
  border-radius: 8px;
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
  gap: 4px;
  border: 1px solid lightgray;
  padding: 16px;
  border-radius: 8px;
}
.stat_block p span{
  font-weight: bolder; 
}
.achievements_title{
  font-size: 16px;
  font-family: Golos Text, sans-serif;
  font-weight: 500;
}
.achievements_list{
  display: flex;
  gap: 16px;
  justify-content: flex-start;
  flex-wrap: wrap;
  align-items: center;
  padding: 16px 0;
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
  border: 1px solid lightgray;
  border-radius: 8px;
  padding: 16px;
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
  display: grid;
  flex-direction: column;
  gap: 16px;
  height: 100%;
}
.achievement_count{
  background-color: #C5FDC5;
  position: absolute;
  width: 30px;
  height: 30px;
  margin-left: 70px;
  margin-bottom: 30px;
  padding: 2px;
  text-align: center;
  font-weight: 500;
  border-radius: 50%;
}
</style>