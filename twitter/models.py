from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(User, related_name="tweets", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="tweet_like", blank=True)
    is_edited = models.BooleanField(default=False)
    
    def number_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return(
            f"{self.user} "
            f"({self.created_at:%d-%m-%Y %H:%M}): "
            f"{self.body}.."
            )
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    profile_bio = models.CharField(null=True, blank=True, max_length=200)
    website_link = models.CharField(null=True, blank=True, max_length=150)
    instagram_link = models.CharField(null=True, blank=True, max_length=150)
    linkedin_link = models.CharField(null=True, blank=True, max_length=150)
    def __str__(self):
       return self.user.username
    def can_follow(self, profile_to_follow):
        return self != profile_to_follow
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
post_save.connect(create_profile, sender=User)

