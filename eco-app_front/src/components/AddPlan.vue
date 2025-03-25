<template>
      <div class="modal">
        <div class="modal_title">
          <p class="title">Добавить новый план</p>
          <button  class="close" @click="closeModal()"></button>
        </div>
        <form class="modal_form" @submit.prevent ="addPlan">
            <input class="modal_input" v-model="goal" placeholder="Цель" type="text"/>
            <multiselect class="modal_input" id="multiselect" v-model="value" :options="habits" :multiple="true" :close-on-select="false" :clear-on-select="false"
                 :preserve-search="true" placeholder="Выберите привычки" label="title" track-by="title" :preselect-first="true">
                <template #selection="{ values, isOpen }">
                    <span class="multiselect__single" v-if="values.length" v-show="!isOpen">
                        {{ values.length }} options selected
                    </span>
                </template>
            </multiselect>
            <p v-for="valu in value" :key="valu.id">{{valu.title}}</p>
            <button class="eco-button" type="submit" @click="closeModal()">Добавить</button>
        </form>
      </div>
</template>
<script>
import Multiselect from 'vue-multiselect'
import {store} from '../store.js'
import { onMounted, computed } from 'vue';
import axiosInstance, { API_URL } from '../http.js'

const habits = computed(() => store.state.habits)
const plan = computed(() => store.state.plan)
const user = computed(() => store.state.user)


export default {
    components: {
      Multiselect,
    },
    setup(){
      onMounted(async () => {
        await axiosInstance
          .get('/habits')
          .then(res => {
            console.log(res.data)
            store.commit('setHabits', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
      })
    }, 
    data () {
      return {
        value: [],
        habits: habits,
        goal: '',
        user: user,
        plan: plan,

    }},
    methods: {
      async addPlan(){
        await axiosInstance
          .post('userplans/', {
            user: this.user.url,
            goal: this.goal,
            status: 'False'
          })
          .then((res) => {
            console.log(res.data)
            store.commit('setPlan', res.data)
          })  
          .catch((err) => {
            console.log(err)
          }) 
        await 
          this.value.map(valu =>
            axiosInstance
              .post('userhabits/', {
                habit: valu.url,
                plan: this.plan.url,
                status: 'False'
              })
              .then((res) => {
                console.log(res.data)
              })  
              .catch((err) => {
                console.log(err)
              }) 
           )   
      },
}}
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
.modal{
  right: 0;
  bottom: 0;
  left: 0;
  top: 0;
  background: white;
  border: gray 1px solid;
  border-radius: 25px;
  max-width: 400px;
  height: 250px;
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
.modal_form{
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 320px;
  justify-content: center;
  align-items: center;
  margin: 10px auto;
}
.modal_input{
  width: 320px;
  min-height: 40px;
  border: 1px solid lightgrey;
  border-radius: 5px;
}

</style>
