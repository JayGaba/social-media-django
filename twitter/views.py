from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm

def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, ("Your tweet has been posted!"))
                return redirect('home')
                
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets":tweets, "form":form})

    else:
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets":tweets})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
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
                
        
        return render(request, "profile.html", {"profile": profile, "tweets":tweets})
    else:
        return handle_unauthenticated_request(request)

def handle_unauthenticated_request(request):
    messages.error(request, "You must be logged in to view this page.")
    return redirect('home')