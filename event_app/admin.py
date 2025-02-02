from django.contrib import admin
from .models import Event,Category,CustomUser,Registration

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display= ("title","category")

@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ("username","role")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Registration)
class Registration(admin.ModelAdmin):
    list_display = ("event","user")