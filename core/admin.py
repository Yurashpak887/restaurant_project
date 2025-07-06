from django.contrib import admin
from .models import CustomUser, MenuItem, Order
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'delivery_time', 'created_at')
    filter_horizontal = ('items',)  # Щоб зручно вибирати багато страв
