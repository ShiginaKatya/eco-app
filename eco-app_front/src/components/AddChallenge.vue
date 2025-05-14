<template>
  <div class="modal">
    <div class="modal_title">
      <p v-if="challenge" class="title">Изменить челлендж</p>
      <p v-else class="title">Добавить челлендж</p>
      <button  class="close" @click="closeModal"></button>
    </div>
    <form class="modal_form">
      <div class="modal_column">
        <label class="modal_text" for="title">Название</label>
        <input class="modal_input" v-model="title" type="text"/>
        <label class="modal_text" for="goal">Цель</label>
        <input class="modal_input" v-model="goal" type="text"/>
        <label class="modal_text" for="description">Описание</label>
        <input class="modal_input" v-model="description" type="text"/>
      </div>
      <div class="modal_column">
        <label class="modal_text">Выберите задания для челленджа</label>
        <multiselect
            class="modal_input-multi"
            id="multiselect"
            v-model="value"
            :options="tasks"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
            :preserve-search="true"
            placeholder=""
            label="title"
            track-by="url"
            :preselect-first="false"
          >
          <template #selection="{ values, isOpen }">
            <span class="multiselect__single" v-if="values.length" v-show="!isOpen">{{ values.length }} options selected</span>
          </template>
            <template #option="{ option }">
              <div class="custom-option">
                <div class="option-title">{{ option.title }}</div>
              </div>
            </template>
        </multiselect>
        <p class="habits" v-for="valu in value" :key="valu.id">{{valu.title}}</p>
        <label class="modal_text">Выберите категорию</label>
        <select class="modal_input" v-model="category">
          <option v-for="category in categories" :key="category.id" :value="category.url">
            {{ category.title }}
          </option>
        </select>
        <label class="modal_text" for="start_date">Дата начала</label>
        <input class="modal_input" v-model="start_date" type="date"/>
        <label class="modal_text" for="finish_date">Дата окончания</label>
        <input class="modal_input" v-model="finish_date" type="date"/>
      </div>
      <button v-if="challenge" class="eco-button" @click.prevent="addChallenge()">Изменить</button>
      <button v-else class="eco-button" @click.prevent="addChallenge()">Добавить</button>
      
    </form>
  </div>
</template>
<script>
import axiosInstance from '../http.js'
import Multiselect from 'vue-multiselect'
import { onMounted, computed } from 'vue';
import {store} from '../store.js'

const categories = computed(() => store.state.categories)
const tasks = computed(() => store.state.tasks)

export default {
    components: {
      Multiselect,
    },
    
    setup(){
      onMounted(async () => {
        await axiosInstance
          .get('/categories')
          .then(res => {
            console.log(res.data)
            store.commit('setCategories', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
        await axiosInstance
          .get('/tasks')
          .then(res => {
            console.log(res.data)
            store.commit('setTasks', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
      })
    },
    props: {
      user: Object,
      challenge: Object
    },
    data () {
      return {
        title: '',
        goal: '',
        description: '', 
        categories: categories,
        tasks: tasks,
        value: [],
        category: '',
        start_date: '',
        finish_date: '',
    }},
    created(){
      if (this.challenge){
        this.title = this.challenge.title
        this.goal = this.challenge.goal
        this.description = this.challenge.description
        this.category = this.challenge.category.url
        this.value = this.challenge.tasks
        this.start_date = this.convertToISODate(this.challenge.start_date)
        this.finish_date = this.convertToISODate(this.challenge.finish_date)
      }
    },
    methods: {
      closeModal() {
        this.$emit('close'); 
      },
      convertToISODate(dateString) {
        if (!dateString) return ''
        const parts = dateString.split('.')
        if (parts.length === 3) {
          const day = parts[0]
          const month = parts[1]
          const year = parts[2]
          return `${year}-${month}-${day}`
        }
        return ''
      },
      async addChallenge(){
        const tasks_list = []
        for (i in this.value.length){
          tasks_list.append(this.value[i].url)
        }
        if (this.challenge){
          await axiosInstance
            .patch('/challenges/', {
              title: this.title,
              goal: this.goal,
              description: this.description,
              tasks: [this.value[0].url, this.value[1].url],
              category: this.category,
              start_date: this.start_date,
              finish_date: this.finish_date
            })
            .then(res => {
              console.log(res.data)
            })
            .catch((err) => {
              console.log(err)
            })
        }
        else {
          await axiosInstance
            .post('/challenges/', {
              title: this.title,
              goal: this.goal,
              description: this.description,
              tasks: [this.value[0].url, this.value[1].url],
              category: this.category,
              start_date: this.start_date,
              finish_date: this.finish_date
            })
            .then(res => {
              console.log(res.data)
            })
            .catch((err) => {
              console.log(err)
            })
        }
        },
      }}
      
      

</script>

<style scoped>
.modal{
  right: 0;
  bottom: 0;
  left: 0;
  top: 0;
  background: white;
  border: 1px solid lightgray;
  border-radius: 8px;
  max-width: 450px;
  height: 70%;
  margin: auto;
  position: fixed;
  padding: 16px;
  display: grid;
  gap: 16px;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
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
  gap: 8px;
  justify-content: center;
  align-items: left;
}
.modal_input{
  width: 100%;
  height: 30px;
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
  margin: 0 auto;
}
.habits{
  margin-top: 6px;
  padding: 4px;
  border: 1px solid #C5FDC5;
  border-radius: 4px;

}

</style>
