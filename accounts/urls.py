from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('password/change/', views.password_change_view, name='password_change'),
]