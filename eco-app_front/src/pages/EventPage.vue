<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu></ProfileMenu>
    </aside>
    <main class="main">
      <ul>
        <li v-for="event in events" :key="event.id">
          <p>{{event.title}}</p>
          <p>{{event.description}}</p>
        </li>
      </ul>
      <input v-model="title" type="text">
      <input v-model="event_date" type="date">
      <button @click="addEvent">Добавить мероприятие</button>
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
const events = computed(() => store.state.events)


export default {
    components: {
      ProfileMenu,
    },
    setup() {
       onMounted(async () => {
        await axiosInstance
          .get('/events')
          .then(res => {
            console.log(res.data)
            store.commit('setEvents', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
       })
    },
    data() {
      return {
        user: user,
        events: events,
        title: '',
        event_date: ''
      }
    },
    computed:{
     
    },
    methods: {
      addEvent(){
        axiosInstance
          .post('events/', {
            user: this.user.url,
            title: this.title,
            event_date: this.event_date,
            status: 'A'
          })
          .then((res) => {
            console.log(res.data)
          })
          .catch((err) => {
            console.log(err)
          })
        axiosInstance
          .get('/events')
          .then(res => {
            console.log(res.data)
            store.commit('setEvents', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
      }
    }
}
</script>

<style scoped>
.page{
  display: flex;
}
.sidebar{
  width: fit-content;
}
.main{
  min-width: 320px;
  width: calc(100vw - 300px);
}

</style>