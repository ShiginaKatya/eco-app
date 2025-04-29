<template>
  <div class="page">
    <aside class="sidebar">
        <ProfileMenu></ProfileMenu>
    </aside>
    <main class="main">
      <div class="main_header">
        <h1 class="header_title">Трекер эко-привычек</h1>
      </div>
      <AddPlanModal v-if="showModal" @close="closeModal"></AddPlanModal>
      <button class="eco-button create" @click="openModal()">Создать план</button>
      <div class="plan_list">
        <ul class="plan_card" v-for="plan in plans" :key="plan.id">
          <li class="plan_goal"> {{plan.goal}}</li>
          <li class="plan_habit" v-for="habit in plan.habits" :key="habit.id">
            <p class="habit_title">{{habit.habit.title}}</p>
            <input class="habit_checkbox" v-model=isChecked[habit.id] type="checkbox" :disabled="habit.status" :checked="habit.status" @input="complete(habit.id)"/>
          </li>
          <li>
            <button @click="showQuestions(plan.url)" v-if="!showList(plan.url)" class="eco-button">Самоанализ</button>
            <ul class="questions" v-if="showList(plan.url)">
              <li class="question" v-for="question in plan.form.questions" :key="question.id">
                <p class="question_title">{{question.title}}</p>
                <input class="question_input" @input="questionUrl[question.id]=question.url" v-model=answers[question.id] placeholder="Напишите свой ответ" type="text">
              </li>
              <li>
                <button @click="sendAnswers(plan.form)" class="eco-button">Завершить план</button>
              </li>
            </ul>
          </li>
        </ul>
      </div>
      <div v-if="achievementNotify" class="modal">
        <div class="modal_title">
          <p class="title">Вы получили награду!</p>
          <button  class="close" @click="achievementNotify = null"></button>
        </div>
        <div class="modal_body">
          <p class="body_title">{{achievementNotify.achievement.title}}</p>
          <img class="modal_img" :src='achievementNotify.achievement.icon' alt="Иконка награды">
          <p class="body_description">{{achievementNotify.achievement.description}}</p>
          <button  class="eco-button" @click="achievementNotify = null">ОК</button>
        </div>
      </div>
    </main>
  </div>
</template>
<script>
import ProfileMenu from '../components/ProfileMenu.vue'
import AddPlanModal from '../components/AddPlan.vue'
import {store} from '../store.js'
import { onMounted, computed } from 'vue';
import axiosInstance from '../http.js'
import axios from 'axios'

const user = computed(() => store.state.user) 
const plans = computed(() => store.state.plans)
// const achievementNotify = computed(() => store.state.achievement)

export default {
    components: {
      ProfileMenu,
      AddPlanModal,
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
          .get('/userplans')
          .then(res => {
            console.log(res.data)
            store.commit('setPlans', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        
      })

    },
    data() {
      return {
        user: user,
        plans: plans,
        showModal: false,
        achievementNotify: null,
        answers: {},
        questionUrl: {},
        openPlan: null,
        isChecked: {}

        
      }
    },
    methods: {
        async complete(habitId){
          console.log(habitId)
          let achievement
          await axiosInstance
            .patch(`userhabits/${habitId}/`, {
              status: 'True'
            })
            .then((res) => {
              console.log(res.data)
              achievement = res.data.achievement.url
              // console.log(achievement)
            })  
            .catch((err) => {
              console.log(err)
            }) 
          if (achievement){
            await axios
            .get(`${achievement}`)
            .then((res) => {
              console.log(res.data)
              this.achievementNotify = res.data
              store.commit('setAchievement', res.data)
            })  
            .catch((err) => {
              console.log(err)
            }) 
          }
          await axiosInstance
            .get('/userplans')
            .then(res => {
              console.log(res.data)
              store.commit('setPlans', res.data)
            })
            .catch((err) => {
              console.log(err)
            })
          // style.disabled = true
        },
        openModal(){
          this.showModal = true
        },
        closeModal() {
          this.showModal= false;
          axiosInstance
          .get('/userplans')
          .then(res => {
            console.log(res.data)
            store.commit('setPlans', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        },
        async sendAnswers(formQuestions){
          await formQuestions.questions.map( question => 
            axiosInstance
              .post('/answers/', {
                question: question.url,
                answer: this.answers[question.id],
                user: this.user.url
              })
              .then(res => {
                console.log(res.data)
              })
              .catch((err) => {
                console.log(err)
              }) 
          )
          
        },
        showQuestions(planId){
          this.openPlan = this.openPlan === planId ? null : planId;
        },
        showList(planId){
          // console.log(planId, this.openPlan)
          return this.openPlan === planId;
        }


    }
}
</script>

<style scoped>
.create{
  margin: 10px;
}
.plan_card{
  list-style-type: none;
  min-width: 300px;
  max-width: 400px;
  height: fit-content;
  border: 1px solid lightgrey;
  border-radius: 8px;
  background-color: white;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px;
}
.plan_list{
  display: grid;
  gap: 10px;
  grid-template-columns: 1fr 1fr;
  margin: 10px;
}
.plan_habit{
  display: flex;
  gap: 20px;
  align-items: center;
  justify-content: space-between;
  background-color: #F5F5DC;
  padding: 8px;
  border-radius: 8px;
  /* font-weight: 500; */
  font-size: 16px;
}
.plan_goal{
  text-align: left;
  font-weight: 500;
  font-size: 16px;
  font-family: Golos Text, sans-serif;
}
.habit_checkbox{
  border: 1px solid lightgray;
  width: 16px;
  height: 16px;
}
.habit_checkbox:disabled{
  background-color: white;
  color: green;
}

.question_title{
  font-size: 14px;
  color: gray;
  width: 300px;
  margin-bottom: 8px;
}
.question_input{
  width: 300px;
  height: 30px;
  font-family: Raleway, sans-serif;
  border-radius: 4px;
  border: 1px solid lightgray;
  padding: 8px;
}
.questions{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: start;
  gap: 10px;
}



.modal{
  right: 0;
  bottom: 0;
  left: 0;
  top: 0;
  background: white;
  border: lightgray 1px solid;
  border-radius: 8px;
  max-width: 300px;
  height: fit-content;
  margin: auto;
  position: fixed;
}
.modal_title{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
}
.body_description{
  text-align: center;
  color: gray;
  font-size: 14px;
}
.close{
  width: 12px;
  height: 12px;
  background-color: transparent;
  border: none;
  background-image: url('close.svg');
  background-size: cover;
}
.modal_img{
  width: 60px;
  height: 60px;
}
.modal_body{
  display: flex;
  margin: 20px auto;
  flex-direction: column;
  gap: 10px;
  justify-content: center;
  align-items: center;
}
.body_title{
  font-weight: 500;
  font-family: Golos Text, sans-serif;
}

</style>