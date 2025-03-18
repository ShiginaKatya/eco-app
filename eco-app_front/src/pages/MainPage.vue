<template>
    <div>
        <header class="main_header">
            <nav class="header_menu">
                <div class="logo">
                    <img src="" alt="">
                </div>
                <ul class="menu_list">
                    <li class="menu_list_item">О сервисе</li>
                    <li class="menu_list_item">Советы</li>
                    <li class="menu_list_item">Эко-привычки</li>
                </ul>
                <router-link to="/register">Зарегистрироваться</router-link>
            </nav>
        </header>
        <main class="main_section">
            <section>
                <h1></h1>
                <p></p>
                <router-link to="/register">Зарегистрироваться</router-link>
            </section>
            <section class="advice_block">
                <h2 class="advice_block_title"></h2>
                <ul class="advices_list">
                    <li class="advices_item"></li>
                    <li class="advices_item"></li>
                    <li class="advices_item"></li>
                </ul>
            </section>
        </main>
        <footer class="main_footer">
        </footer> 
    </div>
</template>