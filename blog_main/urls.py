
from django.contrib import admin
from django.urls import path , include
from . import views
from blogs import views as blogs_views


from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home , name = "home"),
    path('signup/', blogs_views.signup, name="signup"),
    path('signup', blogs_views.signup, name="signup"),
    path('login/', blogs_views.login, name="login"),
    path('login', blogs_views.login, name="login"),
    path('logout/', blogs_views.logout, name="logout"),
    path('logout', blogs_views.logout, name="logout"),
    path('category/', include('blogs.urls') , name = "category"),
    path('search', blogs_views.search , name="search"),
    path('<slug:slug>', blogs_views.singleblog , name = "singleblog"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
