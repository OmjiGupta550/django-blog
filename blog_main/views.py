from django.shortcuts import render
from blogs.models import Category , Blog

def home(request):
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True , status='Published')
    normal_posts = Blog.objects.filter(is_featured=False , status='Published')
    context={
        "categories" : categories ,
        "featured_posts" : featured_posts ,
        "normal_posts" : normal_posts,
    }
    return render(request , "home.html" , context)

