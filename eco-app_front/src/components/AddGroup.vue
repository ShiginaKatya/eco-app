<template>
  <div class="modal">
    <div class="modal_title">
      <p class="title">Создать группу</p>
      <button  class="close" @click="closeModal"></button>
    </div>
    <form class="modal_form" >
      <label class="modal_text" for="group.title">Название</label>
      <input class="modal_input" v-model="group.title" type="text"/>
      <label class="modal_text" for="email">Email участника</label>
      <div class="input_group">
        <input type="email" class="modal_input" v-model="email">
        <button class="eco-button" @click.prevent="addUser()">Добавить</button>
      </div>
      <p class="modal_text" v-if="message">{{ message }}</p>
      <p v-for="member in members" :key="member.id">{{ member.member.email }}</p>
      <button class="eco-button" @click.prevent="createGroup()">Создать</button>
    </form>
  </div>
</template>
<script>
import axiosInstance from '../http.js'
import {store} from '../store.js'
import { onMounted, computed } from 'vue';

const users = computed(() => store.state.users)

export default {
    props: {
      user: Object,
    },
    data () {
      return {
       group: {
          title: ''
        },
        email: '', 
        members: [],
        users: users,
        message: null
    }},
    methods: {
      closeModal() {
        this.$emit('close'); 
      },
      addUser(){
        const member = this.users.find(user => user.email === this.email)
        if (member){
          this.members.push({member: member, is_confirm: false})
          this.message = null
        }
        else {
          this.message = 'Пользователь с таким email не найден'
        }
        this.email = ''
        console.log(this.members)
      },
      async createGroup(){
        this.members.push({member: this.user, is_confirm: true})
        this.group.members = this.members.map(member => ({
          user: member.member.url,
          is_confirm: member.is_confirm
        }))
        console.log(this.group)
        await axiosInstance
          .post('/groups/', this.group)
          .then(res => {
            console.log(res.data)
          })
          .catch((err) => {
            console.log(err)
          })
        this.$emit('close')
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
  max-width: 400px;
  height: fit-content;
  margin: auto;
  position: fixed;
  padding: 16px;
  display: grid;
  gap: 16px;
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
  width: 16px;
  height: 16px;
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
  height: 40px;
  font-size: 14px;
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
  font-size: 14px;
  color: grey;
  font-weight: 500;
}
.option-title {
  font-weight: 400;
  color: black;
  font-size: 14px;
}

.option-category {
  color: #888; 
  font-weight: 300;
  font-size: 14px;
}
.modal .eco-button{
  margin: 0 auto;
}
.input_group{
  display: flex;
  gap: 8px;
}



</style>
