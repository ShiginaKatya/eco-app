<template>
    <div class="main_page">
        <header class="page_header">
            <nav class="header_menu">
                <div class="logo">
                    <!-- <img src="" alt=""> -->
                    <p class="logo_text">ECO GREEN LIFE</p>
                </div>
                <ul class="menu_list">
                    <li class="menu_list_item">О сервисе</li>
                    <li class="menu_list_item">Советы</li>
                    <li class="menu_list_item">Эко-привычки</li>
                </ul>
                <router-link to="/register" class="eco-button">Зарегистрироваться</router-link>
            </nav>
        </header>
        <main class="main_section">
            <section class="main_banner">
                <h1 class="main_banner_title">Eco Green Life</h1>
                <p class="main_banner_text">Новый подход для поддежки экологичного образа жизни и осознанного потребления</p>
                <router-link to="/register" class="eco-button">Присоединиться</router-link>
            </section>
            <section class="advice_block">
                <h2 class="advice_block_title">Советы</h2>
                <ul class="advices_list">
                    <li class="advices_item">
                        <p class="advices_title">Используйте многоразовую посуду</p>
                        <p class="advices_text">Для того, чтобы избежать накопления пластиковой посуды, необходимо перейти на многоразовую. Например, стеклянная бутылка для воды, силиконовая кружка для кофе.</p>
                        <img src="/advice_icon.svg" alt="" class="advices_icon">
                    </li>
                    <li class="advices_item">
                        <p class="advices_title">Используйте многоразовую посуду</p>
                        <p class="advices_text">Для того, чтобы избежать накопления пластиковой посуды, необходимо перейти на многоразовую. Например, стеклянная бутылка для воды, силиконовая кружка для кофе.</p>
                        <img src="/advice_icon.svg" alt="" class="advices_icon">
                    </li>
                    <li class="advices_item">
                        <p class="advices_title">Используйте многоразовую посуду</p>
                        <p class="advices_text">Для того, чтобы избежать накопления пластиковой посуды, необходимо перейти на многоразовую. Например, стеклянная бутылка для воды, силиконовая кружка для кофе.</p>
                        <img src="/advice_icon.svg" alt="" class="advices_icon">
                    </li>
                </ul>
            </section>
            <section class="habit_block">
                <h2 class="habit_block_title">Формируй эко-привычки вместе с ECO Green Life</h2>
                <div class="habit_group">
                    <p class="habit_block_text">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                    <p class="habit_block_text">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                    <router-link to="/login" class="eco-button">Перейти</router-link>
                </div>
            </section>
            <section class="about_block">
                <p class="about_block_text">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                <router-link to="/register" class="eco-button">Зарегистрироваться</router-link>
            </section>
        </main>
        <footer class="main_footer">
            <nav class="footer_menu">
                <div class="logo">
                    <!-- <img src="" alt=""> -->
                    <p class="logo_text">ECO GREEN LIFE</p>
                </div>
                <ul class="menu_list">
                    <li class="menu_list_item">О сервисе</li>
                    <li class="menu_list_item">Советы</li>
                    <li class="menu_list_item">Эко-привычки</li>
                </ul>
            </nav>
        </footer> 
    </div>
</template>

<script setup>
import { useHead } from '@vueuse/head'

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "ECO Green Free Экологическое веб-приложение",
  "description": "Формирование и поддержка пути к экологичному образу жизни и осознанному потреблению",
  "url": "https://example.com/my-awesome-page"
}

useHead({
  title: 'ECO Green Free Экологическое веб-приложение',
  meta: [
    { property: 'og:title', content: 'ECO Green Free Экологическое веб-приложение' },
    { property: 'og:description', content: 'Формирование и поддержка пути к экологичному образу жизни и осознанному потреблению' },
    { property: 'og:type', content: 'website' },
    { property: 'og:image', content: 'https://example.com/images/awesome.jpg' }
  ],
  script: [
    {
      type: 'application/ld+json',
      children: JSON.stringify(jsonLd)
    }
  ]
})
</script>

<style scoped>
.main_page{
    margin: 0 auto;
    max-width: 1200px;
    min-width: 320px;
    display: grid;
    gap: 16px;
    padding: 16px;
}

.header_menu, .footer_menu{
    display: flex;
    justify-content: space-between;
    border: 1px solid lightgrey;
    border-radius: 8px;
    align-items: center;
    padding: 16px;

}
ul{
    list-style-type: none;
}

.menu_list{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 32px;
}
.main_banner{
    background-image: url("/banner_1.jpg");
    height: 500px;
    background-position: center; 
    background-repeat: no-repeat; 
    background-size: cover;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    justify-content: end;
    gap: 2em;
    padding: 2em;
}
.main_banner_title{
    color: white;
    font-weight: bold;
}
.main_banner_text{
    color: white;
    font-weight: 400;
    max-width: 400px;
    font-size: 24px;
}
/* .eco-button{
    color: black;
    display: block;
    padding: 8px 16px;
    text-align: center;
    background-color: #;
    border-radius: 8px;
    width: fit-content;
    font-size: 14px;
    font-family: "Golos Text", sans-serif;
    font-weight: normal;
} */
.advices_list{
    display: flex;
    justify-content: space-between;
    gap: 2em;
    
}

.advices_item{
    display: flex;
    flex-direction: column;
    gap: 20px;
    border: 1px solid grey;
    padding: 20px;
    justify-content: space-between;
    border-radius: 25px;
    align-items: left;
}
.advices_icon{
    max-width: 100px;
    display: block;
    margin-left: 65%;
}
.advices_title{
    font-family: "Golos Text", sans-serif;
    font-size: 18px;
}
.advice_block_title, .habit_block_title{
    font-family: "Golos Text", sans-serif;
    font-size: 26px;
    font-weight: bold;
    margin: 20px;
}
.habit_group{
    display: flex;
    flex-direction: column;
    background-image: url("/Frame 56.png");
    background-position: center; 
    background-repeat: no-repeat; 
    background-size: cover;
    gap: 20px;
    align-items: center;
    flex-wrap: wrap;
    max-width: 1200px;
    justify-content: center;
    margin: 20px;
    padding-top: 100px;
}

.habit_block_text, .about_block_text{
    max-width: 300px;
    text-align: center;
    

}
.about_block_text{
    color: white;
}
.about_block{
    display: flex;
    flex-direction: column;
    gap: 20px;
    align-items: center;
    flex-wrap: wrap;
    justify-content: center;
    max-height: 300px;
    background-color: #1E6B1A;
    padding: 2em;
    border-radius: 25px;
}
</style>
