from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import uuid
from datetime import datetime

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    id_user = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank = True)
    profile_img = models.ImageField(upload_to = 'profile_images', default='default-profile-icon-16.png')
    email = models.EmailField()
    following = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    user_img = models.ImageField(upload_to = 'post_profile_img', default='default-profile-icon-16.png')
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class Follow(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    follower_img = models.ImageField(upload_to='fllwer_img', default='')
    user_img = models.ImageField(upload_to='user_img', default='')

    def __str__(self):
        return self.user


