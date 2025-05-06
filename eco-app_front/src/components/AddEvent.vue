<template>
  <div class="modal">
    <div class="modal_title">
      <p class="title">Добавить мероприятие</p>
      <button  class="close" @click="closeModal"></button>
    </div>
    <form class="modal_form" >
      <label class="modal_text" for="title">Название</label>
      <input class="modal_input" v-model="title" type="text"/>
      <label class="modal_text" for="description">Описание</label>
      <input class="modal_input" v-model="description" type="text"/>
      <label class="modal_text">Добавьте афишу к мероприятию</label>
      <input type="file" class="eco-button" @change="addAfisha"/>
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
      user: Object
    },
    data () {
      return {
        title: '',
        description: '', 
        afisha_file: '',
        event_date: '',
    }},
    methods: {
      closeModal() {
        this.$emit('close'); 
      },
      addAfisha(event) {
        const file = event.target.files[0];
        this.afisha_file = file;
      },
      async addEvent(){
        const eventData = new FormData(); 
        eventData.append('user', this.user.url); 
        eventData.append('title', this.title);
        eventData.append('event_date', this.event_date);
        eventData.append('afisha_image', this.afisha_file);
        eventData.append('status', 'Назначено');
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
  padding: 12px 16px;
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
  padding: 10px 0;
  justify-content: center;
  align-items: left;
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
.modal_input-multi{
  color: black;
  font-size: 14px;
}

.modal_text{
  font-size: 12px;
  color: grey;
  font-weight: 500;
  padding-top: 8px ;
  padding-bottom: 4px;
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
  margin: 10px auto;
}
.habits{
  margin-top: 6px;
  padding: 4px;
  border: 1px solid #C5FDC5;
  border-radius: 4px;

}

</style>
