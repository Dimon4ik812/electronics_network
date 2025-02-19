from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomsUser(AbstractUser):
    username = None

    email = models.EmailField(unique=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return self.email
