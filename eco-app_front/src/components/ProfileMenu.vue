<template>
    <nav class="sidebar_menu">
      <ul class="menu_list">
        <li class="menu_profile">
          <router-link class="menu_link" to="/profile">
            <img src="/profile_image.svg" alt="картинка" class="profile_picture">
            <div class="profile_group">
              <p class="profile_name">{{user.username}}</p>
              <p class="profile_email">{{user.email}}</p>
            </div> 
          </router-link>
        </li>
        <li class="menu_group">действия</li>
        <li class="menu_item" v-for="item in topMenu" :key="item.id">
          <router-link class="menu_link" :to=item.link :style="getStyle(item.link)">{{item.title}}</router-link>
        </li>
      </ul>
      <ul class="menu_list">
        <li class="menu_group">информация</li>
        <li class="menu_item" v-for="item in bottomMenu" :key="item.id">
          <router-link class="menu_link" :to=item.link :style="getStyle(item.link)">{{item.title}}</router-link>
        </li>
        <li class="menu_item" v-if="user.role?.title=='Организация'">
          <router-link class="menu_link" to="/event">Мероприятия</router-link>
        </li>
        <li class="menu_logout">
          <router-link @click="logout" class="menu_link logout" to="/login">
            <p class="logout_title">Выйти</p>
            <img src="/logout.svg" alt="картинка" class="logout_picture">
          </router-link>
        </li>
      </ul>

    </nav>
</template>

<script>
import { store } from '../store.js'
import { computed, onMounted } from 'vue';
import axiosInstance from '../http.js'

const user = computed(() => store.state.user)


export default {
  setup(){
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
              
        }})

  },
  data() {
    return {
      user: user,
      topMenu: [
        { id: 1, title: 'Прогресс', link: '/statistic'},
        { id: 2, title: 'Трекер эко-привычек', link: '/habits'},
        { id: 3, title: 'Челленджи', link: '/challenges'},
      ],
      bottomMenu: [
        { id: 1, title: 'Советы', link: '/advices'},
        { id: 2, title: 'Руководства', link: '/guides'},
        { id: 3, title: 'Избранное', link: '/favorites'},
      ]
    }
  },
  methods: {
    getStyle(itemLink){
      if (this.$route.path === itemLink) {
        return {
          'background': '#C5FDC5',
          'border-radius': '8px',
          'font-weight': '500',
        }
      }
    },
    async logout() {
      await axiosInstance
        .post('logout/')
        .then(res => console.log(res))
        .catch(err => console.log(err))
      await axiosInstance
        .post(`token/blacklist/`, {
          refresh: `${window.localStorage.getItem('refresh_token')}`
        })
        .catch(err => console.log(err))
      store.commit('setIsAuthenticated', false)
      window.localStorage.removeItem('access_token')
      window.localStorage.removeItem('refresh_token')
      window.localStorage.removeItem('userId')
      window.location.href = 'login'
    }
    }
  }

</script>

<style scoped>

.sidebar_menu{
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  /* top: 0;
  left: 0; */
  height: 100vh;
  width: 270px;
  border-radius: 8px;
  border-right: 1px solid lightgray;

}
.menu_list{
  list-style-type: none;
  display: flex;
  flex-direction: column;

}
.menu_profile{
  border-bottom: 1px solid lightgray;
  /* padding: 10px 15px; */
}
.menu_logout{
  border-top: 1px solid lightgray;
}
.menu_group{
  font-size: 10px;
  color: #478A55;
  text-transform: uppercase;
  font-family: Golos Text, sans-serif;
  font-weight: bolder;
  margin: 4px 8px;
  
}
.menu_link{
  margin: 4px 8px;
  padding: 8px;
  display: block;
  color: black;
  font-size: 16px;
  font-family: Golos Text, sans-serif ;
}
.menu_link:hover{
  background-color: #C5FDC5;
  border-radius: 8px;
  color: black;
  font-weight: 500;
}
.menu_profile .menu_link{
  display: flex;
  gap: 24px;
  justify-content: flex-starts;
  align-items: center;
}
.profile_picture{
  width: 40px;
  display: block;
}
.profile_name{
  font-size: 18px;
  font-weight: 500;
}
.profile_email{
  color: gray;
}
.logout{
  display: flex;
  justify-content: space-between;
  color: gray;
}
.logout_picture{
  width: 18px;
}


</style>