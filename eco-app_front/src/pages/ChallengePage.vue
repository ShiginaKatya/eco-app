<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu :burgerMenu="openingMenu" @close="closeMenu()"></ProfileMenu>
    </aside>
    <main class="main">
      <div class="main_header">
        <h1 class="header_title">Челленджи</h1>
      </div>
      <button v-if="user.role?.title === 'Администратор'" @click="openModal()" class="eco-button">Добавить челлендж</button>
      <AddChallenge v-if="showAddModal" :user="user" @close="closeModal"></AddChallenge>
      <div class="main_sections">
        <section class="main_challenges">
          <section class="main_week-challenge">
            <p class="challenge_title">Челлендж недели</p>
            <div class="challenges_list">
              <div class="challenges_item" v-if="week_challenge">
                <p class="challenge_title">{{week_challenge[0]?.title}}</p>
                <p class="challenge_category">{{week_challenge[0]?.category?.title}}</p>
                <button @click="showChallenge(week_challenge[0]?.url)" class="eco-button">Подробнее</button>
                <DetailChallenge v-if="challengeUrl === week_challenge[0]?.url" :challenge="week_challenge[0]" :user="user" @close="closeModal"></DetailChallenge>
              </div>
            </div>
          </section>
          <p class="challenge_title">Доступные челленджи</p>
          <ul class="challenges_list">
            <li class="challenges_item" v-for="challenge in challenges" :key="challenge.id">
              <p class="challenge_title">{{challenge.title}}</p>
              <!-- <p v-for="task in challenge.tasks" :key="task.id">{{task.title}}</p> -->
              <p class="challenge_category">{{challenge.category?.title}}</p>
              <div class="button_group">
                <button @click="showChallenge(challenge.url)" class="eco-button">Подробнее</button>
                <button v-if="user.role?.title === 'Администратор'" @click="showChangeModal(challenge.url)" class="eco-button">Изменить</button>
              </div>
              <DetailChallenge v-if="challengeUrl === challenge.url" :challenge="challenge" :user="user" @close="closeModal"></DetailChallenge>
              <AddChallenge v-if="changeUrl === challenge.url" :user="user" :challenge="challenge" @close="closeModal"></AddChallenge>
            </li>
          </ul> 
        </section>
        <section class="main_userchallenges" v-if="userchallenges.length !== 0 && user.role.title !== 'Администратор'">
          <p class="userchallenges_title">Мои челленджи</p>
          <ul class="userchallenges_list">
            <li class="userchallenges_item" v-for="challenge in userchallenges" :key="challenge.id">
              <div class="userchallenge_title-group">
                <p class="userchallenge_title">{{challenge.challenge.title}}</p>
                <p class="userchallenge_category">{{challenge.challenge.category?.title}}</p>
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
import AddChallenge from '../components/AddChallenge.vue';

 
const challenges = computed(() => store.state.challenges)
const userchallenge = computed(() => store.state.userchallenge)
const userchallenges = computed(() => store.state.userchallenges)
const week_challenge = computed(() => store.state.week_challenge)

export default {
    components: {
      ProfileMenu,
      DetailChallenge,
      AddChallenge
    },
    setup() {
      const user = computed(() => store.state.user) 

      const loadUser = async () => {
        await store.dispatch('loadUser')

      }
      onMounted(async () => {
        await loadUser()
        await axiosInstance
          .get('/challenges?this_week=False')
          .then(res => {
            console.log(res.data)
            store.commit('setChallenges', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        await axiosInstance
          .get('/challenges?this_week=True')
          .then(res => {
            console.log(res.data)
            store.commit('setWeekChallenge', res.data)
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
      return{
        user,
      }
    },
    data() {
      return {
        challenges: challenges,
        userchallenge: userchallenge,
        tasks: [],
        userchallenges: userchallenges,
        chooseStatus: '',
        challengeUrl: null,
        isChecked: false,
        progressValue: 0,
        showModal: false,
        showAddModal: false,
        week_challenge: week_challenge,
        changeUrl: null,
    
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
      openModal(){
        this.showAddModal = true
      },
      showChangeModal(challenge){
        this.changeUrl = challenge
      },
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
          this.showAddModal = false
          this.changeUrl = null
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
  margin-top: 16px;
  display: grid;
  grid-template-columns: 2fr 1fr;
  flex: 1;
  gap: 16px;
}

.button_group{
  display: flex;
  gap: 8px;
  justify-content: flex-start;
}
.challenges_list{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.challenges_item{
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
.main_week-challenge{
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.main_week-challenge .challenges_item{
  background-color: #F5F5DC;
}
.main_week-challenge .eco-button{
  background-color: white;
  border: 1px solid lightgray
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
.main_challenges{
  display: flex;
  flex-direction: column;
  gap: 16px;
}
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
@media screen and (max-width: 1200px) and (min-width: 900px){
  .main_sections{
    grid-template-columns: repeat(2, 1fr);
  }
  /* .main_userchallenges{
    grid-column: span 2;
  } */
  .challenges_list{
    grid-template-columns: repeat(1, 1fr);
  }
}
@media screen and (max-width: 900px) and (min-width: 768px) {
  .main_sections{
    grid-template-columns: repeat(3, 1fr);
  }
  .main_userchallenges{
    grid-column: span 2;
  }
  .challenges_list{
    grid-template-columns: repeat(1, 1fr);
  }
}
@media screen and (max-width: 767px) {
  .main_sections{
    grid-template-columns: repeat(1, 1fr);
    grid-template-rows: 1fr 1fr;
  }
  .main_userchallenges{
    grid-column: span 2;
    grid-row: 1;
  }
  .challenges_list{
    grid-template-columns: repeat(1, 1fr);
    grid-row: 2
  }
}

</style>