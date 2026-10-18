from django.urls import path

from . import views 
from .models import Category



urlpatterns = [
    path('<int:category_id>/', views.posts_by_category, name='posts_by_category'),
]
