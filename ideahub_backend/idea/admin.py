from django.contrib import admin

# Register your models here.
from .models import Idea, IdeaAttachment

admin.site.register(Idea)
admin.site.register(IdeaAttachment)