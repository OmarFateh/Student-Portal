from django.contrib import admin

from .models import Question, Answer


# models admin site registeration
admin.site.register(Question)
admin.site.register(Answer)