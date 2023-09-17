from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Question, Answer, Bookmark

admin.site.register(User, UserAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Bookmark)
