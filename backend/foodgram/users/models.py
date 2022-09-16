from django.db import models
from django.contrib.auth.models import AbstractUser

# ВЫПОЛНЕНО!
class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    ROLE = [
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]

    username = models.TextField(
        verbose_name='Имя пользователя', 
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True
    )
    first_name = models.TextField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = models.TextField(
        verbose_name='Фамилия',
        max_length=150
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=100,
        choices=ROLE,
        default=USER
    )
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN
