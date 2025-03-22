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