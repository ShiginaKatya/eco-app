<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu :burgerMenu="openingMenu" @close="closeMenu()"></ProfileMenu>
    </aside>
    <main class="main">
      <section class="main_header"> 
        <h1 class="header_title">Мероприятия</h1>
      </section>
      <section class="main_sections">
        <button class="eco-button" @click="openEventModal" @close="closeModal">Добавить мероприятие</button>
        <AddEvent v-if="showModal" :user="user" @close="closeModal"></AddEvent>
        <ul class="events_list">
          <li class="event" v-for="event in events" :key="event.id">
            <img class="event_image" :src="event.afisha_image" alt="">
            <p class="event_title">{{ event.title }}</p>
            <p class="event_date">{{ event.event_date }}</p>
            <p class="event_text">{{ event.description }}</p>
            <p class="event_status">{{ event.status }}</p>
            <AddReport v-if="eventUrl === event.url" :event="event" @close="closeModal"></AddReport>
            <div class="button_group">
              <button v-if="event.report" @click="openReportModal(event.url)" class="eco-button">Отчет</button>
              <button v-else class="eco-button" @click="openAddReportModal(event.url)">Добавить отчет</button>
              <button @click="openChangeModal(event.url)" class="eco-button change">Изменить</button>
              <AddEvent v-if="eventChangeUrl === event.url" :user="user" :event="event" @close="closeModal"></AddEvent>
              <DetailReport v-if="eventReportUrl === event.url"  :event="event" @close="closeModal"></DetailReport>
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
import { onMounted, computed } from 'vue';
import axiosInstance from '../http.js'
import axios from 'axios'
import AddEvent from '../components/AddEvent.vue';
import AddReport from '../components/AddReport.vue';
import DetailReport from '../components/DetailReport.vue';

const user = computed(() => store.state.user) 
const events = computed(() => store.state.events)


export default {
    components: {
      ProfileMenu,
      AddEvent,
      AddReport,
      DetailReport
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
        eventUrl: null,
        eventChangeUrl: null,
        eventReportUrl: null
       
      }
    },
    computed:{
     
    },
    methods: {
      openEventModal(){
        this.showModal = true


      },
      openAddReportModal(event){
        this.eventUrl = event

      },
      openChangeModal(event){
        this.eventChangeUrl = event
      },
      openReportModal(event){
        this.eventReportUrl = event
      },
      closeModal() {
        this.showModal = false
        this.eventUrl = null
        this.eventChangeUrl = null
        this.eventReportUrl = null
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

.events_list{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
@media  screen and (max-width: 1024px) and (min-width: 450px) {
  .events_list{
    grid-template-columns: repeat(2, 1fr);
  }
}
@media  screen and (max-width: 450px){
  .events_list{
    grid-template-columns: 1fr;
  }
}

.button_group{
  display: flex;
  justify-content: space-between;
}
.change{
  background-color: white;
  border: 1px solid lightgray;
}
.event{
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  border: 1px solid lightgray;
  border-radius: 8px;
  height: fit-content;
}
.event_title{
  font-weight: 500;
  font-family: Golos Text, sans-serif;
  font-size: 16px;
}
.event_date{
  color: #2E8B57;
  padding: 4px;
  border: 1px solid #2E8B57;
  border-radius: 8px;
  width: fit-content;
}
.event_image{
  display: block;
  margin: 0 auto;
  width: 100%;
  border-radius: 4px;
}


</style>