from django.forms import ModelForm

from post.models import Post, PostAttachment


class CommunityPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('subject','body', 'is_private',)


class CommunityAttachmentForm(ModelForm):
    class Meta:
        model = PostAttachment
        fields = ('image',)