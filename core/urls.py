"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from articles.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('about-us/', about_us, name="about_us"),
    path('contact-us/', contact_us, name="contact_us"),
    path('login/', login_page, name="login_page"),
    path('register/', register, name="register"),
    path('logout/', logout_page, name="logout_page"),
    path('add-article/', articles, name="articles"),
    path('show_published_articles/', show_published_articles, name="show_published_articles"),
    path('articles-list/', articles_list, name="articles_list"),
    path('delete-article/<id>/', delete_article, name="delete_article"),
    path('update-article/<id>/', update_article, name="update_article"),
    path('publish_articles/', publisher, name="publish_articles"),
    path('view_article/<id>/', view_article_to_be_published, name="view_article_to_be_published"),
    path('update_article_status/<article_id>/', update_article_status, name="update_article_status"),
    path('delete_user/<id>/', delete_user, name="delete_user"),
    path('view_users/', view_users, name="view_users"),
    path('home_articles/', home_articles, name="home_articles"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()