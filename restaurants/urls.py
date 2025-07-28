from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('restaurant/<int:pk>/', views.RestaurantDetailView.as_view(), name='detail'),
    path('favorite/toggle/<int:restaurant_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorite_list'),
]