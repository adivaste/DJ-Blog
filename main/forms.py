from django import forms
from main.models import Post, Comment, Author, Category, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"

      
class CommentForm(forms.ModelForm):
    class Meta:
      model = Comment
      fields = "__all__"

class SignUpForm(UserCreationForm):
    dob = forms.DateTimeField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('avatar','dob','first_name','last_name','email','username')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'})
        }
    
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            author = Author.objects.create(
                user = user,
                dob = self.cleaned_data['dob'],
                profile_pic = self.cleaned_data['avatar']
            )
            author.save()

