from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from articles.models import CustomUser

def home(request):
  articles = Article.objects.all()
  context = {'articles': articles}
  return render(request, 'home.html', context)

def about_us(request):
  return render(request, 'about_us.html')

def contact_us(request):
  return render(request, 'contact_us.html')

def login_page(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    if not CustomUser.objects.filter(username=username).exists():
      messages.error(request, 'Invalid Username or password')
      return redirect('/login/')

    user = authenticate(username=username, password=password)
    if user is None:
      messages.error(request, 'Invalid Username or password')
      return redirect('/login/')
    else:
      login(request, user)
      # if user.is_superuser:
      return redirect('/home_articles/')
      # return redirect('/home_articles/')
      # elif user.is_author:
        # return redirect('/add-article/')
      # elif user.is_publisher:
      #   return redirect('/publish_articles/')
      # else:
        # messages.error(request, 'Something went wrong')
        # return redirect('/login/')

  return render(request, 'login.html')  # Render the login page for both GET and POST requests

def logout_page(request):
  logout(request)
  return redirect('/home_articles/')

def register(request):
  if request.method == "POST":
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    password = request.POST.get('password')
    user_role = request.POST.get('user_role')
    email = request.POST.get('email')
    user = CustomUser.objects.filter(username = username)
    if user.exists():
      messages.error(request, "Username already taken.")
      return redirect('/register')

    user = CustomUser.objects.create(
      first_name = first_name,
      last_name = last_name,
      username = username,
      email = email
    )

    user.set_password(password)

    if user_role == 'is_author':
      user.is_author = True
    else:
      user.is_publisher = True

    user.save()
    messages.info(request, 'User registered successfully.')

    return redirect('/register')

  return render(request, 'register.html')

def view_users(request):
  queryset= CustomUser.objects.all()
  context = {'users': queryset}
  return render(request, "view_user.html",context)

@login_required
def articles(request):
  if request.method == "POST":
    data = request.POST
    thumbnail = request.FILES.get('thumbnail')
    title = data.get('title')
    subtitle = data.get('subtitle')
    description = data.get('description')
    
    Article.objects.create(
      thumbnail = thumbnail,
      title = title,
      subtitle = subtitle,
      description = description,
      author = request.user
    )
    return redirect('/articles-list/')
    
  return render(request, 'articles.html')

def articles_list(request):
    user = request.user
    queryset = Article.objects.filter(author=user)
    context = {'articles': queryset}
    return render(request, 'article_list.html', context)

def update_article(request, id):
  queryset = Article.objects.get(id = id)
  if request.method == "POST":
    data = request.POST
    thumbnail = request.FILES.get('thumbnail')
    title = data.get('title')
    subtitle = data.get('subtitle')
    description = data.get('description')

    queryset.title = title
    queryset.subtitle = subtitle
    queryset.description=description

    if thumbnail:
      queryset.thumbnail = thumbnail

    queryset.save()
    return redirect('/articles-list/')
  context = {'articles': queryset}
  return render(request, 'update_articles.html', context)

def delete_article(request, id):
  queryset = Article.objects.get(id = id)
  queryset.delete()
  return redirect('/articles-list/')

def show_published_articles(request):
  queryset = Article.objects.filter(status='Published')
  context = {'articles_published': queryset}
  return render(request, 'published_articles.html', context)

def publisher(request):
  # queryset = Article.objects.all()
  queryset = Article.objects.filter(status = 'Draft')
  context = {'publish_articles': queryset}
  return render(request, 'publisher.html', context)

def view_article_to_be_published(request, id):
  queryset = Article.objects.get(id = id)
  context = {'view_article': queryset}
  return render(request, 'view_articles.html', context)

def update_article_status(request, article_id):
  if request.method == 'POST':
    status = request.POST.get('status')
    article = Article.objects.get(pk=article_id)
    article.status = status
    article.save()

    return redirect('/publish_articles/')

  return render(request, 'view_articles.html')

def delete_user(request, id):
  queryset = CustomUser.objects.get(id = id)
  queryset.delete()
  return redirect('/view_users/')

def home_articles(request):
  queryset = Article.objects.filter(status = 'Published')
  context = {'home_articles': queryset}
  return render(request, 'home.html', context)
