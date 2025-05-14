<template>
  <div class="modal">
    <div class="modal_title">
      <p v-if="advice" class="title">Опубликовать челлендж</p>
      <p v-else class="title">Добавить челлендж</p>
      <button  class="close" @click="closeModal"></button>
    </div>
    <form class="modal_form">
      <label class="modal_text" for="title">Совет</label>
      <input class="modal_input" v-model="title" type="text"/>
      <label class="modal_text" for="description">Описание</label>
      <input class="modal_input" v-model="description" type="text"/>
      <label class="modal_text">Выберите категорию</label>
      <select class="modal_input" v-model="category">
        <option v-for="category in categories" :key="category.id" :value="category.url">
          {{ category.title }}
        </option>
      </select>
      <label class="modal_text">Добавьте иконку к совету</label>
      <input type="file" class="eco-button" @change="addIcon"/>
      <button class="eco-button" @click.prevent="addAdvice()">Опубликовать</button>
    </form>
  </div>
</template>
<script>
import axiosInstance from '../http.js'
import { onMounted, computed } from 'vue';
import {store} from '../store.js'

const categories = computed(() => store.state.categories)

export default {
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
      })
    },
    props: {
      user: Object,
      advice: Object
    },
    data () {
      return {
        title: '',
        description: '', 
        categories: categories,
        category: '',
        icon_file: '',
    }},
    created(){
      if (this.advice){
        this.title = this.advice.title
        this.description = this.advice.description
        this.category = this.advice.category?.url
      }
    },
    methods: {
      closeModal() {
        this.$emit('close'); 
      },
      addIcon(event) {
        const file = event.target.files[0];
        this.icon_file = file;
      },
      async addAdvice(){
        const adviceData = new FormData(); ; 
        adviceData.append('title', this.title);
        adviceData.append('description', this.description);
        adviceData.append('icon', this.icon_file);
        adviceData.append('category', this.category);
        adviceData.append('is_posted', 'True');
        if (this.advice){
          await axiosInstance
            .patch(`advices/${this.advice.id}/`, adviceData, {
              headers: {
                'Content-Type': 'multipart/form-data' 
              }
            })
            .then((res) => {
              console.log(res.data)
            })
            .catch((err) => {
              console.log(err)
            })
        }
        else {
          await axiosInstance
            .post('advices/', adviceData, {
              headers: {
                'Content-Type': 'multipart/form-data' 
              }
            })
            .then((res) => {
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
