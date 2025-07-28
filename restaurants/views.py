from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Restaurant, Category, Review, Favorite

class IndexView(ListView):
    model = Restaurant
    template_name = 'restaurants/index.html'
    context_object_name = 'restaurants'
    paginate_by = 12

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        
        # 検索機能
        keyword = self.request.GET.get('keyword')
        category_id = self.request.GET.get('category')
        
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | 
                Q(description__icontains=keyword) |
                Q(address__icontains=keyword)
            )
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['keyword'] = self.request.GET.get('keyword', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/detail.html'
    context_object_name = 'restaurant'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.get_object()
        
        # レビュー情報を取得
        reviews = Review.objects.filter(restaurant=restaurant).order_by('-created_at')
        context['reviews'] = reviews
        
        # 平均評価を計算
        avg_score = reviews.aggregate(Avg('rating'))['rating__avg']
        context['avg_score'] = round(avg_score, 1) if avg_score else 0
        context['review_count'] = reviews.count()
        
        # ユーザーがログインしている場合、お気に入り状態をチェック
        if self.request.user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(
                user=self.request.user, 
                restaurant=restaurant
            ).exists()
        
        return context


@require_POST
@login_required
def toggle_favorite(request, restaurant_id):
    """お気に入りの追加・削除をAjaxで処理"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        restaurant=restaurant
    )
    
    if not created:
        # 既に存在する場合は削除
        favorite.delete()
        is_favorite = False
        message = 'お気に入りから削除しました'
    else:
        # 新規作成の場合
        is_favorite = True
        message = 'お気に入りに追加しました'
    
    return JsonResponse({
        'is_favorite': is_favorite,
        'message': message
    })


class FavoriteListView(LoginRequiredMixin, ListView):
    """お気に入り一覧ページ"""
    model = Favorite
    template_name = 'restaurants/favorite_list.html'
    context_object_name = 'favorites'
    paginate_by = 12
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('restaurant').order_by('-created_at')