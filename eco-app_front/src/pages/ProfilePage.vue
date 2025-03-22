<template>
    <div>
        <aside>
            <Menu></Menu>
        </aside>
    </div>
</template>
<script>
import Menu from '../components/Menu.vue'
import {store} from '../store.js'
import { onMounted, computed } from 'vue';
import axiosInstance, { API_URL } from '../http.js'

const user = computed(() => store.state.user) 

export default {
    components: {
      Menu,
    },
    setup() {
      onMounted(async () => {
        if (Object.keys(user.value).length === 0) {
          console.log(window.localStorage.getItem('userId'))
          await axiosInstance
            .get(`users/${window.localStorage.getItem('userId')}/`)
            .then(res => {
                console.log(res.data)
                store.commit('setUser', res.data)
              })
              .catch((err) => {
                console.log(err)
        
              })
              .finally(() => {
        })
        }
      })
    },
    data() {
        return {
            user: user
        }
    }
}
</script>