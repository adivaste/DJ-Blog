from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main import views

urlpatterns = [
      path('', views.home, name='home'),
      path('posts', views.posts, name='posts'),
      path('posts/<int:id>', views.post, name='post'),
      path('createpost', views.createpost, name='createpost'),
      path('login', views.user_login, name='login'),
      path('signup', views.signup, name='signup'),
      path('logout', views.user_logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)