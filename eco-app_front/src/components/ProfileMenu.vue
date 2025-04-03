<template>
    <nav class="sidebar_menu">
      <ul class="menu_list">
        <li class="menu_profile">
          <img src="/profile_image.svg" alt="картинка" class="profile_picture">
          <!-- <p class="profile_name">{{ user.username }}</p> -->
          <p class="profile_name">{{user.username}}</p>
        </li>
        <li class="menu_item" v-for="item in topMenu" :key="item.id">
          <router-link class="menu_link" :to=item.link :style="getStyle(item.link)">{{item.title}}</router-link>
        </li>
      </ul>
      <ul class="menu_list">
        <li class="menu_item" v-for="item in bottomMenu" :key="item.id">
          <router-link class="menu_link" :to=item.link :style="getStyle(item.link)">{{item.title}}</router-link>
        </li>
        <!-- <li class="menu_item" v-if="user.role.title='Организация'">
          <router-link class="menu_link" to="/events" >Мероприятия</router-link>
        </li> -->
      </ul>
    </nav>
</template>

<script>
import { store } from '../store.js'
import { computed } from 'vue';

const user = computed(() => store.state.user)


export default {
  data() {
    return {
      user: user,
      topMenu: [
        { id: 1, title: 'ПРОГРЕСС', link: '/statistic'},
        { id: 2, title: 'ТРЕКЕР ЭКО-ПРИВЫЧЕК', link: '/habits'},
        { id: 3, title: 'ЧЕЛЛЕНДЖИ', link: '/challenges'},
      ],
      bottomMenu: [
        { id: 1, title: 'СОВЕТЫ', link: '/advices'},
        { id: 2, title: 'РУКОВОДСТВА', link: '/guides'},
        { id: 3, title: 'ИЗБРАННОЕ', link: '/favorites'},
      ]
    }
  },
  methods: {
    getStyle(itemLink){
      
      if (this.$route.path === itemLink) {
        return {
          'background': '#B8D86B',
          'border-radius': '25px',
          'font-weight': '500',
        }
      }
    }
  }

}
</script>

<style scoped>

.sidebar_menu{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100vh;
  border-right: 1px solid grey;
  width: fit-content;

}
.menu_list{
  list-style-type: none;
  display: flex;
  flex-direction: column;

}
.menu_item, .menu_profile{
  border-bottom: 1px solid grey;
  /* padding: 10px 15px; */
}
.menu_link{
  padding: 10px 15px;
  display: block;
  color: black;
}
.menu_link:hover{
  background-color: #B8D86B;
  border-radius: 25px;
  color: black;
  font-weight: 500;
}
.menu_profile{
  padding: 20px 15px;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
}
.profile_picture{
  width: 45px;
  display: block;
}


</style>