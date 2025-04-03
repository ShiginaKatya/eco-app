<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu></ProfileMenu>
    </aside>
    <main class="main">
      <div class="main_header">
        <h1 class="header_title">ЧЕЛЛЕНДЖИ</h1>
      </div>
      <div class="main_sections">
        <section class="main_challenges">
          <p class="challenges_title">Доступные челленджи</p>
          <ul class="challenges_list">
            <li class="challenges_item" v-for="challenge in challenges" :key="challenge.id">
              <p class="challenge_title">{{challenge.title}}</p>
              <!-- <p v-for="task in challenge.tasks" :key="task.id">{{task.title}}</p> -->
              <p>{{challenge.category.title}}</p>
              <button  class="eco-button" @click="addChallenge(challenge.url)" >{{challengeStatus(challenge)}}</button>
              <button class="eco-button">Подробнее</button>
            </li>
          </ul> 
        </section>
        <section class="main_userchallenges">
          <ul class="userchallenges_list">
            <li class="userchallenges_item" v-for="challenge in userchallenges" :key="challenge.id">
              <p class="userchallenge_title">{{challenge.challenge.title}}</p>
              <p class="active_task" v-if="activeTask(challenge)">{{activeTask(challenge).task.title}}</p>
              <button class="eco-button" @click="completeTask(activeTask(challenge).id)">Отметить выполнения</button>
              <p>Процент выполнения: {{challengeProcent(challenge.tasks)}} %</p>
            </li>
          </ul>
        </section> 
      </div>
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
const challenges = computed(() => store.state.challenges)
const userchallenge = computed(() => store.state.userchallenge)
const userchallenges = computed(() => store.state.userchallenges)

export default {
    components: {
      ProfileMenu,
    },
    setup() {
      onMounted(async () => {
        await axiosInstance
          .get('/challenges')
          .then(res => {
            console.log(res.data)
            store.commit('setChallenges', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        await axiosInstance
          .get('/userchallenges')
          .then(res => {
            console.log(res.data)
            store.commit('setUserChallenges', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        
      })
    },
    data() {
      return {
        user: user,
        challenges: challenges,
        userchallenge: userchallenge,
        tasks: [],
        userchallenges: userchallenges,
        chooseStatus: ''
    
      }
    },
    computed:{
      // activeTask(challenge){
      //   if (challenge){
      //     console.log(challenge)
      //     return challenge.tasks.find(task => !task.status)
      //   }
      //   else {
      //     console.log(2)
      //     return null
      //   }
      // }
      
    },
    methods: {
      async addChallenge(challengeUrl){
        console.log(challengeUrl)
        this.tasks = this.challenges.find(challenge => challenge.url === challengeUrl).tasks
        console.log(this.tasks)
        await axiosInstance
          .post('/userchallenges/', {
            challenge: this.challenges.find(challenge => challenge.url === challengeUrl).url,
            user: this.user.url,
            status: 'False'
          })
          .then(res => {
            console.log(res.data)
            store.commit('setUserChallenge', res.data)
          })
          .catch((err) => {
            console.log(err)
            this.tasks=[]
          }) 
        if (this.tasks != []){
          await Promise.all(
            this.tasks.map(task =>
              axiosInstance
                .post('/usertasks/', {
                  task: task.url,
                  challenge: store.state.userchallenge.url,
                  status: 'False'
                })
                .then(res => {
                  console.log(res.data)
                })
                .catch((err) => {
                  console.log(err)
                }) 
            )
          )
        }
        await axiosInstance
          .get('/userchallenges')
          .then(res => {
            console.log(res.data)
            store.commit('setUserChallenges', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
      },
      async completeTask(Id){
        console.log(Id)
        await axiosInstance
          .patch(`usertasks/${Id}/`, {
            status: 'True'
          })
          .then(res => {
            console.log(res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        await axiosInstance
          .get('/userchallenges')
          .then(res => {
            console.log(res.data)
            store.commit('setUserChallenges', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
      }, 
      activeTask(challenge){
        if (challenge){
          console.log(challenge)
          return challenge.tasks.find(task => !task.status)
        }
        else {
          console.log(2)
          return null
        }
      },
      challengeStatus(challenge){
        if (this.userchallenges.find(userchallenge => userchallenge.challenge.url == challenge.url)){
          return 'уже участвуете'

        }
        else{
          return 'участвовать'
        }
      },
      challengeProcent(tasks){
        let t = 0
        let f = 0
        tasks.map(task =>{
          if (task.status){
            t = t + 1
            console.log(1)
          }
          f = f + 1
          
        })
        return (t/f*100).toFixed()
      }
      
       
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
  width: calc(100vw - 300px);
}
.main_header{
  border-bottom: 1px solid grey;
  padding: 20px;
}
.header_title{
  font-family: Golos Text, sans-serif;
  font-weight: 500;
  font-size: 32px;
  text-align: center;
}
.main_sections{
  display: grid;
  grid-template-columns: 3fr 1fr;
}
.main_challenges{
  margin: 10px;
}
.challenges_list{
  display: grid;
  grid-template-columns: repeat(auto-fit, 200px);
  gap: 10px;
}
.challenges_item{
  max-width: 200px;
  max-height: 200px;
  padding: 20px;
  border-radius: 25px;
  border: 1px solid grey;
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: flex-start;
}
</style>