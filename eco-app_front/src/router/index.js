import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../pages/MainPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import LoginPage from '../pages/LoginPage.vue'
import HabitPage from '../pages/HabitPage.vue'
import ChallengePage from '../pages/ChallengePage.vue'
import ProgressPage from '../pages/ProgressPage.vue'


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
      { path: '/', component: MainPage },
      { path: '/register', component: RegisterPage },
      { path: '/login', component: LoginPage },
      { path: '/habits', component: HabitPage },
      { path: '/challenges', component: ChallengePage },
      { path: '/statistic', component: ProgressPage},
    ]
    })

export default router