from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as lin
from django.contrib.auth import logout as lout
from .models import CreateUserForm, Profile, Post, LikePost, Follow
from itertools import chain


@login_required(login_url='login')
def index(request):
    user = Profile.objects.get(user = request.user)
    user_posts = Post.objects.filter(user = user.user)
    nr_posts = len(user_posts)

    user_following_list = []
    feed = []

    user_following = Follow.objects.filter(follower = request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))


    context = {
        'user': user,
        'posts': feed_list,
        'nr_postari': nr_posts
    }
    return render(request, 'index.html', context)



@login_required(login_url='login')
def prieteni(request, pk):
    following = Follow.objects.filter(follower = pk)
    user_loged = Profile.objects.get(user = request.user)

    context = {

        'following': following,
        'user': user_loged

    }

    return render(request, 'prieteni.html', context)



@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(username = pk)
    user_page = Profile.objects.get(user = user)

    user_loged = Profile.objects.get(user = request.user)
    user_l = user_loged.user.username

    if Follow.objects.filter(follower = user_l, user = pk).first() is None:
        verificare = False

    else:
        verificare = True

    posts = Post.objects.filter(user = pk).all()
    nr_posts = len(posts)

    context = {
        'user_page': user_page,
        'posts': posts,
        'user_loged': user_loged,
        'nr_postari': nr_posts,
        'verificare': verificare
    }

    return render(request, 'profile.html', context)



@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        user_loged = Profile.objects.get(user = request.user)
        user = User.objects.get(username = request.POST['username'])
        user_page = Profile.objects.get(user = user)
        username_loged = user_loged.user.username
        username_page = request.POST['username']

        filtru = Follow.objects.filter(follower = username_loged, user = username_page).first()

        if filtru is None:
            new_follow = Follow.objects.create(follower = username_loged, user = username_page, follower_img = user_loged.profile_img, user_img = user_page.profile_img)
            new_follow.save()
            user_loged.following = user_loged.following + 1
            user_loged.save()
        else:
            filtru.delete()
            user_loged.following = user_loged.following - 1
            user_loged.save()
            
        return redirect('profile/'+username_page)

    else:
        return redirect('/')



@login_required(login_url='login')
def postare(request):

    user_profile = Profile.objects.get(user = request.user)
    
    if request.method == 'POST':
         
        username = user_profile.user.username
        profile_img = user_profile.profile_img
        image = request.FILES.get('image')
        caption = request.POST.get('caption')

        new_post = Post.objects.create(user = username, user_img = profile_img, image = image, caption = caption)
        new_post.save()
        
        return redirect('/')
    
    context = {

        'user': user_profile

    }

    return render(request, 'postare.html', context)



def like(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id = post_id)

    like_filter = LikePost.objects.filter(username = username, post_id = post_id).first()

    if like_filter is None:
        new_like = LikePost.objects.create(username = username, post_id = post_id)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')

    else:
        like_filter = LikePost.objects.get(username = username, post_id = post_id)
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')



def signup(request):
    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            username = request.POST.get('username')
            user = User.objects.get(username = username)
            profil_nou = Profile.objects.create(user = user, id_user = user.id, email = user.email)
            profil_nou.save()

            return redirect('login')

    context = {
        'form': form
    }

    return render(request, 'signup.html', context)




def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            lin(request, user)
            return redirect('/')
        
        else:
            messages.info(request, 'Username or password incorrect')

    return render(request, 'login.html')




@login_required(login_url='login')
def logout(request):

    lout(request)
    return redirect('login')




@login_required(login_url='login')
def settings(request):
    user = Profile.objects.get(user = request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')

        else:
            image = user.profile_img
        
        bio = request.POST.get('bio')
        email = request.POST.get('email')

        user.profile_img = image
        user.bio = bio
        user.email = email
        user.save()
        
        return redirect('profil')   
 

    context = {
        'user': user
    }

    return render(request, 'settings.html', context)



@login_required(login_url='login')
def search(request):
    user_loged = Profile.objects.get(user = request.user)
    context = {

        'user': user_loged,

    }
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains = username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))

        context = {

            'user': user_loged,
            'search_list': username_profile_list

        }

    
    
    return render(request, 'search.html', context)
