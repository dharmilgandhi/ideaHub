from rest_framework import serializers
from .models import Community

class CommunitySerializer(serializers.ModelSerializer):
    
    members_count = serializers.IntegerField(source='members.count', read_only=True)

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'created_by', 'members_count', 'created_at', 'updated_at']

