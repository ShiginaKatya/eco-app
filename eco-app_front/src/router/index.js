import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../pages/MainPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import LoginPage from '../pages/LoginPage.vue'
import HabitPage from '../pages/HabitPage.vue'
import ChallengePage from '../pages/ChallengePage.vue'
import ProgressPage from '../pages/ProgressPage.vue'
import AdvicePage from '../pages/AdvicePage.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import EventPage from '../pages/EventPage.vue'
import GuidePage from '../pages/GuidePage.vue'
import FavoritePage from '../pages/FavoritePage.vue'


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
      { path: '/', component: MainPage },
      { path: '/register', component: RegisterPage },
      { path: '/login', component: LoginPage },
      { path: '/habits', component: HabitPage },
      { path: '/challenges', component: ChallengePage },
      { path: '/statistic', component: ProgressPage},
      { path: '/advices', component: AdvicePage},
      { path: '/profile', component: ProfilePage},
      { path: '/event', component: EventPage},
      { path: '/guides', component: GuidePage},
      { path: '/favorites', component: FavoritePage},
    ]
    })

export default router