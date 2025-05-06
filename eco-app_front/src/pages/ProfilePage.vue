<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu></ProfileMenu>
    </aside>
    <main class="main main_sections">
      <section class="main_profile">
        <img src="/profile_image.svg" alt="avatar" class="profile_image">
        <ul class="header_info">
          <li class="info_item">{{ user.username }}</li>
          <li class="info_item-l">{{ userStats[0]?.level.title }}</li>
        </ul>
        <button class="eco-button">Пройти анкетирование</button>
      </section>
      <section class="main_groups">
        <div class="modal" v-if="formGroup">
          <div class="modal_title">
            <p class="title_text">Создать группу</p>
            <button class="close" @click="closeModal"></button>
          </div>
          <input type="text" v-model="group.title">
          <input type="email" v-model="email">
          <button class="eco-button" @click="addUser()">Добавить пользователя</button>
          <p v-for="member in members" :key="member.id">
            {{ member.member.url }}
          </p>
          <button class="eco-button" @click="createGroup()">Cоздать группу</button>
        </div>
        <button class="eco-button" @click="openGroup()">Создать группу</button>
      </section>
      <ul class="main_usergroups">
        <li class="usergroup" v-for="group in groups" :key="group.id">
          <p class="title_text">{{ group.title }}</p>
          <div class="usergroup_confirm" v-if="needConfirm(group.members)">
            <p class="title">Приглашение в группу</p>
            <div v-for="member in group.members" :key="member.id">
              <div class="button_group" v-if="member.user.url === user.url">
                <button class="eco-button" @click="confirmMember(member.url)">Принять</button>
                <button class="eco-button white" @click="deleteMember(member.url)">Отклонить</button>
              </div>
            </div>
          </div>
          <div v-else class="usergroup_group">
            <ul class="group_list">
              <li class="group_member" v-for="member in group.members" :key="member.id">
                <p class="member_name">{{ member.user.username }}</p>
                <p class="member_points">{{ member.member_stat[0]?.points }}</p>
              </li>
            </ul>
          </div>
        </li>
      </ul>
      <section class="main_actions">
        <div class="actions_plan">
          <p class="latest_type">план</p>
          <p class="latest_title">{{ plans[0]?.goal }}</p>
          <p class="latest_progress">Прогресс: {{ challengeProcent(plans[0]?.habits) }} %</p>
        </div>
        <ul class="actions_challenges">
          <li v-for="challenge in userchallenges" :key="challenge.id" class="challenges_latest">
            <p class="latest_type">челлендж</p>
            <p class="latest_title">{{ challenge.challenge.title }}</p>
            <p class="latest_progress">Прогресс: {{ challengeProcent(challenge.tasks) }} %</p>
          </li>
        </ul>
      </section>
      <p class="title_text">Последние изменения в Избранном</p>
      <section class="main_favorites">
        <ul class="favorites_list">
          <li v-for="favorite in favorites" :key="favorite.id" class="list_latest">
            <p class="latest_title">{{ favorite.advice?.title }}{{ favorite.guide?.title}}</p>
            <p class="latest_type">{{ favorite.advice?.description }}{{ favorite.guide?.annotation }}</p>
          </li>
        </ul>
      </section>
    </main>
  </div>
</template>

<script>
import ProfileMenu from '../components/ProfileMenu.vue'
import {store} from '../store.js'
import { onMounted, computed } from 'vue';
import axiosInstance from '../http.js'
import axios from 'axios'

const user = computed(() => store.state.user) 
const userchallenges = computed(() => store.state.userchallenges)
const plans = computed(() => store.state.plans)
const userStats = computed(() => store.state.userstat)
const favorites = computed(() => store.state.favorites)
const users = computed(() => store.state.users)
const groups = computed(() => store.state.groups)


export default {
    components: {
      ProfileMenu,
    },
    setup() {
      onMounted(async () => {
        await axiosInstance
          .get('/userplans/latest')
          .then(res => {
            console.log(res.data)
            store.commit('setPlans', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        await axiosInstance
          .get('/userchallenges/latest')
          .then(res => {
            console.log(res.data)
            store.commit('setUserChallenges', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        await axiosInstance
          .get('/userstats/')
          .then(res => {
            console.log(res.data)
            store.commit('setUserStat', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        await axiosInstance
          .get('/favorites/latest')
          .then(res => {
            console.log(res.data)
            store.commit('setFavorites', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        await axiosInstance
          .get('/groups')
          .then(res => {
            console.log(res.data)
            store.commit('setGroups', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
        
      })
    },
    data() {
      return {
        user: user,
        userchallenges: userchallenges,
        plans: plans,
        userStats: userStats,
        favorites: favorites,
        users: users,
        formGroup: false,
        email: '',
        members: [],
        group: {
          title: ''
        },
        groups: groups

    
      }
    },
    computed:{
    },
    methods: {
      challengeProcent(tasks){
        if (tasks){
          let t = 0
          let f = 0
          tasks.map(task =>{
            if (task.status){
              t = t + 1
            }
            f = f + 1
          })
          return (t/f*100).toFixed()
        }
        else{
          return null
        }
      },
      async openGroup(){
        await axiosInstance
          .get('/users')
          .then(res => {
            console.log(res.data)
            store.commit('setUsers', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
        this.formGroup = true
      },
      addUser(){
        const member = this.users.find(user => user.email === this.email)
        this.members.push({member: member, is_confirm: false})
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
      },
      async confirmMember(memberUrl){
        await axios
          .patch(`${memberUrl}`, {
            is_confirm: true
          })
      },
      async deleteMember(memberUrl){
        await axios
          .delete(`${memberUrl}`)
      },
      sortGroups(){
        this.groups.map(group => (
          group.members
        )

        )
      },
      needConfirm(members){
        return members.some(member => 
          member.user.url === this.user.url && member.is_confirm === false
        )
      }


       
    }
}
</script>

<style scoped>
/* .page{
  display: flex;
}
.sidebar{
  width: fit-content;
}
.main{
  min-width: 320px;
  width: calc(100vw - 300px);
} */

.main_usergroups{
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.main_profile{
  display: flex;
  gap: 16px;
  padding: 16px;
  align-items: center;
  justify-items: center;
}
.profile_image{
  width: 80px;
  border: 1px solid gray;
  padding: 50px;
  border-radius: 50%;
  background-color: grey;
}
.main_actions{
  display: grid;
  gap: 16px;
  grid-template-columns: 2fr 1fr 1fr;
}
.usergroup_confirm{
  display: grid;
  gap: 8px;
}
.usergroup{
  padding: 16px;
  border: 1px solid lightgray;
  border-radius: 8px;
  display: grid;
  gap: 8px;

}
.modal{
  right: 0;
  bottom: 0;
  left: 0;
  top: 0;
  background: white;
  border: 1px solid lightgray;
  border-radius: 8px;
  max-width: fit-content;
  height: fit-content;
  max-height: 100vh;
  margin: auto;
  position: fixed;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
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
.modal_input{
  width: 100%;
  height: 40px;
  font-size: 16px;
  font-family: Raleway, sans-serif;
  border-radius: 4px;
  border: 1px solid lightgray;
  padding: 8px;
}

.actions_challenges{
  display: flex;
  flex-direction: column;
  gap: 20px;

}
.actions_plan{
  border: 1px solid gray;
  border-radius: 8px;
  height: 300px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.challenges_latest{
  min-width: 300px;
  max-width: 500px;
  border: 1px solid gray;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  gap: 10px;
  flex-direction: column;
  justify-content: space-between;

}
.latest_title{
  font-weight: 500;
  font-size: 16px;
  font-family: 'Golos Text', sans-serif;
}
.latest_type{
  font-size: 14px;
  color: grey;
}
.favorites_list{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.list_latest{
  padding: 16px;
  border: 1px solid gray;
  border-radius: 8px;
  display: grid;
  gap: 8px;

}
.info_item{
  font-size: 16px;
  font-weight: 500;
  font-family: Golos Text, sans-serif;
}
.info_item-l{
  font-size: 14px;
  color: gray
}

</style>