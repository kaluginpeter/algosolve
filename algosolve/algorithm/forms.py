from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm


from .models import User, Comment


class ChangeUserNameForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
