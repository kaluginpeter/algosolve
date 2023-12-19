from django.forms import ModelForm


from .models import CommentDataStructure




class CommentForm(ModelForm):
    class Meta:
        model = CommentDataStructure
        fields = ('text',)
