<template>
    <div class="page">
        <aside class="sidebar">
            <ProfileMenu></ProfileMenu>
        </aside>
        <main class="main">
            <AddPlanModal v-if="showModal" @close="showModal = false"></AddPlanModal>
            <button class="eco-button" @click="openModal()">Создать план</button>
            <ul v-for="plan in plans" :key="plan.id">
                <li> {{plan.goal}}</li>
                <li v-for="habit in plan.habits" :key="habit.id">
                    <p>{{habit.habit.title}}</p>
                    <button @click="complete(habit.id)">Выполнить</button>
            </li>
          </ul>
        </main>
    </div>
</template>
<script>
import ProfileMenu from '../components/ProfileMenu.vue'
import AddPlanModal from '../components/AddPlan.vue'
import {store} from '../store.js'
import { onMounted, computed } from 'vue';
import axiosInstance from '../http.js'


const user = computed(() => store.state.user) 

const plans = computed(() => store.state.plans)

export default {
    components: {
      ProfileMenu,
      AddPlanModal,
    },
    setup() {
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
              
        }
        await axiosInstance
          .get('/userplans')
          .then(res => {
            console.log(res.data)
            store.commit('setPlans', res.data)
          })
          .catch((err) => {
            console.log(err)
        
          }) 
      })

    },
    data() {
      return {
        user: user,
        plans: plans,
        showModal: false,
      }
    },
    methods: {
        async complete(habitId){
          console.log(habitId)
          await axiosInstance
            .patch(`userhabits/${habitId}/`, {
              status: 'True'
            })
            .then((res) => {
              console.log(res.data)
            })  
            .catch((err) => {
              console.log(err)
            }) 

        },
        openModal(){
          this.showModal = true
        },
        closeModal() {
          this.isModalOpen = false;
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
}

</style>