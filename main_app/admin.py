from django.contrib import admin
from .models import Brand, Polish, Review, Photo

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'polish', 'brand', 'review')
admin.site.register(Review, ReviewAdmin)

class PolishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand')
admin.site.register(Polish, PolishAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(Brand, BrandAdmin)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'review')
admin.site.register(Photo, PhotoAdmin)