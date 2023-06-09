from django.contrib import admin
from .models import ImageUploader,Profile, Cart
# Register your models here.

@admin.register(ImageUploader)
class AdminImageUploader(admin.ModelAdmin):
        list_display = ['id','image_name','image','user','user_profile','date','price']

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
        list_display = ['id','user','image']
        list_editable = ('user',)
        list_filter = ['user']
        search_fields = ['user','image']

@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['image','image_id', 'image_name']