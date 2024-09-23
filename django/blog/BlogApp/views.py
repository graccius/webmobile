from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Post
from django.contrib.auth.models import User

# View para a página inicial exibindo os posts
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'  # O nome da variável que será usada no template

# View para o login
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Buscar o usuário pelo e-mail
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # Redireciona para a página inicial após o login
            else:
                messages.error(request, 'Credenciais inválidas')
        except User.DoesNotExist:
            messages.error(request, 'Usuário com este e-mail não existe')

    return render(request, 'login.html')
