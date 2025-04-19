<template>
      <div class="modal">
        <div class="modal_title">
          <p class="title">Создать план по привычкам</p>
          <button  class="close" @click="closeModal"></button>
        </div>
        <form class="modal_form" >
            <label class="modal_text" for="goal">Цель</label>
            <input class="modal_input" v-model="goal"  type="text"/>
            <label class="modal_text" for="multiselect">Выберите привычки</label>
            <multiselect
              class="modal_input-multi"
              id="multiselect"
              v-model="value"
              :options="habits"
              :multiple="true"
              :close-on-select="false"
              :clear-on-select="false"
              :preserve-search="true"
              placeholder=""
              label="title"
              track-by="title"
              :preselect-first="true"
            >
            <template #selection="{ values, isOpen }">
              <span class="multiselect__single" v-if="values.length" v-show="!isOpen">{{ values.length }} options selected</span>
            </template>
              <template #option="{ option }">
                <div class="custom-option">
                  <div class="option-title">{{ option.title }}</div>
                  <div class="option-category">{{option.category.title }}</div>
                </div>
              </template>
            </multiselect>
            <p class="habits" v-for="valu in value" :key="valu.id">{{valu.title}}</p>
            <button class="eco-button"  @click.prevent="addPlan()" >Сохранить</button>
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
    // props: {
    //   showModal: Boolean,
    // },
    data () {
      return {
        value: [],
        habits: habits,
        goal: '',
        user: user,
        plan: plan,
        showModal: true,

    }},
    methods: {
      closeModal() {
        this.$emit('close'); 
      },
      async addPlan(){
        await axiosInstance
          .post('userplans/', {
            user: this.user.url,
            goal: this.goal,
            status: 'False',
          })
          .then((res) => {
            console.log(res.data)
            store.commit('setPlan', res.data)
          })  
          .catch((err) => {
            console.log(err)
          }) 
        await Promise.all(
          this.value.map(valu =>
            axiosInstance
              .post('userhabits/', {
                habit: valu.url,
                plan:  store.state.plan.url,
                status: 'False'
              })
              .then((res) => {
                console.log(res.data)
              })  
              .catch((err) => {
                console.log(err)
              })))
        this.$emit('close')
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
  border: 1px solid lightgray;
  border-radius: 8px;
  max-width: 400px;
  height: fit-content;
  margin: auto;
  position: fixed;
  padding: 12px 16px;
}
p, li{
  font-size: 16px;
}
.modal_title{
  display: flex;
  justify-content: space-between;
  align-self: stretch;
  align-items: center;
}
.title{
  font-size: 16px;
  font-weight: 500;
  font-family: Golos Text, sans-serif;
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
  padding: 10px 0;
  justify-content: center;
  align-items: left;
}
.modal_input{
  width: 100%;
  height: 40px;
  font-size: 16px;
  font-family: Raleway, sans-serif;
  border-radius: 4px;
  border: 1px solid lightgray;
  padding: 8px;
}
.modal_input-multi{
  color: black;
  font-size: 14px;
}

.modal_text{
  font-size: 12px;
  color: grey;
  font-weight: 500;
  padding-top: 8px ;
  padding-bottom: 4px;
}
.option-title {
  font-weight: 400;
  color: black;
  font-size: 14px;
}
.multiselect__element:hover {
  background-color: lightblue !important;
}
.option-category {
  color: #888; 
  font-weight: 300;
  font-size: 14px;
}
.eco-button{
  margin: 10px auto;
}
.habits{
  margin-top: 6px;
  padding: 4px;
  border: 1px solid #C5FDC5;
  border-radius: 4px;

}

</style>
