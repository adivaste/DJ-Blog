from django import forms
from main.models import Post, Comment, Author

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
      
class CommentForm(forms.ModelForm):
    class Meta:
      model = Comment
      fields = "__all__"