from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main.models import Todo
from django.contrib import messages


# 1. Asosiy To-Do Sahifasi (Faqat tizimga kirganlar uchun)
@login_required(login_url='login')
def index(request):
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'index.html', {'todos': todos})

# 2. Login Sahifasi
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
            
    return render(request, 'login.html')



# 3. Ro'yxatdan O'tish (Register)
def register_view(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        # Username bazada bor-yo'qligini tekshirish
        if User.objects.filter(username=username_input).exists():
            messages.error(request, "Bu username allaqachon band! Boshqa nom tanlang.")
            return redirect('login')
        
        # Yangi foydalanuvchi yaratish
        user = User.objects.create_user(username=username_input, password=password_input)
        login(request, user)
        return redirect('index')
            
    return redirect('login')

# 4. Yangi vazifa qo'shish
@login_required(login_url='login')
def add_todo(request):
    if request.method == 'POST':
        task_text = request.POST.get('task')
        if task_text:
            Todo.objects.create(user=request.user, task=task_text)
    return redirect('index')

# 5. Vazifani bajarildi deb belgilash/yo'qotish
@login_required(login_url='login')
def complete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('index')

# 6. Vazifani o'chirish
@login_required(login_url='login')
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect('index')

# 7. Tizimdan chiqish
def logout_view(request):
    logout(request)
    return redirect('login')