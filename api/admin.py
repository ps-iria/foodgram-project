from django.contrib import admin

from .models import Favorite, Follow, Purchase


class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "author")
    list_filter = ("user", "author")


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipe")
    list_filter = ("user", "recipe")


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipe")
    list_filter = ("user", "recipe")


admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Purchase, PurchaseAdmin)
