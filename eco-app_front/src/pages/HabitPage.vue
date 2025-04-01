<template>
    <div class="page">
        <aside class="sidebar">
            <ProfileMenu></ProfileMenu>
        </aside>
        <main class="main">
            <AddPlanModal v-if="showModal" @close="closeModal"></AddPlanModal>
            <button class="eco-button" @click="openModal()">Создать план</button>
            <div class="plan_list">
              <ul class="plan_card" v-for="plan in plans" :key="plan.id">
                <li class="plan_goal"> {{plan.goal}}</li>
                <li class="plan_habit" v-for="habit in plan.habits" :key="habit.id">
                    <p class="habit_title">{{habit.habit.title}}</p>
                    <button class="eco-button"  @click="complete(habit.id)" :style="getButtonStyle(habit.status)">
                      <span v-if="habit.status">Выполнено</span>
                      <span v-else >Выполнить</span>
                    </button>
                </li>
                <li>
                  <button class="eco-button">Пройти анкетирование</button>
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
const achievementNotify = computed(() => store.state.achievement)

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
        achievementNotify: null
      }
    },
    methods: {
        async complete(habitId){
          let achievement
          await axiosInstance
            .patch(`userhabits/${habitId}/`, {
              status: 'True'
            })
            .then((res) => {
              achievement = res.data.achievement.url
              console.log(achievement)
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
          style.disabled = true

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

        getButtonStyle(habitStatus){
          if (habitStatus){
            return {
              'background': 'grey'
            }
          }
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
.plan_card{
  list-style-type: none;
  min-width: 300px;
  max-width: 400px;
  height: fit-content;
  border: 1px solid grey;
  border-radius: 25px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
}
.plan_list{
  display: grid;
  gap: 10px;
  grid-template-columns: 1fr 1fr;
  margin: 10px;
}
.plan_habit{
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
}
.plan_goal{
  text-align: center;
  font-weight: 500;
  border-bottom: 1px solid grey;

}
.eco-button:hover{
  background-color: white;
}

.modal{
  right: 0;
  bottom: 0;
  left: 0;
  top: 0;
  background: white;
  border: gray 1px solid;
  border-radius: 25px;
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
  border-bottom: gray 1px solid;
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
}

</style>