from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify

class Profile(models.Model):
    ACCOUNT_CHOICES = (("fan", "Fan"), ("artist", "Artist"), ("venue", "Venue"))
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    account_type = models.CharField(max_length = 6, choices = ACCOUNT_CHOICES, default = "Fan", blank = False)
    display_name = models.CharField(max_length = 50, blank = False)
    bio = models.TextField(max_length = 200, blank = True)
    photo = models.ImageField(upload_to = "media", blank = True)
    city = models.CharField(max_length = 25)
    
    def __str__(self):
        return self.user.username

class Contact(models.Model):
    user_from = models.ForeignKey(Profile, related_name = "rel_from_set", on_delete = models.CASCADE)
    user_to = models.ForeignKey(Profile, related_name = "rel_to_set", on_delete = models.CASCADE)
    created = models.DateTimeField(default = datetime.now)

    class Meta:
        ordering = ("-created",)

User.add_to_class("following", models.ManyToManyField("self", through = Contact, related_name = "followers", symmetrical = False))

class Fan(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    spotify = models.URLField(max_length = 200, blank = True)

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    spotify = models.URLField(max_length = 200, blank = True)
    store = models.URLField(max_length = 200, blank = True)
    tickets = models.URLField(max_length = 200, blank = True)

class Venue(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    store = models.URLField(max_length = 200, blank = True)
    tickets = models.URLField(max_length = 200, blank = True)
    address_one = models.CharField(max_length = 150, blank = False)
    address_two = models.CharField(max_length = 150, blank = False)
    post_code = models.CharField(max_length = 8, blank = False)
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post_content = models.TextField(max_length = 500, blank = False)
    published = models.DateTimeField("date_published", default = datetime.now)
    slug = models.SlugField(max_length = 200, blank = True)
    created = models.DateField(default = datetime.now)
    users_like = models.ManyToManyField(User, related_name = "posts_liked", blank = True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.created)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id, self.slug])

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, blank = False)
    comment_text = models.TextField(max_length = 200)
    published = models.DateTimeField("date_published", default = datetime.now)
    
