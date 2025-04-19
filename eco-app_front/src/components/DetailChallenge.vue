<template>
  <div class="modal">
    <div class="modal_title">
      <p class="title_text">{{ challenge.title }}</p>
      <button  class="close" @click="closeModal"></button>
    </div>
    <p class="modal_text">Цель</p>
    <p class="goal">{{ challenge.goal }}</p>
    <p class="modal_text">Описание</p>
    <p class="description">{{ challenge.description }}</p>
    <p class="modal_text">Категория</p>
    <p class="category">{{ challenge.category.title }}</p>
    <p class="modal_text">Задания</p>
    <ul class="tasks_list">
      <li class="task" v-for="task in challenge.tasks" :key="task.id">
        {{ task.title }}
      </li>
    </ul>
    <p class="modal_text">Даты проведения</p>
    <p class="date">{{ challenge.start_date }} - {{ challenge.finish_date }}</p>
    <div class="button">
      <button class="eco-button" @click="addChallenge()" :disabled="ifDisabled(challenge)">{{ challengeStatus(challenge) }}</button>
    </div>
  </div>
</template>

<script>
import {store} from '../store.js'
import { onMounted, computed } from 'vue';
import axiosInstance, { API_URL } from '../http.js'

// const habits = computed(() => store.state.habits)
// const plan = computed(() => store.state.plan)
// const user = computed(() => store.state.user)
const userchallenge = computed(() => store.state.userchallenge)
const userchallenges = computed(() => store.state.userchallenges)

export default {
  setup(){
    
  }, 
  props: {
    challenge: Object,
    user: Object
  },
  data () {
    return {
      userchallenge:userchallenge,
      userchallenges: userchallenges,
      userStatus: true

  }},
  methods: {
    closeModal() {
      this.$emit('close'); 
    },
    async addChallenge(){
      console.log(this.challenge)
      await axiosInstance
        .post('/userchallenges/', {
          challenge: this.challenge.url,
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
      if (this.challenge.tasks != []){
        await Promise.all(
          this.challenge.tasks.map(task =>
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
      this.closeModal() 
    },
    challengeStatus(challenge){
      if (this.userchallenges.find(userchallenge => userchallenge.challenge.url == challenge.url)){
        return 'Участвуете'
      }
      else{
        return 'Участвовать'
      }
    },
    ifDisabled(challenge){
      if (this.userchallenges.find(userchallenge => userchallenge.challenge.url == challenge.url)){
        return true
      }
      else {
        return false
      }
    },
    
  }
}
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
.modal{
  right: 0;
  bottom: 0;
  left: 0;
  top: 0;
  background: white;
  border: 1px solid lightgray;
  border-radius: 8px;
  max-width: 600px;
  height: 80%;
  max-height: 100vh;
  margin: auto;
  position: fixed;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;

}
.modal::-webkit-scrollbar {
    display: none; /* Для Chrome, Safari и Opera */
}
p, li{
  font-size: 14px;
}
.modal_title{
  display: flex;
  justify-content: space-between;
  align-self: stretch;
  align-items: center;
}
.title_text{
  font-size: 16px;
  font-weight: 500;
  font-family: Golos Text, sans-serif;
}
.modal_text{
  font-size: 12px;
  color: grey;
  font-weight: 500;
  padding-top: 8px ;
  padding-bottom: 4px;
}
.tasks_list{
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.goal{
  font-weight: 500;
}
.task{
  padding: 8px;
  background-color: #F5F5DC;
  border-radius: 8px;
  width: fit-content;
  font-weight: 500;
}

.close{
  width: 14px;
  height: 14px;
  background-color: transparent;
  border: none;
  background-image: url('close.svg');
  background-size: cover;
}
.button{
  align-self: flex-end;
}
.category{
  color: #2E8B57;
  padding: 4px;
  border: 1px solid #2E8B57;
  border-radius: 8px;
  width: fit-content;
}
.date{
  color: #2E8B57;
  font-weight: 500;
}

</style>
