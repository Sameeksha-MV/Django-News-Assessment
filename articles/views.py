
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from articles.models import CustomUser

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
      return redirect('/add-article/')

  return render(request, 'login.html')  # Render the login page for both GET and POST requests

def logout_page(request):
  logout(request)
  return redirect('/login/')

def register(request):
  if request.method == "POST":
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    password = request.POST.get('password')
    user_role = request.POST.get('user_role')

    user = CustomUser.objects.filter(username = username)
    if user.exists():
      messages.error(request, "Username already taken.")
      return redirect('/register')

    user = CustomUser.objects.create(
      first_name = first_name,
      last_name = last_name,
      username = username
    )

    user.set_password(password)

    if user_role == 'is_author':
      user.is_author = True
      user.is_publisher = False
    elif user_role == 'is_publisher':
      user.is_author = False
      user.is_publisher = True
    else:
      user.is_author = False
      user.is_publisher = False

    user.save()

    messages.info(request, 'User registered successfully.')

    return redirect('/register')

  return render(request, 'register.html')

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
    return redirect('/add-article/')
    queryset = Articles.objects.all()

  if request.GET.get('search'):
    queryset = queryset.filter(title__icontains = request.GET.get('search'))

  # context = {'articles': queryset}
  return render(request, 'articles.html')

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
    return redirect('/update-article/')

  context = {'articles': queryset}
  return render(request, 'update_articles.html', context)

def delete_article(request, id):
  queryset = Article.objects.get(id = id)
  queryset.delete()
  return redirect('/add-article/')