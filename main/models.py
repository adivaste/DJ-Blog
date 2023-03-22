from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.conf.urls.static import static
from datetime import datetime, date


# Create your models here.
class Post(models.Model):
      title = models.CharField(max_length=255)
      content = HTMLField(blank=True,null=True)
      publish_date = models.DateTimeField(auto_now_add=True)
      author = models.ForeignKey('Author', on_delete=models.CASCADE)
      views = models.IntegerField(default=0)
      likes = models.ManyToManyField('Author',related_name="liked_posts", null=True, blank=True)
      time_to_read = models.IntegerField(default=0)
      tags = models.ManyToManyField('Tag', related_name='post_set', null=True, blank=True)
      category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL)

      def __str__(self):
            return str(self.title)


class Author(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE)
      dob = models.DateField(default=date.today())
      profile_pic = models.ImageField(upload_to='author_pics', blank=True, null=True, default='author_pics/default1.png')
      favorites = models.ManyToManyField('Post', related_name='favorite_of_authors', null=True, blank=True)

      def __str__(self):
            return str(self.user.username)

      @staticmethod
      def get_default_profile_pic():
        return 'author_pics/default1.png'



class Comment(models.Model):
      author = models.ForeignKey('Author', on_delete=models.CASCADE)
      post = models.ForeignKey('Post', on_delete=models.CASCADE)
      body = models.TextField()
      publish_date = models.DateTimeField(auto_now_add=True)
      parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

      def __str__(self):
            return str(self.body)


class Tag(models.Model):
      name = models.CharField(max_length=100)

      def __str__(self):
            return str(self.name)


class Category(models.Model):
      name = models.CharField(max_length=255)

      def __str__(self):
            return str(self.name)