from django.db import models
from django_countries.fields import CountryField
import datetime
# Create your models here.
from django.contrib.auth.models import AbstractUser
current_time = datetime.datetime.now()
class Edu(models.Model):
    educationLevels = models.CharField("Education", max_length=50, null=True)

    def __str__(self):
        return self.educationLevels
    
class Color(models.Model):
    colors = models.CharField(("Color"), max_length=50, null=True)
    def __str__(self):
        return self.colors    

class AppUser(AbstractUser):
    avatar = models.FileField(("User Avatar"), upload_to="uploads", null=True, blank=True)
    about = models.CharField(( "About"), max_length=50,null=True)
    education = models.ForeignKey(Edu, verbose_name=("Education"), on_delete=models.CASCADE, null=True)
    country = CountryField(null=True)
    city = models.CharField(( "City"), max_length=50,null=True)
    bornDate = models.DateField(("Birth of date"), null=True)
    takipciSayisi = models.IntegerField(("takipciSayisi"),default=0)
    takipEdilenSayisi = models.IntegerField(("takipEdilenSayisi"),default=0)
    is_Confirm = models.BooleanField(("Is confirm?"), default=False )
    userColor = models.ForeignKey(Color, verbose_name=("Color"), on_delete=models.CASCADE, null=True)

    def isModerator(self):
        role = self.groups.filter(name="Mod").exists()
        return role



    def handleAvatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return "uploads/default.png"





class Tweet(models.Model):
    user = models.ForeignKey(AppUser, verbose_name=("User"), on_delete=models.CASCADE)
    tweetTitle = models.CharField(("Title"), max_length=50, null=True)
    tweetDescription = models.TextField(("Description"), max_length=200, null=True)
    tweetImage= models.FileField(("Image"), upload_to="uploads", null=True,blank=True)
    likeQuatity = models.IntegerField(("Like"),default=0)
    createdAt = models.DateTimeField(("Created"), auto_now=True)
    commentQuatity = models.IntegerField(("Comment"),default=0)
   
    def handleImage(self):
        if self.tweetImage:
            return self.tweetImage.url
        else:
            return "uploads/default.png"

    def __str__(self):
        return self.tweetTitle

class PostLikes(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    author = models.ForeignKey(AppUser, verbose_name=("Comment Author"), on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, verbose_name=("Tweet"), on_delete=models.CASCADE)
    message = models.TextField(("Message"))
    createdAt = models.DateTimeField(("Created"), auto_now=True)

class Report(models.Model):
    sender = models.ForeignKey(AppUser, verbose_name=("Report sender"), on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    description = models.CharField(("Description"), max_length=50)
    createdAt = models.DateTimeField(("Created"), auto_now=True)

class Follow(models.Model):
    takipEden = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    takipEdilen = models.ForeignKey(AppUser,related_name='Follower', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    recipient = models.ForeignKey(AppUser,related_name='Recipient', on_delete=models.CASCADE)
    message = models.TextField(("Message"), max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    is_Read = models.BooleanField(("has it been read?"), default=False )










