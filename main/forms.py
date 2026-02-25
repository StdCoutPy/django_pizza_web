from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from main.models import P_Menu


User = get_user_model()


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

class AddPostForm(forms.ModelForm):
    class Meta():
        model = P_Menu
        fields = ['title','text','photo','which_product','price']
