from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser
from .forms import UserProfileForm


class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/mypage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # お気に入り店舗を取得
        from restaurants.models import Favorite
        context['favorite_restaurants'] = Favorite.objects.filter(user=user).select_related('restaurant')[:5]
        
        # 最近のレビューを取得（後で実装）
        # context['recent_reviews'] = user.review_set.all()[:5]
        
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:mypage')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'プロフィールを更新しました。')
        return super().form_valid(form)


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # セッションを維持
            messages.success(request, 'パスワードを変更しました。')
            return redirect('accounts:mypage')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/password_change.html', {'form': form})