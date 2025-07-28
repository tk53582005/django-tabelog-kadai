from django.shortcuts import render
from django.views.generic import ListView
from .models import Restaurant, Category

class IndexView(ListView):
    """トップページ"""
    model = Restaurant
    template_name = 'restaurants/index.html'
    context_object_name = 'restaurants'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context