import uuid

from django.conf import settings
from django.db import models
from django.utils.timesince import timesince

from account.models import User

# Create your models here.

class IdeaAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='attachments')
    created_by = models.ForeignKey(User, related_name='idea_attachments', on_delete=models.CASCADE)

    def get_image(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        else:
            return ''


class Idea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)

    attachments = models.ManyToManyField(IdeaAttachment, blank=True)

    is_private = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='ideas', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
    
    def created_at_formatted(self):
       return timesince(self.created_at)