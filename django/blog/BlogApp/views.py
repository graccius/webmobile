from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Follow
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse  # for likes
from django.contrib.auth.hashers import make_password
from requests import request

# View para a página inicial exibindo os posts
class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verifica se o usuário está seguindo os autores dos posts
        user_following = {post.author.id: self.request.user in post.author.followers.all() for post in context['posts']}
        context['user_following'] = user_following
        return context

# View para curtir/descurtir um post
class LikePostView(View):
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})
    
    
## VIEW PARA VER DETALHES DO POST
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    
    
## FOLLOW VIEW ##
class FollowUserView(View):
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        
        # Verifica se o usuário já está seguindo
        follow_relation, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)

        if not created:  # Se já existe um relacionamento, removemos
            follow_relation.delete()
            following = False
        else:
            following = True
        
        # Conta quantos seguidores o usuário seguido tem
        followers_count = user_to_follow.followers.count()
        
        return JsonResponse({'following': following, 'followers_count': followers_count})
    

#VIEW PARA REGISTRAR USUARIO ##
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'register.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "O nome de usuário já existe.")
            return render(request, 'register.html')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Este email já está registrado.")
            return render(request, 'register.html')

        # Create the user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password1)  # Hash the password
        )
        user.save()
        messages.success(request, "Registro realizado com sucesso! Você pode entrar agora.")
        return redirect('login')  # Redirect to login page after successful registration

# VIEW PARA PERFIL DO USUARIO
class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = 'profile.html'
    login_url = '/login/'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Adiciona o usuário ao contexto
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()
    
    


# View para o login
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        # Renderiza o template de login quando a requisição é GET
        return render(request, self.template_name)

    def post(self, request):
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

        return render(request, self.template_name)

## LOGOUT 
class LogoutView(View):
    def get(self, request):
        logout(request)  # Desconecta o usuário
        return redirect('/login/')
