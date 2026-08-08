from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Todo

# 1. Asosiy To-Do Sahifasi
@login_required(login_url='login')
def index(request):
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'todo_app/index.html', {'todos': todos})

# 2. Login va Sign Up Sahifasi
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        user = authenticate(request, username=username_input, password=password_input)
        if user is not None:
            login(request, user)
            return redirect('index')
            
    return render(request, 'todo_app/login.html')

# 3. Ro'yxatdan O'tish
def register_view(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        if not User.objects.filter(username=username_input).exists():
            user = User.objects.create_user(username=username_input, password=password_input)
            login(request, user)
            return redirect('index')
            
    return redirect('login')

# 4. Vazifa Qo'shish
@login_required(login_url='login')
def add_todo(request):
    if request.method == 'POST':
        task_text = request.POST.get('task')
        if task_text:
            Todo.objects.create(user=request.user, task=task_text)
    return redirect('index')

# 5. Vazifani Bajarildi Deb Belgilash
@login_required(login_url='login')
def complete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('index')

# 6. Vazifani O'chirish
@login_required(login_url='login')
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect('index')

# 7. Tizimdan Chiqish
def logout_view(request):
    logout(request)
    return redirect('login')
