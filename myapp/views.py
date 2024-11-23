from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post, Comment, Contact
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

def index(request):
    return render(request, 'index.html', {'posts': Post.objects.all(), 
                                          'media_url':settings.MEDIA_URL} )

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        user_type = request.POST['type']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exist.')
                return redirect('myapp:signup')
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exist.')
                return redirect('myapp:signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                if user_type == 'superuser':
                    user.is_superuser = True
                    user.save()
                elif user_type == 'staff':
                    user.is_staff = True
                    user.save()
                else:
                    user.save()
                return redirect('myapp:signin')
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('myapp:index')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return redirect('myapp:signin')
    else:
        return render(request, 'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('myapp:index')

def blog(request):
    return render(request, 'blog.html', {
        'posts': Post.objects.filter(user_id = request.user.id).order_by('id').reverse(), 
        'top_posts' : Post.objects.all().order_by('-likes'),
        'recent_posts' : Post.objects.all().order_by('-id'),
        'user': request.user,
        'media_url': settings.MEDIA_URL
    })

def create(request):
    if request.method == 'POST':
        postname = request.POST['postname']
        category = request.POST['category']
        image = request.FILES.get('image')
        content = request.POST['content']
        time = request.POST.get('time', timezone.now())
        likes = request.POST['likes']
        new_blog  = Post(postname=postname, category=category, image=image, content=content, time=time, likes=likes, user = request.user)
        new_blog.save()
        return redirect('myapp:index')
    else:
        return render(request, 'create.html')
    
def profile(request, id):
    return render(request, 'profile.html', {
        'user':User.objects.get(id=id),
        'posts':Post.objects.all(),
        'media_url':settings.MEDIA_URL
    })

def profileedit(request, id):
    if request.method=='POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        user = User.objects.get(id=id)
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.save()
        return profile(request, id)
    return render(request, 'profileedit.html', {
        'user': User.objects.get(id = id)
        
    })


def increaselikes(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id = id)
        post.likes += 1
        post.save()
    return redirect('myapp:index')

def post(request, id):
    post = Post.objects.get(id = id)
    return render(request, 'post_details.html', {
        'user': request.user, 
        'post': Post.objects.get(id = id),
        'recent_posts': Post.objects.all().order_by('-id'),
        'media_url': settings.MEDIA_URL,
        'comments':Comment.objects.filter(post_id=post.id) ,
        'total_comments':len(Comment.objects.filter(post_id=post.id))

    })

def savecomment(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        content = request.POST['message']
        Comment(post_id = post.id, user_id = request.user.id, content = content).save()
        return redirect('myapp:index')
    
def deletecomment(request, id):
    comment = Comment.objects.get(id= id)
    post_id = comment.post.id
    comment.delete()
    return post(request, post_id)

def editpost(request, id):
    post = Post.objects.get(id = id)
    if request.method == 'POST':
        postname = request.POST['postname']
        category = request.POST['category']
        content = request.POST['content']
        time = request.POST.get('time', timezone.now())
        post.postname = postname
        post.category = category
        post.content = content
        post.time = time
        post.save()
        return profile(request, request.user.id)
    else:
        return render(request, 'editpost.html', {
            'post':post
        })


def deletepost(request, id):
    post = Post.objects.get(id = id)
    post_id = post.id
    post.delete()
    return render(request, 'profile.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        obj = Contact(name = name, email = email, subject = subject, message = message )
        obj.save()
        context = {'message': f'Dear {name}, Thanks for your time!'}
        
    return render(request, 'contact.html')