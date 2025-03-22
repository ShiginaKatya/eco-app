import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../pages/MainPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import LoginPage from '../pages/LoginPage.vue'
import ProfilePage from '../pages/ProfilePage.vue'


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
      { path: '/', component: MainPage },
      { path: '/register', component: RegisterPage },
      { path: '/login', component: LoginPage },
      { path: '/profile', component: ProfilePage },
    ]
    })

export default router