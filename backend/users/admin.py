from django.contrib import admin

from users.models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass
