from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Idea

class IdeaSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Idea
        fields = ('id', 'body', 'created_by', 'created_at_formatted',)