from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect
from main.forms import PostForm, CommentForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from main.models import Post, Comment, Tag, Author
from main.utils import calculate_time_to_read
from django.contrib.auth.models import User

# Create your views here.
def home(request):
      context = {}
      return render(request, 'main/home.html', context)

# Author Profile 
def profile(request):
      posts = Post.objects.filter(author__user=request.user.id)
      author = Author.objects.get(user=request.user.id)
      return render(request, 'main/profile.html', {'posts' : posts, 'author' : author})

def authorProfile(request,id):
      posts = Post.objects.filter(author__user=id)
      author = Author.objects.get(user=id)
      return render(request, 'main/profile.html', {'posts' : posts, 'author' : author})

def post(request, id):

      # Adding the comment 
      if request.method == 'POST':
            modifiedPostRequest = request.POST.copy()
            modifiedPostRequest['author'] = Author.objects.get(user=request.user.id)
            modifiedPostRequest['post'] = Post.objects.get(pk=id)
            form = CommentForm(modifiedPostRequest)

            if form.is_valid():
                  form.save()

      # Get the post
      post = get_object_or_404(Post, pk=id)
      comments = Comment.objects.filter(post=id, parent=None)
      comment_form = CommentForm

      # Increamenting the views of post by 1
      if post:
            post.views = post.views + 1
            post.save()

      # Check Liked and Bookmarked
      isLiked = post.likes.filter(user=request.user.id).exists()
      isFavorited = Author.objects.get(user=request.user.id).favorites.filter(id=id).exists()
      
      return render(request, 'main/post.html', {'id': id, 'post' : post, 'comments': comments, "comment_form": comment_form, "isLiked" : isLiked, "isFavorited" : isFavorited})

#  Like the post
def like(request, id):
      post = get_object_or_404(Post, pk=id)
      liked = post.likes.filter(user=request.user.id).exists()
      current_url = request.get_full_path()
      if request.method == "POST" and not liked :
            post.likes.add(Author.objects.get(user=request.user.id))
            post.save()
            print(post.likes.count())
            return HttpResponse("Liked")
      elif (request.method == "DELETE"):
            post.likes.remove(Author.objects.get(user=request.user.id))
            return HttpResponse("Deleted")
      else:
            return HttpResponse("Internal Error")
      
      if request.method == "GET":
            post = get_object_or_404(Post, pk=id)
            if not post.likes.filter(pk=request.user.id).exists():
                  post.likes.add(Author.objects.get(pk=request.user.id))
                  post.save()
                  print(post.likes.count())
                  return HttpResponse('Liked')
            else:
                  post.likes.remove(Author.objects.get(pk=request.user.id))
                  return HttpResponse("removed")
      return HttpResponse('Some diff')


#  Like the post
def favorite(request, id):
      
      userObj = get_object_or_404(Author, user=request.user.id)
      isFavorited = userObj.favorites.filter(pk=id).exists()
      if request.method == "POST" and not isFavorited:
            userObj.favorites.add(Post.objects.get(pk=id))
            userObj.save()
            print(userObj.favorites.count())
            return HttpResponse('Added to favorites')
      elif (request.method == "DELETE"):
            userObj.favorites.remove(Post.objects.get(pk=id))
            return HttpResponse('Removed bookmark')
      else:
            return HttpResponse("Internal Error")


def posts(request):

      # Search Query
      search_query =  request.GET.get('search', '')
      
      if search_query:
            posts = Post.objects.filter(title__icontains=search_query)
      else:
            posts = Post.objects.all()

      for post in posts:
            print(post.tags.all())
      return render(request, 'main/posts.html', {"posts": posts})

def createpost(request):
      if request.method == 'POST':
            # form = PostForm(request.POST)
            print(request.POST)

            # Make a copy of the request.POST QueryDict object
            post_data = request.POST.copy()
            
            # Get the tags string from the form data
            tags_string = post_data.get('tags', '')
            
            # Split the tags string into a list
            tag_names = tags_string.split()
            
            # Create Tag objects for each tag name
            tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names]
            
            # Add the tags to the post_data copy
            post_data.setlist('tags', [str(tag.id) for tag in tags])
            
            # Modify the 'title' field in the copy
            print("--------",request.user.id)
            userObj, created = Author.objects.get_or_create(user=request.user.id) 
            print("----------------------???????" + str(userObj.id))
            post_data['author'] = str(userObj.id)
            userObj = User.objects.get(pk=request.user.id)
            post_data['author'] = str(Author.objects.get_or_create(user=userObj)[0].id)
            post_data['views'] = "0"
            # post_data['likes'] = None
            post_data['time_to_read'] = calculate_time_to_read(post_data['content'])

            print(request.user.id)
            
            # Create a new form instance using the modified data
            form = PostForm(post_data)
            print(post_data)
            
            # Process the form as usual
            if form.is_valid():
                  form.save()
                  print("-----")
                  return HttpResponse("Created broiiii!") 
            else:
                  print(form.errors)

      return render(request, 'main/createpost.html', {"form" : PostForm})

def signup(request):
      if request.method == 'POST':
            print(request.POST)
            print(request.FILES)
            form = SignUpForm(request.POST, request.FILES)
            if form.is_valid():
                  form.save()
                  return HttpResponse("Registration done successfully!")
      else:
            form = SignUpForm()
      return render(request, 'main/signup.html', {"form" : form})

def user_login(request):
      if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                  uname = form.cleaned_data['username']
                  upass = form.cleaned_data['password']
                  user = authenticate(username=uname, password=upass)
                  if user is not None:
                        login(request, user)
                        return HttpResponseRedirect("/createpost")
            
      form  = AuthenticationForm()
      return render(request, 'main/login.html',{ 'form' : form})


def user_logout(request):
      logout(request)
      return HttpResponseRedirect("/login")
