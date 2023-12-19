from django.contrib import admin

from .models import (
    CategoryDateStructure,
    DataStructure,
    ImageDataStructure,
    TaskDataStructure,
    CommentDataStructure,
    UrlDataStructure,
)

admin.site.register(CategoryDateStructure)
admin.site.register(DataStructure)
admin.site.register(ImageDataStructure)
admin.site.register(TaskDataStructure)
admin.site.register(CommentDataStructure)
admin.site.register(UrlDataStructure)
