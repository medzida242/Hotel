from django.contrib import admin
from .models import *
from .models import Comment

# Register your models here.

admin.site.register(MyUser)

admin.site.register(Mjesto)
admin.site.register(Hotel)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass