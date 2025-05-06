<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu></ProfileMenu>
    </aside>
    <main class="main">
      <div class="main_header">
        <h1 class="header_title">Челленджи</h1>
      </div>
      <div class="main_sections">
        <section class="main_challenges">
          <!-- <p class="challenges_title">Доступные челленджи</p> -->
          <ul class="challenges_list">
            <li class="challenges_item" v-for="challenge in challenges" :key="challenge.id">
              <p class="challenge_title">{{challenge.title}}</p>
              <!-- <p v-for="task in challenge.tasks" :key="task.id">{{task.title}}</p> -->
              <p class="challenge_category">{{challenge.category.title}}</p>
              <button @click="showChallenge(challenge.url)" class="eco-button">Подробнее</button>
              <DetailChallenge v-if="challengeUrl === challenge.url" :challenge="challenge" :user="user" @close="closeModal"></DetailChallenge>
            </li>
          </ul> 
        </section>
        <section class="main_userchallenges" v-if="userchallenges.length !== 0">
          <p class="userchallenges_title">Мои челленджи</p>
          <ul class="userchallenges_list">
            <li class="userchallenges_item" v-for="challenge in userchallenges" :key="challenge.id">
              <div class="userchallenge_title-group">
                <p class="userchallenge_title">{{challenge.challenge.title}}</p>
                <p class="userchallenge_category">{{challenge.challenge.category.title}}</p>
              </div>
              <p class="userchallenge_text">текущее задание</p>
              <div class="userchallenge_task">
                <label class="active_task" v-if="activeTask(challenge)">{{activeTask(challenge).task.title}}</label>
                <input v-model="isChecked" type="checkbox" @change="completeTask(activeTask(challenge).id)"/>
              </div>
              <!-- <button class="eco-button" @click="completeTask(activeTask(challenge).id)">Отметить выполнение</button> -->
              <div class="userchallenge_progress">
                <p class="progress_count">выполнено: {{ challengeProcent(challenge.tasks) }}</p>
                <progress class="progress_bar" :max="100" :value="progressValue"></progress>
              </div>
              <p class="userchallenge_text">{{ challenge.challenge.description }}</p>
            </li>
          </ul>
        </section> 
      </div>
    </main>
  </div>
</template>

<script>
import ProfileMenu from '../components/ProfileMenu.vue'
import DetailChallenge from '../components/DetailChallenge.vue';
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
      DetailChallenge
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
        chooseStatus: '',
        challengeUrl: null,
        isChecked: false,
        progressValue: 0,
        showModal: false

    
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
        this.isChecked=false
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
        let tasksTrue = 0
        tasks.map(task =>{
          if (task.status){
            tasksTrue = tasksTrue + 1
          } 
        })
        this.progressValue = ((tasksTrue/tasks.length)*100).toFixed()
        return `${tasksTrue}/${tasks.length}`
        
      },
      showChallenge(challenge){
        this.challengeUrl = challenge
      },
      closeModal() {
          this.challengeUrl = null
          axiosInstance
          .get('/userchallenges')
          .then(res => {
            console.log(res.data)
            store.commit('setUserChallenges', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        },  
    }
}
</script>

<style scoped>
.main_sections{
  display: grid;
  grid-template-columns: 2fr 1fr;
  flex: 1;
  gap: 16px;
}

.challenges_list{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.challenges_item{
  max-width: 350px;
  max-height: 200px;
  padding: 16px;
  border-radius: 8px;
  background-color: white;
  border: 1px solid lightgray;
}
.challenge_title{
  font-size: 16px;
  font-family: Golos Text, sans-serif;
  color: black;
  font-weight: 500;
}
.challenge_category{
  font-size: 14px;
  color: gray;
  margin-bottom: 16px;
}
.main_userchallenges{
  border: 1px solid lightgray;
  background-color: white;
  border-radius: 8px;
  padding: 16px;
}
.userchallenges_title{
  font-family: Raleway, sans-serif;
  font-size: 14px;
  font-weight: 500;
  color: gray;
  margin-bottom: 16px ;
}
.userchallenges_list{
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
  justify-content: center;
}
.userchallenges_item{
  border-radius: 8px;
  background-color: white;
  border: 1px solid lightgray;
}
.userchallenge_title{
  /* padding: 16px; */
  font-size: 16px;
  font-weight: 500;
  font-family: Golos Text, sans-serif;
  /* border-bottom: 1px solid lightgray; */
}
.userchallenge_title-group{
  border-bottom: 1px solid lightgray;
  padding: 16px;
}
.userchallenge_category{
  font-size: 14px;
  color: #2E8B57;
  text-transform: lowercase;
  text-align: right;
}
.userchallenge_text{
  padding: 8px 16px 2px;
  font-size: 14px;
  color: gray;
}
.userchallenge_task{
  margin: 8px;
  padding: 8px;
  font-size: 14px;
  border-radius: 8px;
  background-color: #C5FDC5;
  display: grid;
  grid-template-columns: auto 20px;
  align-items: center;
  gap: 8px;
  justify-content: center;
}
input[type="checkbox"] {
  border: 1px solid lightgray;
  border-radius: 50%;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 15px; 
  height: 15px;
  display: inline-block;
  background: white;
}
input[type="checkbox"]:checked {
  background-image: url("/check.svg");
  background-position: center;
}
/* .userchallenges_item .eco-button{
  margin: 10px auto;
} */
.progress_bar{
  accent-color: #2E8B57;
  margin: 0 auto;
  width: auto;
  display: block;
}
.userchallenge_progress{
  padding: 8px 16px;

}
.progress_count{
  text-align: right;
  font-size: 14px;
}

</style>