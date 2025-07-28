from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """カスタムユーザーモデル"""
    
    # メールアドレスでログイン
    email = models.EmailField('メールアドレス', unique=True)
    
    # 基本情報
    first_name = models.CharField('名', max_length=30)
    last_name = models.CharField('姓', max_length=30)
    phone_number = models.CharField('電話番号', max_length=15, blank=True)
    
    # 有料会員関連
    is_premium = models.BooleanField('有料会員フラグ', default=False)
    stripe_customer_id = models.CharField('Stripe顧客ID', max_length=100, blank=True)
    
    # タイムスタンプ
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    # メールアドレスをユーザー名として使用
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = '会員'
        verbose_name_plural = '会員'
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    def get_full_name(self):
        """フルネームを返す"""
        return f"{self.last_name} {self.first_name}"