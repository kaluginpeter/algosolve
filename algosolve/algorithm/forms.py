from django.contrib.auth.forms import UserChangeForm
from .models import User


class ChangeUserNameForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')