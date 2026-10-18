from django.shortcuts import get_object_or_404, render

from .models import Blog, Category


def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    context = {
        "categories": Category.objects.all(),
        "category": category,
        "category_posts": Blog.objects.filter(
            category=category,
            status="Published",
        ).order_by("-created_at"),
    }
    return render(request, "category_posts.html", context)
