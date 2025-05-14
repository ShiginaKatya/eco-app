<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu :burgerMenu="openingMenu" @close="closeMenu()"></ProfileMenu>
    </aside>
    <main class="main">
      <AddEvent v-if="showModal" :user="user" @close="closeModal"></AddEvent>
      <ul>
        <li v-for="event in events" :key="event.id">
          <p>{{ event.title }}</p>
          <p>{{ event.description }}</p>
          <p>{{ event.event_date }}</p>
          <p>{{ event.status }}</p>
          <AddReport v-if="eventUrl === event.url" :event="event" @close="closeModal"></AddReport>
          <button class="eco-button" @click="openReportModal(event.url)">Добавить отчет</button>
        </li>
      </ul>
      <button class="eco-button" @click="openEventModal" @close="closeModal">Добавить мероприятие</button>
    </main>
  </div>
</template>

<script>
import ProfileMenu from '../components/ProfileMenu.vue'
import {store} from '../store.js'
import { onMounted, computed } from 'vue';
import axiosInstance from '../http.js'
import axios from 'axios'
import AddEvent from '../components/AddEvent.vue';
import AddReport from '../components/AddReport.vue';

const user = computed(() => store.state.user) 
const events = computed(() => store.state.events)


export default {
    components: {
      ProfileMenu,
      AddEvent,
      AddReport
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
        showModal: false,
        eventUrl: ''
       
      }
    },
    computed:{
     
    },
    methods: {
      openEventModal(){
        this.showModal = true
      },
      openReportModal(event){
        this.eventUrl = event
      },
      closeModal() {
        this.showModal = false
        this.eventUrl = null
        axiosInstance
          .get('/events')
          .then(res => {
            console.log(res.data)
            store.commit('setEvents', res.data)
          })
          .catch((err) => {
            console.log(err)
          }) 
      },
      
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