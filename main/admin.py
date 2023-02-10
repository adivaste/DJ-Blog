from django.contrib import admin
from main.models import Post, Comment, Author, Tag


# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Tag)