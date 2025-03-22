<template>
    <nav class="sidebar_menu">
      <ul class="menu_list">
        <li class="menu_profile">
          <img src="" alt="картинка" class="profile_picture">
          <p class="profile_name">{{ user.username }}</p>
        </li>
        <li class="menu_item">
          <router-link to="/">ПРОГРЕСС</router-link>
        </li>
        <li class="menu_item">
          <router-link to="/">ЭКО-ПРИВЫЧКИ</router-link>
        </li>
        <li class="menu_item">
          <router-link to="/">ЧЕЛЛЕНДЖИ</router-link>
        </li>
        <li class="menu_item">
          <router-link to="/">СОВЕТЫ</router-link>
        </li>
        <li class="menu_item">
          <router-link to="/">РУКОВОДСТВА</router-link>
        </li>
        <li class="menu_item">
          <router-link to="/">ИЗБРАННОЕ</router-link>
        </li>
      </ul>
    </nav>
</template>

<script>
import { store } from '../store.js'
import { computed } from 'vue';

const user = computed(() => store.state.user)


export default {
  data() {
    return {
      user: user,
    }
  },}
</script>