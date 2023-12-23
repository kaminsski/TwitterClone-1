"""
URL configuration for Twitter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Users.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="home"),
    path("404", error, name="404"),
    path("login", login, name="login"),
    path("logout", log_out, name="log_out"),
    path("register", register, name="register"),
    path("reports", reports, name="reports"),
    path("requests", requests, name="requests"),
    path("trends", trends, name="trends"),
    path("messages", privateMessages, name="messages"),
    path("messages/<messageId>", messageDetail, name="messageDetail"),
    path("profile/<userId>", profile, name="profile"),
    path("confirmUser/<userId>", confirmUser, name="confirmUser"),
    path("updateProfile/<userId>", updateProfile, name="upProfile"),
    path("createMod/<userId>", createMod, name="createMod"),    
    path("delete/<tweetId>", deleteTweet, name="deleteTweet"),
    path("deleteReport/<reportId>", deleteReport, name="deleteReport"),
    path("deleteProfile/<userId>", deleteProfile, name="deleteProfile"),
    path("updateTweet/<tweetId>", updateTweet, name="upTweet"),
    path("updatePassword/<userId>", updatePassword, name="upPassword"),
    path("detailTweet/<tweetId>", tweetDetail, name="tweetDetail"),
    path("delete/<commentId>/<tweetId>", deleteComment, name="deleteComment"),
    path("like/<userId>/<tweetId>", addLike, name="addLike"),
    path("follow/<takipEdenId>/<takipEdilenId>", addFollow, name="addFollow"),
    path("updateComment/<commentId>/<tweetId>", updateComment, name="upComment"),
    path("userBan/<userId>/<reportId>", userBan, name="userBan"),
    path("reportTweet/<tweetId>/<userId>", reportTweet, name="reportTweet"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)