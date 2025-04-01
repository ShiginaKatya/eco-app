from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        UserStat.objects.create(user=self)


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
    habit = models.ForeignKey(verbose_name='Эко-привычка', to=Habit, on_delete=models.CASCADE, )
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
    
class Task(models.Model):
    title = models.CharField(verbose_name='Задание', max_length=255)

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.title

class Challenge(models.Model):
    title = models.CharField(verbose_name='Название челленджа', max_length=255)
    goal = models.CharField(verbose_name='Цель', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True)
    achievement = models.ForeignKey(verbose_name='Награда', to=Achievement, on_delete=models.PROTECT)
    category = models.ForeignKey(verbose_name='Категория', to=Category, on_delete=models.PROTECT)
    start_date = models.DateField(verbose_name='Дата начала', null=True)
    finish_date = models.DateField(verbose_name='Дата окончания', null=True)
    status = models.BooleanField(verbose_name='Доступен', default=True)
    tasks = models.ManyToManyField(verbose_name='Задания', to=Task)

    class Meta:
        verbose_name = 'Челлендж'
        verbose_name_plural = 'Челленджи'

    def __str__(self):
        return self.title

class UserChallenge(models.Model):
    challenge = models.ForeignKey(verbose_name='Челлендж', to=Challenge, on_delete=models.PROTECT)
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.PROTECT)
    status = models.BooleanField(verbose_name='Статус выполнения', default=False)

    class Meta:
        verbose_name = 'Челлендж пользователя'
        verbose_name_plural = 'Челленджи пользователей'

    def __str__(self):
        return self.challenge.title

class UserTask(models.Model):
    task = models.ForeignKey(verbose_name='Задание', to=Task, on_delete=models.PROTECT)
    status = models.BooleanField(verbose_name='Статус выполнения', default=False)
    challenge = models.ForeignKey(verbose_name='Челлендж', to=UserChallenge,  related_name='tasks', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Задание пользователя'
        verbose_name_plural = 'Задания пользователей'

    def __str__(self):
        return self.task.title

class Level(models.Model):
    title = models.CharField(verbose_name='Название уровня', max_length=255)
    description = models.TextField(verbose_name='Описание уровня', null=True)
    min_points = models.PositiveIntegerField(verbose_name='Минимальное кол-во баллов')

    class Meta:
        verbose_name = 'Уровень'
        verbose_name_plural = 'Уровни'

    def __str__(self):
        return self.title

class UserStat(models.Model):
    user = models.OneToOneField(verbose_name='Пользователь', to=User, on_delete=models.PROTECT)
    points = models.PositiveIntegerField(verbose_name='Баллы', default=0)
    level = models.ForeignKey(verbose_name='Уровень', to=Level, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = 'Статистика пользователя'
        verbose_name_plural = 'Статистика пользователей'

    def __str__(self):
        return self.user.username
    
    @property
    def all_achievements(self):
        return UserAchievement.objects.filter(user=self.user)
    
    @property
    def completed_plans(self):
        return UserPlan.objects.filter(user=self.user, status=True).count()
    


@receiver(pre_save, sender=UserStat) 
def determine_level(sender, instance, **kwargs):
    levels = Level.objects.all()
    for level in levels:
        if (level.min_points <= instance.points):
            instance.level = level

