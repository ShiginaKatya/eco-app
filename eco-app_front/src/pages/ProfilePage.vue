<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu :burgerMenu="openingMenu" @close="closeMenu()"></ProfileMenu>
    </aside>
    <main  class="main main_sections">
      <section class="main_profile">
        <img src="/profile_image.svg" alt="avatar" class="profile_image">
        <ul class="header_info">
          <li class="info_item">{{ user.username }}</li>
          <li v-if="user.role?.title === 'Пользователь'" class="info_item-l">{{ userStats[0]?.level.title }}</li>
          <li v-else class="info_item-l">{{ user.role?.title }}</li>
        </ul>
        <button v-if="user.role?.title === 'Пользователь'" class="eco-button" @click="sendChange()">Сделать аккаунт организации</button>
      </section>
      <section v-if="user.role?.title !== 'Администратор'" class="main_groups">
        <button class="eco-button" @click="openGroup()">Создать группу</button>
        <AddGroup v-if="formGroup" :user="user" @close="closeModal()"></AddGroup>
      </section>
      <ul v-if="user.role?.title !== 'Администратор'" class="main_usergroups">
        <li class="usergroup" v-for="group in groups" :key="group.id">
          <p class="title_text">{{ group.title }}</p>
          <div class="usergroup_confirm" v-if="needConfirm(group.members)">
            <p class="title">Приглашение в группу</p>
            <div v-for="member in group.members" :key="member.id">
              <div class="button_group" v-if="member.user.url === user.url">
                <button class="eco-button" @click="confirmMember(member.url)">Принять</button>
                <button class="eco-button exit" @click="deleteMember(member.url)">Отклонить</button>
              </div>
            </div>
          </div>
          <div v-else class="usergroup_group">
            <ul class="group_list">
              <li class="group_member" v-for="member in group.members" :style="getStyle(member)" :key="member.id">
                <div class="member_user">
                  <img src="/profile_group.png" alt="">
                  <p class="member_name">{{ member.user.username }}</p>
                </div>
                <p v-if="member.is_confirm" class="member_points">{{ member.member_stat[0]?.points }}</p>
                <p v-else class="member_status">Подтверждение...</p>
              </li>
            </ul>
            <button  class="eco-button exit">Выйти из группы</button>
          </div>
         
        </li>
      </ul>
       <p v-if="user.role?.title !== 'Администратор'" class="title_text">Последние действия</p>
      <section v-if="user.role?.title !== 'Администратор'" class="main_actions">
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
      <p v-if="user.role?.title !== 'Администратор'" class="title_text">Последние изменения в Избранном</p>
      <section v-if="user.role?.title !== 'Администратор'" class="main_favorites">
        <ul class="favorites_list">
          <li v-for="favorite in favorites" :key="favorite.id" class="list_latest">
            <p class="latest_title">{{ favorite.advice?.title }}{{ favorite.guide?.title}}</p>
            <p class="latest_type">{{ favorite.advice?.description }}{{ favorite.guide?.annotation }}</p>
          </li>
        </ul>
      </section>
      <section class="main_confirm" v-else>
        <p class="title_text">Заявки на регистрацию организации</p>
        <ul class="confirm_list">
          <li class="confirm_organization" v-for="organization in send_organizations" :key="organization.id">
            <p class="confirm_text">{{ organization.username }}</p>
            <p class="confirm_text">{{ organization.email }}</p>
            <div class="confirm_buttons">
              <button class="eco-button" @click="changeRole(organization.id)">Изменить</button>
              <button class="eco-button cancel" @click="cancelChange(organization.id)">Отменить</button>
            </div>
          </li>
        </ul>
      </section>
    </main>
  </div>
</template>

<script>
import ProfileMenu from '../components/ProfileMenu.vue'
import {store} from '../store.js'
import {useStore} from 'vuex'
import { onMounted, computed } from 'vue';
import axiosInstance from '../http.js'
import axios from 'axios'
import AddGroup from '../components/AddGroup.vue';


const userchallenges = computed(() => store.state.userchallenges)
const plans = computed(() => store.state.plans)
const userStats = computed(() => store.state.userstat)
const favorites = computed(() => store.state.favorites)
const users = computed(() => store.state.users)
const groups = computed(() => store.state.groups)
const send_organizations = computed(() => store.state.send_organizations)
const roles = computed(() => store.state.roles)

// const user = computed(() => store.state.user) 
export default {
    components: {
      ProfileMenu,
      AddGroup
    },
    setup() {
      const user = computed(() => store.state.user) 

      const loadUser = async () => {
        await store.dispatch('loadUser')

      }
      onMounted(async () => {
        await loadUser()
        if (user.value && user.value.role.title === 'Администратор') {
          await axiosInstance
            .get('/users?want_organization=True')
            .then(res => {
              console.log(res.data)
              store.commit('setSendOrganizations', res.data)
            })
            .catch((err) => {
              console.log(err)
            }) 
          await axiosInstance
            .get('roles/')
            .then(res => {
              console.log(res.data)
              store.commit('setRoles', res.data)
            })
            .catch((err) => {
              console.log(err)
            }) 
        }
        if (user.value && user.value.role.title !== 'Администратор'){
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
        } 
      })
      return {
        user
      }
    },
    data() {
      return {
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
        groups: groups,
        send_organizations: send_organizations,
        roles: roles,

    
      }
    },
    computed:{
    },
    methods: {
      getStyle(member){
        if (member.is_confirm){
          if (member.user.url === this.user.url){
            return {
              'backgroundColor': '#E0FFE0',
              'borderColor': '#2E8B57'
            }
          }
          else{
            return {
              'borderColor': '#2E8B57'
            }
          }
  
        }
        else{
          return {
            'borderColor': 'lightgray'
          }
        }
      },
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
      },
      async sendChange(){
        await axiosInstance
          .patch(`users/${this.user.id}/`,{
            want_organization: true
          })
          .then(res => {
            console.log(res.data)
          })
          .catch((err) => {
            console.log(err)
          })
      },
      async changeRole(organizationId){
        await axiosInstance
          .patch(`users/${organizationId}/`,{
            role: this.roles.find(role => role.title === 'Организация').url,
            want_organization: false
          })
          .then(res => {
            console.log(res.data)
          })
          .catch((err) => {
            console.log(err)
          })
      },
      async cancelChange(organizationId){
        await axiosInstance
          .patch(`users/${organizationId}/`,{
            want_organization: false
          })
          .then(res => {
            console.log(res.data)
          })
          .catch((err) => {
            console.log(err)
          })
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
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.main_profile{
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding-top: 16px;
  align-items: center;
  justify-items: start;
}
.profile_image{
  width: 80px;
  border: 1px solid lightgray;
  padding: 50px;
  border-radius: 50%;
  background-color: grey;
}
.main_actions{
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(2, 1fr);
}
.usergroup_confirm{
  display: flex;
  gap: 8px;
  align-items: center;
}

.usergroup{
  padding: 16px;
  border: 1px solid lightgray;
  border-radius: 8px;
  display: grid;
  gap: 16px;

}

.actions_challenges{
  display: flex;
  flex-direction: column;
  gap: 16px;

}
.actions_plan{
  border: 1px solid lightgray;
  border-radius: 8px;
  grid-row: span 2;
  grid-column: span 2;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.challenges_latest{
  border: 1px solid lightgray;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  gap: 10px;
  flex-direction: column;
  justify-content: space-between;

}
.latest_title, .title_text{
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
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.exit{
  align-self: end;
  background-color: white;
  border: 1px solid lightgray;
}

@media screen and (max-width: 1024px) and (min-width: 768px){
  .favorites_list{
    grid-template-columns: repeat(2, 1fr);
  }
  .main_actions{
    grid-template-columns: repeat(2, 1fr);
  }
  .actions_plan{
    grid-column: span 1;
  }

}
.list_latest{
  padding: 16px;
  border: 1px solid lightgray;
  border-radius: 8px;
  display: grid;
  gap: 8px;

}
.member_points{
  font-size: 16px;
  font-weight: 500;
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
.main_confirm{
  display: grid;
  gap: 16px;
}
.confirm_list{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.confirm_organization{
  display: flex;
  gap: 16px;
  padding: 16px;
  border: 1px solid lightgray;
  align-items: center;
  justify-content: space-between;
  border-radius: 8px;
  grid-column: span 1;
}
.cancel{
  background-color: white;
  border: 1px solid lightgray;
}
.confirm_buttons{
  display: flex;
  gap: 8px;
}
.group_list{
  display: grid;
  gap: 8px;
}
.group_member{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid lightgray;
  border-radius: 4px;
  padding: 8px;
  gap: 16px;
}
.member_status{
  font-size: 14px;
  color: gray;
}
.member_user{
  display: flex;
  gap: 4px;
  align-items: center;
}
.button_group{
  display: flex;
  gap: 8px;
}
.usergroup_group{
  display: grid;
  gap: 16px;
}

</style>