<template>
  <div class="modal">
    <div class="modal_title">
      <p v-if="event" class="title">Изменить мероприятие</p>
      <p v-else class="title">Добавить мероприятие</p>
      <button  class="close" @click="closeModal"></button>
    </div>
    <form class="modal_form" >
      <label class="modal_text" for="title">Название</label>
      <input class="modal_input" v-model="title" type="text"/>
      <label class="modal_text" for="description">Описание</label>
      <input class="modal_input" v-model="description" type="text"/>
      <div v-if="event && event.afisha_image">
        <img :src="event.afisha_image" alt="Текущее изображение" style="max-width: 200px; max-height: 200px;">
      </div>
      <label v-if="event" class="modal_text">Изменить афишу к мероприятию</label>
      <label v-else class="modal_text">Добавьте афишу к мероприятию</label>
      <input type="file" class="input_file"  @change="addAfisha"/>
      <label class="modal_text" for="event_date">Дата проведения</label>
      <input class="modal_input" v-model="event_date" type="date"/>
      <button class="eco-button" @click.prevent="addEvent()">Добавить</button>
    </form>
  </div>
</template>
<script>
import axiosInstance from '../http.js'

export default {
    props: {
      user: Object,
      event: Object
    },
    data () {
      return {
        title: '',
        description: '', 
        afisha_file: '',
        event_date: '',
    }},
    created(){
      if (this.event){
        this.title = this.event.title
        this.description = this.event.description
        this.event_date = this.convertToISODate(this.event.event_date)
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
      addAfisha(event) {
        const file = event.target.files[0];
        this.afisha_file = file;
      },
      async addEvent(){
        const eventData = new FormData() 
        eventData.append('user', this.user.url)
        eventData.append('title', this.title)
        eventData.append('event_date', this.event_date)
        if (this.afisha_file){
          eventData.append('afisha_image', this.afisha_file)
        }
        if (this.event){
          await axiosInstance
            .patch(`events/${this.event.id}/`, eventData, {
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
        else{
          await axiosInstance
            .post('events/', eventData, {
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
        
        this.$emit('close')
      }
      
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
.input_file{
  font-family: "Raleway", sans-serif;
  font-size: 14px;
}
input::file-selector-button {
  color: black;
  padding: 8px 16px;
  text-align: center;
  background-color: #C5FDC5;
  border-radius: 8px;
  font-size: 14px;
  font-family: "Golos Text", sans-serif;
  font-weight: normal;
  border: none;
}



</style>
