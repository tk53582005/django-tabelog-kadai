from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_premium = models.BooleanField(default=False)
    
    # 追加のプロフィールフィールド
    postal_code = models.CharField(max_length=8, blank=True, null=True, verbose_name='郵便番号')
    address = models.TextField(blank=True, null=True, verbose_name='住所')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='電話番号')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'
    
    def __str__(self):
        return self.email