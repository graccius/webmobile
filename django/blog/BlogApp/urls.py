from django.urls import path
from .views import HomeView, login_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Página inicial
    path('login/', login_view, name='login'),  # Página de login
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)