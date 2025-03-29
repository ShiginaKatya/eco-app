from django.db import models

from django.contrib.auth.models import AbstractUser

from .managers import UserManager

class Role(models.Model):
    title = models.CharField(verbose_name='Роль', max_length=255)
    
    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.title
    

class User(AbstractUser):
    username = models.CharField(verbose_name='Имя', max_length=255)
    email = models.EmailField(verbose_name='Email', unique=True)
    role = models.ForeignKey(verbose_name='Роль', to=Role, on_delete=models.PROTECT, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.email

class Category(models.Model):
    title = models.CharField(verbose_name='Категория', max_length=255)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

class Habit(models.Model):
    title = models.CharField(verbose_name='Эко-привычка', max_length=255)
    category = models.ForeignKey(verbose_name='Категория', to=Category, on_delete=models.PROTECT, null=True)
    description = models.TextField(verbose_name='Описание', null=True)
    difficulty_level = models.PositiveIntegerField(verbose_name='Уровень сложности')
    
    class Meta:
        verbose_name = 'Эко-привычка'
        verbose_name_plural = 'Эко-привычки'

    def __str__(self):
        return self.title

class Form(models.Model):
    title = models.CharField(verbose_name='Анкета', max_length=255)
    
    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'

    def __str__(self):
        return self.title

class UserPlan(models.Model):
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.PROTECT)
    goal = models.CharField(verbose_name='Цель', max_length=255)
    form = models.ForeignKey(verbose_name='Анкета', to=Form, on_delete=models.PROTECT, null=True)
    status = models.BooleanField(verbose_name='Статус выполнения', default=False)

    class Meta:
        verbose_name = 'План'
        verbose_name_plural = 'Планы'

    def __str__(self):
        return self.goal


class UserHabit(models.Model):
    plan = models.ForeignKey(verbose_name='План', to=UserPlan, related_name='habits', on_delete=models.CASCADE)
    habit = models.ForeignKey(verbose_name='Эко-привычка', to=Habit, on_delete=models.PROTECT)
    status = models.BooleanField(verbose_name='Статус выполнения', default=False)

    class Meta:
        verbose_name = 'Привычка пользователя'
        verbose_name_plural = 'Привычки пользователей'

    def __str__(self):
        return self.habit.title

class Achievement(models.Model):
    title = models.CharField(verbose_name='Наименование награды', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True)
    icon = models.ImageField(verbose_name='Иконка награды', upload_to='achievements')
    points_required = models.PositiveIntegerField(verbose_name='Требуемые баллы')

    class Meta:
        verbose_name = 'Награда'
        verbose_name_plural = 'Награды'

    def __str__(self):
        return self.title

class UserAchievement(models.Model):
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.PROTECT)
    achievement = models.ForeignKey(verbose_name='Награда', to=Achievement, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Награда пользователя'
        verbose_name_plural = 'Награды пользователей'

    def __str__(self):
        return self.achievement.title

