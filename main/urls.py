from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main import views

urlpatterns = [
      path('', views.home, name='home'),
      path('posts', views.posts, name='posts'),
      path('posts/<int:id>', views.post, name='post'),
      path('posts/<int:id>/like', views.like, name='like'),
      path('posts/<int:id>/favorite', views.favorite, name='favorite'),
      path('createpost', views.createpost, name='createpost'),
      path('profile1', views.profile, name='profile'),
      path('profile/<int:id>', views.authorProfile, name='authorProfile'),
      path('login', views.user_login, name='login'),
      path('signup', views.signup, name='signup'),
      path('logout', views.user_logout, name='logout'),
      path('bookmarks', views.bookmarks, name='bookmarks'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)