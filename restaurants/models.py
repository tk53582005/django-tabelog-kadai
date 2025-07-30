from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Category(models.Model):
    """カテゴリモデル"""
    name = models.CharField('カテゴリ名', max_length=50, unique=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = 'カテゴリ'
        verbose_name_plural = 'カテゴリ'
    
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    """店舗モデル"""
    name = models.CharField('店舗名', max_length=100)
    description = models.TextField('説明', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='カテゴリ')
    
    # 住所・連絡先
    address = models.CharField('住所', max_length=200)
    phone_number = models.CharField('電話番号', max_length=15)
    
    # 営業時間・定休日
    opening_time = models.TimeField('開店時間')
    closing_time = models.TimeField('閉店時間')
    regular_holiday = models.CharField('定休日', max_length=100, blank=True)
    
    # 画像・URL
    image = models.ImageField('画像', upload_to='restaurants/', blank=True, null=True)
    website_url = models.URLField('ウェブサイトURL', blank=True)
    
    # タイムスタンプ
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = '店舗'
        verbose_name_plural = '店舗'
    
    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        """平均評価を取得"""
        reviews = self.review_set.all()
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0

class Review(models.Model):
    """レビューモデル"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='会員')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='店舗')
    
    rating = models.IntegerField(
        '評価',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField('コメント')
    
    # 追加フィールド
    is_approved = models.BooleanField('承認済み', default=True)
    helpful_count = models.PositiveIntegerField('役に立った数', default=0)
    
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = 'レビュー'
        verbose_name_plural = 'レビュー'
        unique_together = ['user', 'restaurant']  # 1人1店舗1レビュー
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.user.email} ({self.rating}★)"
    
    def get_star_display(self):
        """星の表示用"""
        return '★' * self.rating + '☆' * (5 - self.rating)

class Reservation(models.Model):
    """予約モデル"""
    STATUS_CHOICES = [
        ('confirmed', '確定'),
        ('cancelled', 'キャンセル'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='会員')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='店舗')
    
    # 予約情報
    reservation_date = models.DateField('予約日')
    reservation_time = models.TimeField('予約時間')
    number_of_people = models.IntegerField('人数', validators=[MinValueValidator(1)])
    status = models.CharField('ステータス', max_length=20, choices=STATUS_CHOICES, default='confirmed')
    
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
    class Meta:
        verbose_name = '予約'
        verbose_name_plural = '予約'
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.reservation_date} {self.reservation_time}"

class Favorite(models.Model):
    """お気に入りモデル"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='会員')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, verbose_name='店舗')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    
    class Meta:
        verbose_name = 'お気に入り'
        verbose_name_plural = 'お気に入り'
        unique_together = ['user', 'restaurant']  # 重複防止
    
    def __str__(self):
        return f"{self.user.email} - {self.restaurant.name}"