from django.contrib import admin

from .models import (Category,
                     Algorithm,
                     ImageAlgorithm,
                     ImageCategory,
                     Comment)

admin.site.register(Category)
admin.site.register(Algorithm)
admin.site.register(ImageAlgorithm)
admin.site.register(ImageCategory)
admin.site.register(Comment)
