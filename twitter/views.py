from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm
from django.contrib.auth import authenticate, login, logout

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
        profiles = Profile.objects.exclude(user=request.user)
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
