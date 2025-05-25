<template>
  <div class="modal-guide">
    <div class="modal_title">
      <p class="title_text">{{ event.title }}</p>
      <button class="close" @click="closeModal"></button>
    </div>
    <p class="modal_text">Отчет</p>
    <p class="goal">{{ event.report }}</p>
    <img class="event_image" :src="event.report_image" alt="">
  </div>
</template>

<script>

export default {
  setup(){
    
  }, 
  props: {
    event: Object,
  },
  data () {
    return {
  }},
  methods: {
    closeModal() {
      this.$emit('close'); 
    },}}

</script>

<style scoped>
.modal-guide{
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
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;

}
.modal::-webkit-scrollbar {
    display: none; /* Для Chrome, Safari и Opera */
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
.tasks_list{
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.goal{
  font-weight: 500;
}
.task{
  padding: 8px;
  background-color: #F5F5DC;
  border-radius: 8px;
  width: fit-content;
  font-weight: 500;
}

.close{
  width: 14px;
  height: 14px;
  background-color: transparent;
  border: none;
  background-image: url('close.svg');
  background-size: cover;
}
.button{
  align-self: flex-end;
}
.category{
  color: #2E8B57;
  padding: 4px;
  border: 1px solid #2E8B57;
  border-radius: 8px;
  width: fit-content;
}
.date{
  color: #2E8B57;
  font-weight: 500;
}
.event_image{
  display: block;
  margin: 0 auto;
  width: 100%;
  border-radius: 4px;
}
</style>