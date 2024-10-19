from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm, SignUpForm, UserUpdateForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, "Your tweet has been posted!")
            return redirect('home')

        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets": tweets, "form": form})

    return handle_unauthenticated_request(request)

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user).order_by("-date_modified")
        return render(request, 'profile_list.html', {"profiles": profiles})

    return handle_unauthenticated_request(request)

def profile(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")

        if request.method == "POST":
            curr_user_profile = request.user.profile
            action = request.POST['follow']
            
            if action == "unfollow":
                curr_user_profile.follows.remove(profile)
            elif action == "follow":
                curr_user_profile.follows.add(profile)
            curr_user_profile.save()
        return render(request, "profile.html", {"profile": profile, "tweets": tweets})
    
    return handle_unauthenticated_request(request)

def handle_unauthenticated_request(request):
    messages.error(request, "You must be logged in to view this page.")
    return redirect('login')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have successfully logged in! Start tweeting now!!"))
            return redirect('home')
        else:
            messages.error(request, ("There was an error logging in...Please try again!"))
            return redirect('login')
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

def register_user(request):
    form=SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user= authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("You have successfully registered! Start tweeting now!!"))            
            return redirect('home')
        
    return render(request, "register.html", {'form':form})

def update_user(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = UserUpdateForm(request.POST, instance=request.user)
            profile_pic_form = ProfilePicForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid() and profile_pic_form.is_valid():
                user = form.save()
                profile_pic_form.save()
                if form.cleaned_data.get('password'):
                    update_session_auth_hash(request, user)
                messages.success(request, "Your profile has been updated successfully!")
                return redirect('profile', pk=request.user.pk)
            else:
                messages.error(request, "There was an error updating your profile. Please check the form and try again.")
        else:
            form = UserUpdateForm(instance=request.user)
            profile_pic_form = ProfilePicForm(instance=request.user.profile)
        
        return render(request, "update_user.html", {"form": form, "profile_pic_form": profile_pic_form})
    else:
        return handle_unauthenticated_request(request)

def tweet_like(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))   
    else:
        return handle_unauthenticated_request(request)
    
def view_tweet(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    
    if tweet:
        return render(request, "view_tweet.html", {'tweet':tweet})
    else:
        return handle_unauthenticated_request(request)
    
def unfollow(request, pk):
    if request.user.is_authenticated:
        profile_to_unfollow = get_object_or_404(Profile, user_id=pk)
        request.user.profile.follows.remove(profile_to_unfollow)
        messages.success(request, f"Successfully unfollowed {profile_to_unfollow.user.username}!")
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        return handle_unauthenticated_request(request)

def follow(request, pk):
    if request.user.is_authenticated:
        profile_to_unfollow = get_object_or_404(Profile, user_id=pk)
        request.user.profile.follows.add(profile_to_unfollow)
        messages.success(request, f"Successfully followed {profile_to_unfollow.user.username}!")
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        return handle_unauthenticated_request(request)
