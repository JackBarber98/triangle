from django import forms
from .models import *
from django.contrib.auth.models import User
from django.forms import HiddenInput

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta():
        model = User
        fields = ("username", "password", "email")

class ProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ("account_type", "display_name", "bio", "photo",)

class LoginForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ("username", "password")
        widgets = {
            'password': forms.PasswordInput(),
        }

class FanForm(forms.ModelForm):
    class Meta():
        model = Fan
        fields = ("spotify",)

class ArtistForm(forms.ModelForm):
    class Meta():
        model = Artist
        fields = ("spotify", "store", "tickets")

class VenueForm(forms.ModelForm):
    class Meta():
        model = Venue
        fields = ("store", "tickets", "address_one", "address_two", "post_code")

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ("post_content",)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["post_content"].widget.attrs['style'] = "width: 500"
        self.fields["post_content"].widget.attrs["style"] = "height: 500"
        self.fields["post_content"].widget.attrs['style'] = "resize: none"
        self.fields["post_content"].label = ""

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ("comment_text",)

    def __init__(self, *args, **kwargs):        
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields["comment_text"].widget.attrs['style'] = "width: 500"
        self.fields["comment_text"].widget.attrs["style"] = "height: 500"
        self.fields["comment_text"].widget.attrs['style'] = "resize: none"
        self.fields["comment_text"].label = ""
