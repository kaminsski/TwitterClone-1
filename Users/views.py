from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout, authenticate
from .models import *
from .form import *
from django.contrib import messages
from django.contrib.auth.models import Group


# Create your views here.
def index(request):
    context = {}
    tweets = Tweet.objects.filter(user__is_active=True).order_by("-createdAt")
    context["tweets"] = tweets
    likedtweets = Tweet.objects.extra(
        select={'sum':
                'likeQuatity + commentQuatity'}, order_by=('-sum', ))[:4]

    context["likedtweets"] = likedtweets

    comments = Comment.objects.all().order_by("-createdAt")
    context["comments"] = comments

    postLikes = PostLikes.objects.all()
    context["postLikes"] = postLikes

    reports = Report.objects.all()
    context["reports"] = reports

    if request.user.is_authenticated:
        context["is_Mod"] = request.user.isModerator

    if request.method == "POST":
        form = TweetAddForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.add_message(request, messages.INFO, "Tweet shared")

            return redirect("home")
        else:
            return redirect("home")
    else:
        context["form"] = TweetAddForm
        context["form1"] = CommentForm

        return render(request, "index.html", context)


def profile(request, userId):
    context = {}
    if request.user.is_authenticated == False:
        messages.add_message(request, messages.INFO,
                             "The page you are looking for not avaible!")

        return redirect("404")
    if request.user.is_authenticated:
        context["is_Mod"] = request.user.isModerator
    tweets = Tweet.objects.filter(user=userId).order_by("-createdAt")
    user1 = AppUser.objects.filter(id=userId).first()
    if request.method == "POST":

        form = MessageForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = user1
            message.save()
            messages.add_message(request, messages.SUCCESS, "Message sent")

            return redirect("profile", user1.id)

    userFollow = Follow.objects.filter(
        takipEden=request.user) & Follow.objects.filter(takipEdilen=user1)
    context["userFollow"] = userFollow

    postLikes = PostLikes.objects.all()
    context["postLikes"] = postLikes
    context["user"] = user1
    context["tweets"] = tweets
    comments = Comment.objects.all()
    context["comments"] = comments
    context["form"] = MessageForm
    context["form1"] = CommentForm
    return render(request, "profile.html", context)


def reports(request):
    context = {}
    if request.user.is_authenticated == False:
        messages.add_message(request, messages.INFO,
                             "The page you are looking for not avaible!")

        return redirect("404")
    reports = Report.objects.all()
    context["reports"] = reports

    return render(request, "reports.html", context)


def error(request):
    return render(request, "404.html")


def trends(request):
    context = {}
    likedtweets = Tweet.objects.extra(
        select={'sum':
                'likeQuatity + commentQuatity'}, order_by=('-sum', ))[:4]
    if request.user.is_authenticated:
        context["is_Mod"] = request.user.isModerator
    context["tweets"] = likedtweets
    bestAccounts = AppUser.objects.filter(
        is_active=True).order_by("-takipciSayisi")[:4]
    context["users"] = bestAccounts
    postLikes = PostLikes.objects.all()
    context["postLikes"] = postLikes
    comments = Comment.objects.all().order_by("-createdAt")
    context["comments"] = comments

    return render(request, "trends.html", context)


def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)

                return redirect("home")
            else:
                messages.add_message(request, messages.INFO, "User not found")
                return redirect("login")
        else:
            messages.add_message(request, messages.INFO, "User not found")
            return redirect("login")
    else:
        return render(request, "login.html")


def log_out(request):
    logout(request)
    return redirect("home")


def register(request):
    context = {}
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        avatar = request.FILES.get("avatar")
        form = RegisterForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.avatar = avatar
            user.save()
            messages.add_message(request, messages.INFO,
                                 "Registration Successful")
            return redirect("login")
        else:
            return redirect("register")

    else:
        context["form"] = RegisterForm
        return render(request, "register.html", context)


def updateProfile(request, userId):
    context = {}
    user = AppUser.objects.filter(id=userId).first()
    if request.user.is_authenticated == False:
        messages.add_message(request, messages.INFO,
                             "The page you are looking for not avaible!")
        return redirect("404")
    if request.user.id != user.id and request.user.is_superuser == False:
        messages.add_message(request, messages.INFO,
                             "The page you are looking for not avaible!")
        return redirect("404")

    if user:
        form = UpdateForm(instance=user)
        context["form"] = form
        context["user"] = user

    if request.method == "POST":

        form = UpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form = form.save(commit=False)

            form.save()
            messages.add_message(request, messages.INFO, "Update successful")

            return redirect("profile", user.id)
        else:
            return redirect("upProfile", user.id)
    else:
        return render(request, "updateProfile.html", context)


def deleteTweet(request, tweetId):
    tweet = Tweet.objects.filter(id=tweetId).first()

    if request.user.is_authenticated == False:
        messages.add_message(request, messages.INFO,
                             "The page you are looking for not avaible!")
        return redirect("404")
    if request.user.id != tweet.user.id and request.user.is_superuser == False and request.user.isModerator == False:
        messages.add_message(request, messages.INFO,
                             "The page you are looking for not avaible!")
        return redirect("404")

    if tweet:
        tweet.delete()

        messages.add_message(request, messages.SUCCESS,
                             "Tweet was successfully deleted")
        return redirect("home")
    else:
        return redirect("home")


def deleteProfile(request, userId):
    user = AppUser.objects.filter(id=userId).first()
    if request.user.is_authenticated == False:
        messages.add_message(request, messages.INFO,
                             "The page you are looking for not avaible!")
        return redirect("404")
    if request.user.id != user.id and request.user.is_superuser == False:
        messages.add_message(request, messages.INFO,
                             "The page you are looking for not avaible!")
        return redirect("404")
    if user:
        user.is_active = False
        user.save()
        messages.add_message(request, messages.INFO,
                             "User was successfully deleted")
        return redirect("home")


def updateTweet(request, tweetId):
    context = {}
    tweet = Tweet.objects.filter(id=tweetId).first()
    if request.user.is_authenticated == False:
        messages.add_message(request, messages.INFO,
                             "The page you are looking for not avaible!")
        return redirect("404")
    if request.user.id != tweet.user.id and request.user.is_superuser == False and request.user.isModerator == False:
        messages.add_message(request, messages.INFO,
                             "The page you are looking for not avaible!")
        return redirect("404")

    if tweet:
        form = TweetUpdateForm(instance=tweet)
        context["form"] = form
        context["tweet"] = tweet

    if request.method == "POST":

        form = TweetUpdateForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid:
            form = form.save(commit=False)
            form.user = tweet.user
            form.save()
            messages.add_message(request, messages.INFO, "Update successful")
            return redirect("home")
    else:

        return render(request, "updateTweet.html", context)


def tweetDetail(request, tweetId):
    context = {}
    tweet = Tweet.objects.filter(id=tweetId).first()
    allComments = Comment.objects.filter(
        tweet_id=tweetId).order_by("-createdAt")
    context["allComments"] = allComments
    if request.user.is_authenticated:
        context["is_Mod"] = request.user.isModerator
    if tweet:
        context["tweet"] = tweet

    if request.method == "POST":

        form = CommentForm(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            form.author = request.user
            form.tweet = tweet
            form.save()

            commentCount = tweet.commentQuatity + 1
            comment = Tweet.objects.get(id=tweetId)
            comment.commentQuatity = commentCount
            comment.save(update_fields=['commentQuatity'])
            messages.add_message(request, messages.INFO, "Comment created")
            return redirect("tweetDetail", comment.id)
    else:
        context["form"] = CommentForm
        return render(request, "tweetDetail.html", context)


def addLike(request, userId, tweetId):
    if request.user.is_authenticated == False:
        return redirect("404")

    user = AppUser.objects.filter(id=userId).first()
    tweet = Tweet.objects.filter(id=tweetId).first()
    is_liked = PostLikes.objects.filter(user=user) & PostLikes.objects.filter(
        tweet=tweet)

    if is_liked:

        likeCount = tweet.likeQuatity - 1
        like = Tweet.objects.get(id=tweetId)
        like.likeQuatity = likeCount
        like.save(update_fields=['likeQuatity'])
        is_liked.delete()
        return redirect("home")

    if user and tweet:
        PostLikes.objects.create(user=user, tweet=tweet)
        likeCount = tweet.likeQuatity + 1
        like = Tweet.objects.get(id=tweetId)
        like.likeQuatity = likeCount
        like.save(update_fields=['likeQuatity'])

        return redirect("home")


def updatePassword(request, userId):
    user = AppUser.objects.filter(id=userId).first()
    if request.user.is_authenticated == False:
        return redirect("404")
    if request.user.id != user.id and request.user.is_superuser == False:
        return redirect("404")
    if request.method == "POST":
        password = request.POST.get("password")

        if password:
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.INFO, "Update successful")
            return redirect("login")

        else:
            return redirect("profile", user.id)

    else:
        return render(request, "updatePassword.html")


def userBan(request, userId, reportId):
    if request.user.is_superuser == False:
        return redirect("404")

    user = AppUser.objects.filter(id=userId).first()
    report = Report.objects.filter(id=reportId).first()

    if user:
        user.is_active = False
        user.save()
        report.delete()
        messages.add_message(request, messages.INFO,
                             "User was successfully deleted")
        return redirect("reports")


def deleteReport(request, reportId):
    if request.user.is_superuser == False:
        return redirect("404")

    report = Report.objects.filter(id=reportId).first()

    if report:
        report.delete()
        messages.add_message(request, messages.INFO,
                             "Report was successfully deleted")
        return redirect("reports")
    else:
        return redirect("home")


def updateComment(request, commentId, tweetId):
    context = {}
    tweet = Tweet.objects.filter(id=tweetId).first()
    comment = Comment.objects.filter(id=commentId).first()
    if request.user.is_superuser == False and request.user.id != comment.author.id and request.user.isModerator == False:
        return redirect("404")
    if comment:
        form = UpdateCommentForm(instance=comment)
        context["form"] = form
        context["tweet"] = tweet
        context["comment"] = comment

    if request.method == "POST":

        form = UpdateCommentForm(request.POST, instance=comment)
        if form.is_valid:
            form = form.save(commit=False)
            form.author = comment.author
            form.tweet = tweet
            form.save()
            messages.add_message(request, messages.INFO, "Update successful")
            return redirect("tweetDetail", tweet.id)
    else:
        return render(request, "updateComment.html", context)


def reportTweet(request, tweetId, userId):
    context = {}
    tweet = Tweet.objects.filter(id=tweetId).first()
    user = AppUser.objects.filter(id=userId).first()
    if request.user.is_authenticated == False:
        return redirect("404")
    if tweet:
        form = ReportForm()
        context["reportform"] = form
        context["reporttweet"] = tweet

    if request.method == "POST":

        form = ReportForm(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            form.sender = user
            form.tweet = tweet
            form.save()
            messages.add_message(request, messages.INFO, "Report created")
            return redirect("home")
    else:
        context["reportform"] = ReportForm
        return render(request, "reportTweet.html", context)


def deleteComment(request, commentId, tweetId):
    comment = Comment.objects.filter(id=commentId).first()
    if request.user.is_superuser == False and request.user.id != comment.author.id and request.user.isModerator == False:
        return redirect("404")
    if comment:

        tweet = Tweet.objects.filter(id=tweetId).first()

        commentCount = tweet.commentQuatity - 1
        tweet1 = Tweet.objects.get(id=tweetId)
        tweet1.commentQuatity = commentCount
        tweet1.save(update_fields=['commentQuatity'])
        comment.delete()
        messages.add_message(request, messages.INFO,
                             "Comment was successfully deleted")
        return redirect("tweetDetail", comment.tweet.id)
    else:
        return redirect("home")


def addFollow(request, takipEdenId, takipEdilenId):
    if request.user.is_authenticated == False:
        return redirect("404")

    takipEden = AppUser.objects.filter(id=takipEdenId).first()
    takipEdilen = AppUser.objects.filter(id=takipEdilenId).first()
    if request.user.id != takipEden.id:
        return redirect("404")
    is_follow = Follow.objects.filter(
        takipEden__username=takipEden.username) & Follow.objects.filter(
            takipEdilen__username=takipEdilen.username)
    if is_follow:
        newFollowerCount = takipEden.takipEdilenSayisi - 1
        takipEden = AppUser.objects.get(id=takipEdenId)
        takipEden.takipEdilenSayisi = newFollowerCount
        takipEden.save(update_fields=['takipEdilenSayisi'])

        newFollowCount = takipEdilen.takipciSayisi - 1
        takipEdilen = AppUser.objects.get(id=takipEdilenId)
        takipEdilen.takipciSayisi = newFollowCount
        takipEdilen.save(update_fields=['takipciSayisi'])
        is_follow.delete()

        return redirect("home")

    if takipEden and takipEdilen:
        Follow.objects.create(takipEden=takipEden, takipEdilen=takipEdilen)
        newFollowerCount = takipEden.takipEdilenSayisi + 1
        takipEden = AppUser.objects.get(id=takipEdenId)
        takipEden.takipEdilenSayisi = newFollowerCount
        takipEden.save(update_fields=['takipEdilenSayisi'])

        newFollowCount = takipEdilen.takipciSayisi + 1
        takipEdilen = AppUser.objects.get(id=takipEdilenId)
        takipEdilen.takipciSayisi = newFollowCount
        takipEdilen.save(update_fields=['takipciSayisi'])

        return redirect("home")


def privateMessages(request):
    if request.user.is_authenticated == False:
        return redirect("404")

    messages = Message.objects.filter(
        sender=request.user).order_by("-createdAt")
    recipients = Message.objects.filter(
        recipient=request.user).order_by("-createdAt")
    context = {}
    print(type(messages), recipients)

    if messages or recipients:
        context["messages"] = messages
        context["recipients"] = recipients

        return render(request, "messages.html", context)
    else:
        return render(request, "messages.html", context)


def requests(request):
    if request.user.is_superuser == False:
        return redirect("404")

    users = AppUser.objects.filter(is_Confirm=False) & AppUser.objects.filter(
        is_active=True)
    moderatorsRequests = AppUser.objects.filter(
        groups__isnull=True) & AppUser.objects.filter(is_Confirm=True)
    context = {}

    if users or moderatorsRequests:
        context["users"] = users
        context["moderators"] = moderatorsRequests

        return render(request, "Requests.html", context)
    else:
        return render(request, "Requests.html", context)


def confirmUser(request, userId):
    user = AppUser.objects.filter(id=userId).first()
    if request.user.is_superuser == False:
        return redirect("404")
    if user:
        user.is_Confirm = True
        user.save()
        return redirect("requests")


def createMod(request, userId):
    user = AppUser.objects.filter(id=userId).first()
    if request.user.is_superuser == False:
        return redirect("404")
    if user:
        modRole, id = Group.objects.get_or_create(name="Mod")
        user.groups.add(modRole)
        return redirect("requests")


def messageDetail(request, messageId):
    dm = Message.objects.filter(id=messageId).first()
    if dm.is_Read == False:
        dm.is_Read = True
        dm.save()
        print("true")

    context = {}
    context["dm"] = dm
    context["form"] = MessageForm
    return render(request, "messageDetail.html", context)
