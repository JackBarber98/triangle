from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "triangle"
urlpatterns = [

        path("login", views.user_login, name = "user_login"),
        path("logout", views.user_logout, name="logout"),
        path("setup_profile.html", views.setup_profile, name = "setup_profile"),
        path("setup_account.html", views.setup_account, name = "setup_account"),
        path("update_profile.html", views.update_profile, name = "update_profile"),
        path("update_account.html", views.update_account, name = "update_account"),
        path("index.html", views.index, name = "index"),
        path("post/<int:post_id>/", views.post_detail, name = "post_detail"),
        path("like/", views.like_post, name = "like"),
        path("users/follow", views.follow_user, name = "follow_user"),
        path("following/<int:user_id>/", views.following_user, name = "following_user"),
        path("follows/<int:user_id>/", views.follows_user, name = "follows_user"),
        path("profile/<int:profile_id>/", views.profile_detail, name = "profile_detail"),
        path("write_post/", views.write_post, name = "write_post"),
        path("charts.html", views.track_user, name = "charts"),
    ]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
