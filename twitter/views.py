from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Profile

def home(request):
    return render(request, 'home.html', {})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        return handle_unauthenticated_request(request)
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user_id=pk)  # Use get_object_or_404 for better error handling
        return render(request, "profile.html", {"profile": profile})
    else:
        return handle_unauthenticated_request(request)

def handle_unauthenticated_request(request):
    messages.error(request, "You must be logged in to view this page.")
    return redirect('home')