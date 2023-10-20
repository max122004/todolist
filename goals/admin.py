from django.contrib import admin

from goals.models import GoalCategory


class GoalsCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'update', 'user')
    search_fields = ('title', 'user')


# admin.site.register(GoalsCategoryAdmin, GoalCategory)