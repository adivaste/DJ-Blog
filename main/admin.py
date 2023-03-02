from django.contrib import admin
from main.models import Post, Comment, Author, Tag, Category
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class AuthorInline(admin.StackedInline):
      model = Author
      can_delete = False
      verbose_name = 'Authors'

class CustomizedAdmin(UserAdmin):
      inlines = (AuthorInline,)

# Register your models here.
admin.site.unregister(User)
admin.site.register(User, CustomizedAdmin)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Category)