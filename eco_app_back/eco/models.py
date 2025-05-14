from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db import connection
from django.utils import timezone
from datetime import timedelta
# import random
# import uuid


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
    want_organization = models.BooleanField(verbose_name='Заявка на организацию', default=False)
    # is_email_confirmed = models.BooleanField(default=False)
    # email_confirmation_token = models.CharField(default=uuid.uuid4, editable=False, max_length=255)

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
    this_day = models.BooleanField(verbose_name='Привычка недели', default=False)

    class Meta:
        verbose_name = 'Эко-привычка'
        verbose_name_plural = 'Эко-привычки'

    def __str__(self):
        return self.title
    
class FormQuestion(models.Model):
    title = models.CharField(verbose_name='Вопрос', max_length=255)
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.title

class Form(models.Model):
    title = models.CharField(verbose_name='Анкета', max_length=255)
    questions = models.ManyToManyField(verbose_name='Вопросы', to=FormQuestion)

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'

    def __str__(self):
        return self.title

class UserAnswer(models.Model):
    answer = models.CharField(verbose_name='Ответ', max_length=255)
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)
    question = models.ForeignKey(verbose_name='Вопрос', to=FormQuestion, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'

    def __str__(self):
        return self.anwser

class UserPlan(models.Model):
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.PROTECT)
    goal = models.CharField(verbose_name='Цель', max_length=255)
    form = models.ForeignKey(verbose_name='Анкета', to=Form, on_delete=models.PROTECT, null=True)
    status = models.BooleanField(verbose_name='Статус выполнения', default=False)
    is_done = models.BooleanField(verbose_name='Статус завершения', default=False)

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
    icon = models.ImageField(verbose_name='Иконка награды', upload_to='achievements', null=True)
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
    achievement = models.ForeignKey(verbose_name='Награда', to=Achievement, on_delete=models.PROTECT, null=True)
    category = models.ForeignKey(verbose_name='Категория', to=Category, on_delete=models.PROTECT, null=True)
    start_date = models.DateField(verbose_name='Дата начала', null=True)
    finish_date = models.DateField(verbose_name='Дата окончания', null=True)
    status = models.BooleanField(verbose_name='Доступен', default=True)
    tasks = models.ManyToManyField(verbose_name='Задания', to=Task, related_name='challenges')
    this_week = models.BooleanField(verbose_name='Челлендж недели', default=False)
    this_week_date = models.DateTimeField(null=True, blank=True)
    
    def get_effective_status(self):
        if self.this_week:
            if self.this_week_date:
                if timezone.now() - self.this_week_date >= timedelta(weeks=1):
                    self.this_week = False
                    self.this_week_date = None
                    self.save(update_fields=['this_week', 'this_week_date'])
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False

    class Meta:
        verbose_name = 'Челлендж'
        verbose_name_plural = 'Челленджи'

    def __str__(self):
        return self.title
    
    # @property
    # def format_date(self):
    #     return self.start_date.stfftime('%d.%m.%Y')

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
    user = models.OneToOneField(verbose_name='Пользователь', to=User, on_delete=models.CASCADE, unique=True)
    points = models.PositiveIntegerField(verbose_name='Баллы', default=0)
    level = models.ForeignKey(verbose_name='Уровень', to=Level, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = 'Статистика пользователя'
        verbose_name_plural = 'Статистика пользователей'

    def __str__(self):
        return self.user.username

    @property
    def achievements_count(self):
        return UserAchievement.objects.filter(user=self.user).count()
    
    @property
    def all_achievements(self):
        achievement_stat = []
        user_achievements = UserAchievement.objects.filter(user=self.user)
        achievements_types = Achievement.objects.all()
        for achievement_type in achievements_types:
            user_count = user_achievements.filter(achievement = achievement_type).count()
            if user_count > 0:
                achievement_stat.append({'achievement': achievement_type, 'count': user_count })
        return achievement_stat
    
    @property
    def completed_plans(self):
        return UserPlan.objects.filter(user=self.user, status=True).count()
    
    @property
    def next_level(self):
        return Level.objects.filter(id=self.level.id + 1).first()
    


@receiver(pre_save, sender=UserStat) 
def determine_level(sender, instance, **kwargs):
    levels = Level.objects.all()
    for level in levels:
        if (level.min_points <= instance.points):
            instance.level = level

# @receiver(pre_save, sender=UserPlan)
# def determine_form(sender, instance, **kwargs):
#     if not created:
#         forms = Form.objects.all()
#         instance.form = random.choice(forms)

class Advice(models.Model):
    title = models.CharField(verbose_name='Cовет', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True)
    icon = models.ImageField(verbose_name='Иконка совета', upload_to='advices', null=True)
    category = models.ForeignKey(verbose_name='Категория', to=Category, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(verbose_name='Автор', to=User, on_delete=models.CASCADE, null=True)
    is_posted = models.BooleanField(verbose_name='Выложен', default=True)

    class Meta:
        verbose_name = 'Совет'
        verbose_name_plural = 'Советы'

    def __str__(self):
        return self.title

# @receiver(post_save, sender=Advice)
# def update_fts(sender, instance, **kwargs):
#     with connection.cursor() as cursor:
#         cursor.execute("DELETE FROM advice_search WHERE rowid = %s", [instance.id])
#         cursor.execute(
#             "INSERT INTO advice_search (rowid, title, description) VALUES (%s, %s, %s)",
#             [instance.id, instance.title, instance.description]
#         )

# @receiver(post_delete, sender=Advice)
# def delete_fts(sender, instance, **kwargs):
#     with connection.cursor() as cursor:
#         cursor.execute("DELETE FROM advice_search WHERE rowid = %s", [instance.id])

class Guide(models.Model):
    title = models.CharField(verbose_name='Руководство', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True)
    annotation = models.TextField(verbose_name='Важное', null=True)
    icon = models.ImageField(verbose_name='Изображение для руководства', upload_to='guides')
    category = models.ForeignKey(verbose_name='Категория', to=Category, on_delete=models.CASCADE)
    is_posted = models.BooleanField(verbose_name='Выложен', default=True)
    author = models.ForeignKey(verbose_name='Автор', to=User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Руководство'
        verbose_name_plural = 'Руководства'

    def __str__(self):
        return self.title


class Favorite(models.Model):
    FAVORITE_CHOICE = [
        ('A', 'Совет'),
        ('G', 'Руководство')
    ]
    
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)
    advice = models.ForeignKey(verbose_name='Совет', to=Advice, on_delete=models.CASCADE, null=True)
    guide = models.ForeignKey(verbose_name='Руководство', to=Guide, on_delete=models.CASCADE, null=True)
    favorite_type = models.CharField(verbose_name='Тип', choices=FAVORITE_CHOICE, max_length=255)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное пользователей'

    def __str__(self):
        return self.user.username

class Event(models.Model):
    STATUS_CHOICE = [
        ('Назначено', 'Назначено'),
        ('Перенесено', 'Перенесено'),
        ('Завершено', 'Завершено'),
        ('Отменено', 'Отменено')

    ]
    title = models.CharField(verbose_name='Название мероприятия', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True)
    afisha_image = models.ImageField(verbose_name='Изображение для объявления', upload_to='events', null=True)
    event_date = models.DateField(verbose_name='Дата мероприятия')
    report = models.TextField(verbose_name='Отчет о прохождении', null=True)
    report_image = models.ImageField(verbose_name='Изображение для отчета', upload_to='reports', null=True)
    status = models.CharField(verbose_name='Статус мероприятия', choices=STATUS_CHOICE, default='Назначено', max_length=255)
    user = models.ForeignKey(verbose_name='Организатор мероприятия', to=User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        return self.title

class UserGroup(models.Model):
    title = models.CharField(verbose_name='Название группы', max_length=255)

    class Meta:
        verbose_name = 'Группа пользователей'
        verbose_name_plural = 'Группы пользователей'

    def __str__(self):
        return self.title

class GroupMember(models.Model):
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(verbose_name='Группа', to=UserGroup, on_delete=models.CASCADE, related_name='members', null=True)
    is_confirm = models.BooleanField(verbose_name='Потверждение', default=False)

    class Meta:
        verbose_name = 'Участник группы'
        verbose_name_plural = 'Участники группы'

    def __str__(self):
        return self.user.username
    
    @property
    def member_stat(self):
       return UserStat.objects.filter(user=self.user)
