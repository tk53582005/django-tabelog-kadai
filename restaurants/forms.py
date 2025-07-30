from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta, time
from .models import Review, Reservation


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i}つ星') for i in range(1, 6)],
                attrs={
                    'class': 'form-select',
                    'id': 'rating-select'
                }
            ),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'こちらのお店の感想をお聞かせください...\n\n例：\n・料理の味について\n・サービスについて\n・雰囲気について\n・おすすめメニュー',
                'maxlength': 1000
            })
        }
        labels = {
            'rating': '評価',
            'comment': 'レビュー内容'
        }
    
    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment.strip()) < 10:
            raise forms.ValidationError('レビューは10文字以上で入力してください。')
        return comment
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not rating or rating < 1 or rating > 5:
            raise forms.ValidationError('評価は1〜5の範囲で選択してください。')
        return rating


class ReservationForm(forms.ModelForm):
    # 30分刻みの時間選択肢を生成
    TIME_CHOICES = []
    start_hour = 18  # 営業開始時間を18:00に変更
    end_hour = 21    # 最終受付時間
    
    for hour in range(start_hour, end_hour + 1):
        for minute in [0, 30]:
            if hour == end_hour and minute > 0:
                break  # 21:30は含まない（21:00まで）
            time_obj = time(hour, minute)
            time_str = time_obj.strftime('%H:%M')
            TIME_CHOICES.append((time_str, time_str))
    
    reservation_time = forms.ChoiceField(
        choices=TIME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='予約時間'
    )
    
    class Meta:
        model = Reservation
        fields = ['reservation_date', 'reservation_time', 'number_of_people']
        widgets = {
            'reservation_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': timezone.now().date().strftime('%Y-%m-%d')
            }),
            'number_of_people': forms.Select(
                choices=[(i, f'{i}名') for i in range(1, 11)],
                attrs={'class': 'form-select'}
            )
        }
        labels = {
            'reservation_date': '予約日',
            'number_of_people': '人数'
        }
    
    def clean_reservation_date(self):
        reservation_date = self.cleaned_data.get('reservation_date')
        
        if not reservation_date:
            raise ValidationError('予約日を選択してください。')
        
        # 本日以降の日付のみ許可
        if reservation_date < timezone.now().date():
            raise ValidationError('本日以降の日付を選択してください。')
        
        # 3ヶ月先まで予約可能
        max_date = timezone.now().date() + timedelta(days=90)
        if reservation_date > max_date:
            raise ValidationError('予約は3ヶ月先まで可能です。')
        
        return reservation_date
    
    def clean_reservation_time(self):
        reservation_time_str = self.cleaned_data.get('reservation_time')
        
        if not reservation_time_str:
            raise ValidationError('予約時間を選択してください。')
        
        try:
            # 文字列をtimeオブジェクトに変換
            reservation_time = datetime.strptime(reservation_time_str, '%H:%M').time()
        except ValueError:
            raise ValidationError('正しい時間形式を選択してください。')
        
        # 営業時間チェック（18:00-21:00）
        if reservation_time < time(18, 0):
            raise ValidationError('営業時間は18:00からです。')
        
        if reservation_time > time(21, 0):
            raise ValidationError('最終受付は21:00です。')
        
        # timeオブジェクトを返す
        return reservation_time
    
    def clean(self):
        cleaned_data = super().clean()
        reservation_date = cleaned_data.get('reservation_date')
        reservation_time_str = cleaned_data.get('reservation_time')
        
        if reservation_date and reservation_time_str:
            try:
                # もしstringならtimeオブジェクトに変換
                if isinstance(reservation_time_str, str):
                    reservation_time = datetime.strptime(reservation_time_str, '%H:%M').time()
                else:
                    reservation_time = reservation_time_str
                
                # 本日の場合、現在時刻より後の時間のみ許可
                if reservation_date == timezone.now().date():
                    current_time = timezone.now().time()
                    if reservation_time <= current_time:
                        raise ValidationError('本日の予約は現在時刻より後の時間を選択してください。')
                
            except ValueError:
                raise ValidationError('正しい時間形式を選択してください。')
        
        return cleaned_data