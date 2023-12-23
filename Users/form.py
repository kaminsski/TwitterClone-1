from django import forms
from .models import *

class RegisterForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ["username","first_name","last_name", "password", "email","about","education", "country", "city", "bornDate","userColor" ]

        help_texts = {
            "username" : None
           
        }
  
class UpdateForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ["avatar","email","about","education", "country", "city", "bornDate","userColor" ]

class TweetUpdateForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["tweetTitle","tweetDescription","tweetImage"]  

class TweetAddForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["tweetTitle","tweetDescription","tweetImage"]                

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"] 
        labels = {
            "message" : "Make comment"
        }
class UpdateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]       
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["description"]         

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["message"]    
        labels = {
            "message" : "Send message"
        }        
                 
       