from django.contrib import admin

from .models import (Category,
                     Algorithm,
                     ImageAlgorithm,
                     ImageCategory,
                     UrlAlgorithm,
                     UrlCategory,
                     Comment)

admin.site.register(Category)
admin.site.register(Algorithm)
admin.site.register(ImageAlgorithm)
admin.site.register(ImageCategory)
admin.site.register(UrlAlgorithm)
admin.site.register(UrlCategory)
admin.site.register(Comment)
