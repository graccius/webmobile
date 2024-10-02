from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import HomeView, LikePostView, UserProfileView, LoginView, LogoutView, RegisterView, PostDetailView, FollowUserView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('like/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
