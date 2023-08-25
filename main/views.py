from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect
from main.forms import PostForm, CommentForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from main.models import Post, Comment, Tag, Author, Category
from main.utils import calculate_time_to_read
from django.contrib.auth.models import User
from utils.extractImageFromContent import extract_Images_From_Content

def home(request):
    context = {}
    return render(request, 'main/home.html', context)

def profile(request):
    posts = Post.objects.filter(author__user=request.user.id)
    author = Author.objects.get(user=request.user.id)
    return render(request, 'main/profile.html', {'posts': posts, 'author': author})

def authorProfile(request, id):
    posts = Post.objects.filter(author__user=id)
    author = Author.objects.get(user=id)
    return render(request, 'main/profile.html', {'posts': posts, 'author': author})

def post(request, id):
    if request.method == 'POST':
        modifiedPostRequest = request.POST.copy()
        modifiedPostRequest['author'] = Author.objects.get(user=request.user.id)
        modifiedPostRequest['post'] = Post.objects.get(pk=id)
        form = CommentForm(modifiedPostRequest)

        if form.is_valid():
            form.save()

    post = get_object_or_404(Post, pk=id)
    comments = Comment.objects.filter(post=id, parent=None)
    comment_form = CommentForm

    post.views += 1
    post.save()

    user = User.objects.get(id=request.user.id)
    isLiked = post.likes.filter(user=user).exists()
    isFavorited = Author.objects.get(user=user).favorites.filter(id=id).exists()

    return render(request, 'main/post.html', {'id': id, 'post': post, 'comments': comments, "comment_form": comment_form, "isLiked": isLiked, "isFavorited": isFavorited})

def like(request, id):
    post = get_object_or_404(Post, pk=id)
    liked = post.likes.filter(user=request.user.id).exists()

    if request.method == "POST" and not liked:
        post.likes.add(Author.objects.get(user=request.user.id))
        post.save()
        return HttpResponse("Liked")
    elif request.method == "DELETE":
        post.likes.remove(Author.objects.get(user=request.user.id))
        return HttpResponse("Deleted")
    else:
        return HttpResponse("Internal Error")

def favorite(request, id):
    userObj = get_object_or_404(Author, user=request.user.id)
    isFavorited = userObj.favorites.filter(pk=id).exists()

    if request.method == "POST" and not isFavorited:
        userObj.favorites.add(Post.objects.get(pk=id))
        userObj.save()
        return HttpResponse('Added to favorites')
    elif request.method == "DELETE":
        userObj.favorites.remove(Post.objects.get(pk=id))
        return HttpResponse('Removed bookmark')
    else:
        return HttpResponse("Internal Error")

def posts(request):
    query = request.GET.get('search')
    category = request.GET.get('category')
    sort_by = request.GET.get('sort')

    posts = Post.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)

    elif category:
        try :
            cat = Category.objects.get(name=category)
            posts = posts.filter(category=cat)
        except:
            posts = []

    elif sort_by == 'recent':
        posts = posts.order_by('-publish_date')

    elif sort_by == 'top10':
        posts = posts.order_by('-views')[:10]
    

    context = {
        'posts': posts,
        'selected_category': category,
        'selected_sort': sort_by,
    }

    return render(request, 'main/posts.html', context)


def createpost(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        tags_string = post_data.get('tags', '')
        tag_names = tags_string.split()
        tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names]
        post_data.setlist('tags', [str(tag.id) for tag in tags])
        user = User.objects.get(username=request.user.username)
        userObj, created = Author.objects.get_or_create(user=user)
        post_data['author'] = str(userObj.id)
        userObj = User.objects.get(pk=request.user.id)
        post_data['author'] = str(Author.objects.get_or_create(user=userObj)[0].id)
        post_data['views'] = "0"
        post_data['time_to_read'] = calculate_time_to_read(post_data['content'])

        form = PostForm(post_data)

        if form.is_valid():
            post = form.save(commit=False)
            thumbnail_url = extract_Images_From_Content(post.content)

            if thumbnail_url:
                post.thumbnail_url = thumbnail_url

            post.save()
            return HttpResponse("Created!")

        else:
            print(form.errors)

    return render(request, 'main/createpost.html', {"form": PostForm})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Registration done successfully!")
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {"form": form})

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
    form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login")

def bookmarks(request):
    posts = Post.objects.filter(author__user=request.user.id)
    author = Author.objects.get(user=request.user.id)

    user = request.user  
    author = Author.objects.get(user=user)
    bookmarks = author.favorites.all()

    context = {
        'bookmarks': bookmarks,
        'posts': posts, 
        'author': author
    }

    return render(request, 'main/bookmarks.html', context)
