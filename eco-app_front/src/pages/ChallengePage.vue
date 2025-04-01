<template>
    <div class="page">
        <aside class="sidebar">
            <ProfileMenu></ProfileMenu>
        </aside>
        <main class="main">
          <p>{{user.username}}</p>
          <ul>
                <li v-for="challenge in challenges" :key="challenge.id">
                    <p class="challenge_title">{{challenge.title}}</p>
                    <p v-for="task in challenge.tasks" :key="task.id">{{task.title}}</p>
                    <button class="eco-button" @click="addChallenge" >Участвовать</button>
                </li>
          </ul> 
          <div>
              <p>Ваши челленджи</p>
              <ul>
                <li v-for="challenge in userchallenges" :key="challenge.id">
                    <p class="challenge_title">{{challenge.challenge.title}}</p>
                    <p >{{activeTask.task.title}}</p>
                    <button class="eco-button" @click="completeTask">Отметить выполнения</button>
                </li>
              </ul>
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
        userchallenges: userchallenges
      }
    },
    computed:{
      activeTask(){
        const challenge  = this.userchallenges.find(userchallenge => userchallenge.id === this.challenge)
        if (challenge){
          return challenge.tasks.find(task => !task.status) 
        }
        return null
      }
    },
    methods: {
      async addChallenge(){
        this.tasks = this.challenges.find(challenge => challenge.id === this.challenge).tasks
        console.log(this.tasks)
        await axiosInstance
          .post('/userchallenges/', {
            challenge: this.challenges.find(challenge => challenge.id === this.challenge).url,
            user: this.user.url,
            status: 'False'
          })
          .then(res => {
            console.log(res.data)
            store.commit('setUserChallenge', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
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
      },
      async completeTask(){
        await axiosInstance
          .patch(`usertasks/${this.activeTask.id}/`, {
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
  margin: 10px;
  max-width: 100vw;
}
</style>