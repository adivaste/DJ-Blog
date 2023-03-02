from django.shortcuts import render, HttpResponse, get_object_or_404
from main.forms import PostForm, CommentForm
from main.models import Post, Comment

# Create your views here.
def home(request):
      context = {}
      return render(request, 'main/home.html', context)

def post(request, id):
      if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                  form.save()
      post = get_object_or_404(Post, pk=id)
      comments = Comment.objects.filter(post=id)
      comment_form = CommentForm

      return render(request, 'main/post.html', {'id': id, 'post' : post, 'comments': comments, "comment_form": comment_form})


def posts(request):
      posts = Post.objects.all()
      return render(request, 'main/posts.html', {"posts": posts})

def createpost(request):
      if request.method == 'POST':
            form = PostForm(request.POST)
            print(request.POST)
            if form.is_valid():
                  form.save()
                  return HttpResponse("Created broiiii!")
      return render(request, 'main/createpost.html', {"form" : PostForm})