<template>
  <div class="page">
    <aside class="sidebar">
      <ProfileMenu></ProfileMenu>
    </aside>
    <main class="main">
      <ul>
        <li v-for="advice in advices" :key="advice.id">
          <p>{{advice.title}}</p>
          <p>{{advice.description}}</p>
          <button @click="addFavorite(advice.url)">Избранное</button>
        </li>
      </ul>
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
const advices = computed(() => store.state.advices)


export default {
    components: {
      ProfileMenu,
    },
    setup() {
       onMounted(async () => {
        await axiosInstance
          .get('/advices')
          .then(res => {
            console.log(res.data)
            store.commit('setAdvices', res.data)
          })
          .catch((err) => {
            console.log(err)
          })
       })
    },
    data() {
      return {
        user: user,
        advices: advices
      }
    },
    computed:{
     
    },
    methods: {
      addFavorite(adviceUrl){
        axiosInstance
          .post('favorites/', {
            user: this.user.url,
            advice: adviceUrl,
            favorite_type: 'A'
          })
          .then((res) => {
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