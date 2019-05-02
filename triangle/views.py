from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import RedirectView
from django.http import HttpResponse, JsonResponse
from .models import Post
from .forms import *
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
import json
from django.db.models import Count
from django.contrib.gis.geoip2 import GeoIP2


#Allows a user to register to the site as a regular user. Redirects to the account setup page
def register(request):
    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            login(request, user)
            user.save()
            return redirect("setup_profile.html")
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, "triangle/user_login.html", {"user_form": user_form})

def setup_profile(request):
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES)
        url_form = FanForm()
        if profile_form.is_valid():
            print("files: " + str(request.FILES))
            profile = profile_form.save(commit = False)
            profile.user = request.user
            print(str(profile.photo.url))
            profile.save()
            return redirect("setup_account.html")
        else:
            print(profile_form.errors)
    else:
        profile_form = ProfileForm()
    return render(request, "triangle/setup_profile.html", {"profile_form": profile_form})

def setup_account(request):
    profile = Profile.objects.get(user = request.user)
    if request.method == "POST":
        if profile.account_type == "fan":
            url_form = FanForm(data = request.POST)
        if profile.account_type == "venue":
            url_form = VenueForm(data = request.POST)
        if profile.account_type == "artist":
            url_form = ArtistForm(data = request.POST)
        if url_form.is_valid():
            urls = url_form.save(commit = False)
            urls.user = request.user
            urls.save()
            return redirect("index.html")
        else:
            print(url_form.errors)
    else:
        if profile.account_type == "fan":
            url_form = FanForm()
        if profile.account_type == "venue":
            url_form = VenueForm()
        if profile.account_type == "artist":
            url_form = ArtistForm()
    return render(request, "triangle/setup_account.html", {"url_form": url_form})

def update_profile(request):
    current_profile = Profile.objects.get(user = request.user)
    if request.method == "POST":
        update_form = ProfileForm(request.POST, request.FILES)
        
        if update_form.is_valid():
            updated_profile = update_form.save(commit = False)
            if updated_profile.bio != "":
                current_profile.bio = updated_profile.bio
            if updated_profile.photo != "":
                current_profile.photo = updated_profile.photo
            if updated_profile.display_name != "":
                current_profile.display_name = updated_profile.display_name
            current_profile.save()
            return redirect("index.html")
    else:
        update_form = ProfileForm()
    return render(request, "triangle/update_profile.html", {"update_form": update_form})

def update_account(request):
    current_profile = Profile.objects.get(user = request.user)
    if request.method == "Post":
        if current_profile.account_type == "artist":
            update_form = ArtistForm(data = request.POST)
            current_account = Artist.objects.get(user = request.user)
        if current_profile.account_type == "venue":
            update_form = VenueForm(data = request.POST)
            current_account = Venue.objects.get(user = request.user)
        if current_profile.account_type == "fan":
            update_form = FanForm(data == request.POST)
            current_account = Fan.objects.get(user = request.user)
        if update_form.is_valid():
            updated_account = update_form.save(commit = False)
            if current_profile.account_type == "artist":
                if updated_account.spotify != "":
                    current_account.spotify = updated_account.spotify
                if updated_account.store != "":
                    current_account.store = updated_account.store
                if updated_account.tickets != "":
                    current_account.tickets = updated_account.tickets
            if current_profile.account_type == "venue":
                if updated_account.store != "":
                    current_account.store = updated_account.tickets
                if updated_account.tickets != "":
                    current_account.store = updated_account.store
                if updated_account.address_one != "":
                    current_account.address_one = updated_account.address_one
                if updated_account.address_two != "":
                    current_account.address_two = updated_account.address_two
                if updated_account.post_code != "":
                    current_account.post_code = updated_account.post_code
            if current_profile.account_type == "fan":
                if updated_account.spotify != "":
                    current_account.spotify = updated_account.spotify
            current_profile.save()
            print("current: " + str(current_profile))
            return redirect("index.html")
        else:
            print(update_form.errors)
    else:
        if current_profile.account_type == "artist":
            update_form = ArtistForm()
        if current_profile.account_type == "venue":
            update_form = VenueForm()
        if current_profile.account_type == "fan":
            update_form = FanForm()
    return render(request, "triangle/update_account.html", {"update_form": update_form})
                

#Allows a user to login to the site before being redirected to the index page
def user_login(request):
    geo = GeoIP2()
    if request.method == "POST":
        login_form = AuthenticationForm(data = request.POST)
        user_form = UserForm(data = request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            profile = Profile.objects.filter(user = user).get()

            try:
                profile.city = geo.city(str(request.META.get("HTTP_X_REAL_IP")))
            except:
                profile.city = "Dublin"
            print("city: " + profile.city)
            profile.save()
            return redirect("index.html")

        if user_form.is_valid():
            user = user_form.save(commit = False)
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect("setup_profile.html")
        else:
            print(user_form.errors, login_form.errors)
    else:
        login_form = AuthenticationForm()
        user_form = UserForm()
    return render(request, "triangle/user_login.html", {"login_form": login_form, "user_form": user_form})

def user_logout(request):
    logout(request)
    return redirect("index.html")

#Displays all posts by accounts a user follows
def index(request):
    geo = GeoIP2()
    
    if request.user.is_authenticated:
        post_form = PostForm(data = request.POST or None)
        latest_posts_list = Post.objects.order_by("-published")[:100]
        popular_posts_list = Post.objects.annotate(count=Count('users_like')).order_by('-count')[:3]

        popular_profile_list = []
        for post in popular_posts_list:
            popular_profile_list.append(Profile.objects.get(user = post.user))

        print("profiles: " + str(popular_profile_list))
        
        latest_comments_list = []
        latest_profile_list = []
        for post in latest_posts_list:
            comment_count = Comment.objects.filter(post = post).count()
            latest_comments_list.append(comment_count)
            latest_profile_list.append(Profile.objects.get(user = post.user))

        if post_form.is_valid():
            post = post_form.save(commit = False)
            post.user = request.user
            post.save()
        else:
            print(post_form.errors)
        
        context = {
                "latest_posts_list": latest_posts_list,
                "latest_comments_list": latest_comments_list,
                "popular_posts_list": popular_posts_list,
                "post_form": post_form,
                "latest_profile_list": latest_profile_list,
                "popular_profile_list": popular_profile_list,
            }
        return render(request, "triangle/index.html", context)
    else:
        return redirect("/triangle/login")

def profile_detail(request, profile_id):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = profile_id)
        post_form = PostForm(data = request.POST or None)
        user_posts_list = Post.objects.filter(user = profile.user).order_by("-published")
        comments_list = []
        current_profile = Profile.objects.get(user = request.user)

        for post in user_posts_list:
            comment_count = Comment.objects.filter(post = post).count()
            comments_list.append(comment_count)
        
        followers = Contact.objects.filter(user_to = Profile.objects.get(user = profile.user))
        following = Contact.objects.filter(user_from = Profile.objects.get(user = profile.user))
        print("followers: " + str(followers))
        if profile.account_type == "artist":
            acc = Artist.objects.get(user = request.user)
        if profile.account_type == "fan":
            acc = Fan.objects.get(user = request.user)
        if profile.account_type == "venue":
            acc = Venue.objects.get(user = request.user)

        if profile.user == request.user:
            if post_form.is_valid():
                post = post_form.save(commit = False)
                post.user = request.user
                post.save()
            else:
                print(post_form.errors)
        else:
            post_form = None

        context = {
            "acc": acc,
            "profile": profile,
            "followers": followers,
            "following": following,
            "user_posts_list": user_posts_list,
            "comments_list": comments_list,
            "post_form": post_form,
            "current_profile": current_profile,
            }
        return render(request, "triangle/profile_detail.html", context)
    else:
        return redirect("/triangle/login")
    
#Shows a post, its comments and likes. Provides a comment and like box
def post_detail(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk = post_id)
        profile = Profile.objects.get(user = post.user)
        if request.method == "POST":
            comment_form = CommentForm(data = request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit = False)
                comment.user = request.user
                comment.post = post
                comment.save()
            return redirect(request.path_info)
        else:
            comment_form = CommentForm()
        return render(request, "triangle/post_detail.html", {"post": post, "comment_form": comment_form, "profile": profile})
    else:
        return redirect("/triangle/login")

@login_required
def following_user(request, user_id):
    profile = Profile.objects.get(user = user_id)
    following = Contact.objects.filter(user_from = Profile.objects.get(user = User.objects.get(id = user_id)))
    return render(request, "triangle/following.html", {"following": following, "profile": profile})

@login_required
def follows_user(request, user_id):
    profile = Profile.objects.get(user = user_id)
    followers = Contact.objects.filter(user_to = Profile.objects.get(user = User.objects.get(id = user_id)))
    return render(request, "triangle/followers.html", {"followers": followers, "profile": profile})

@login_required
def comments(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk = post)
        return render(request, "triangle/comments.html", {"post": post})
    else:
        return redirect("/triangle/login")

@require_POST
def like_post(request):
    if request.user.is_authenticated:
        post_id = request.POST.get("post_id")
        action = request.POST.get("action")
        if post_id:
            try:
                post = Post.objects.get(id = post_id)
                if action == "like": 
                    post.users_like.add(request.user)
                    post.like_count = post.like_count + 1
                else:
                    post.users_like.remove(request.user)
                    post.like_count = post.like_count - 1
                return JsonResponse({"status": "ok"})
            except:
                pass
                return JsonResponse({"status": "ok"})
    else:
        return redirect("/triangle/login")

@login_required
@require_POST
def follow_user(request):
    if request.user.is_authenticated:
        user_id = request.POST.get("id")
        action = request.POST.get("action")
        if user_id and action:
            try:
                user = User.objects.get(id = user_id)
                if action == "follow":
                    print("created")
                    Contact.objects.get_or_create(user_from = Profile.objects.get(user = request.user), user_to = Profile.objects.get(user = user))
                else:
                    print("uncreate")
                    Contact.objects.filter(user_from = Profile.objects.get(user = request.user), user_to = Profile.objects.get(user = user)).delete()
                return JsonResponse({"status": "ok"})
            except User.DoesNotExist:
                return JsonResponse({"status": "ko"})
        return JsonResponse({"status": "ko"})
    else:
        return redirect("/triangle/login")
    
@login_required
def write_post(request):
    if request.method == "POST":
        post_form = PostForm(data = request.POST)
        if post_form.is_valid():
            post = post_form.save(commit = False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect("")
        else:
            print(post_form.errors)
        return redirect(request.path_info)
    else:
        post_form = PostForm()
    return render(request, "triangle/write_post.html", {"post_form": post_form})

def track_user(request):
    city_data = Profile.objects.values('city').annotate(c = Count('city')).order_by('-c')
    login_datetimes = User.objects.values_list('last_login', flat = True)
    print(login_datetimes)
    recent_login = []
    for log in login_datetimes:
        now = datetime.now().date()
        if (now - log.date()).days <= 1:
            recent_login.append("Last Day")
        elif (now - log.date()).days <= 7:
            recent_login.append("Last Week")
        elif (now - log.date()).days <= 14:
            recent_login.append("Last Two Weeks")
        elif (now - log.date()).days <= 31:
            recent_login.append("Last Month")
        else:
            recent_login.append("Not Recent")

    login_count = {}
    login_count["Last Day"] = recent_login.count("Last Day")
    login_count["Last Week"] = recent_login.count("Last Week")
    login_count["Last Two Weeks"] = recent_login.count("Last Two Weeks")
    login_count["Last Month"] = recent_login.count("Last Month")
    login_count["Not Recent"] = recent_login.count("Not Recent")   
    return render(request, "triangle/charts.html", {"city_data": city_data, "login_data": login_count})
