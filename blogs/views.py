from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

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


def singleblog(request , slug):
    singleblog = get_object_or_404(Blog , slug = slug , status = "Published")
    context = {
        "singleblog" : singleblog
    }
    return render(request , "singleblog.html" , context)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})


def login(request):
    redirect_to = request.POST.get("next", request.GET.get("next", ""))
    if request.user.is_authenticated:
        if not url_has_allowed_host_and_scheme(
            redirect_to,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            redirect_to = "home"
        return redirect(redirect_to)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            if not url_has_allowed_host_and_scheme(
                redirect_to,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                redirect_to = "home"
            return redirect(redirect_to)
    else:
        form = AuthenticationForm(request)

    return render(request, "login.html", {"form": form, "next": redirect_to})


@require_POST
def logout(request):
    auth_logout(request)
    return redirect("home")


def search(request):
    keywords = request.GET.get("keywords", "").strip()
    blog = Blog.objects.none()
    if keywords:
        blog = Blog.objects.filter(
            Q(title__icontains=keywords)
            | Q(blog_body__icontains=keywords)
            | Q(short_description__icontains=keywords),
            status="Published",
        ).order_by("-created_at")

    context = {
        "categories": Category.objects.all(),
        "keywords": keywords,
        "blog": blog,
    }
    return render(request, "search.html", context)