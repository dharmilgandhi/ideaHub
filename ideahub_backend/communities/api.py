from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Community
from .serializers import CommunitySerializer
from post.models import Post
from post.serializers import PostSerializer
from .forms import CommunityAttachmentForm, CommunityPostForm

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_community(request):
    data = request.data
    data['created_by'] = request.user.id
    serializer = CommunitySerializer(data=data)
    print(serializer)
    print(data)
    if serializer.is_valid():
        community = serializer.save()
        community.members.add(request.user)  # Add the creator as the first member
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_communities(request):
    communities = Community.objects.all()
    serializer = CommunitySerializer(communities, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_community(request, community_id):
    try:
        community = Community.objects.get(id=community_id)
        community.members.add(request.user)
        return Response({'message': 'Joined the community successfully.'})
    except Community.DoesNotExist:
        return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_community_post(request, community_id):
    try:
        # Fetch the community
        community = Community.objects.get(id=community_id)

        # Check if the user is a member of the community
        if community not in request.user.communities.all():
            return JsonResponse({'error': 'You are not a member of this community.'}, status=status.HTTP_403_FORBIDDEN)

        # Initialize form with request data
        post_form = CommunityPostForm(request.POST)
        attachment_form = CommunityAttachmentForm(request.POST, request.FILES)

        attachment = None

        # Handle attachment creation
        if attachment_form.is_valid():
            attachment = attachment_form.save(commit=False)
            attachment.created_by = request.user
            attachment.save()

        # Handle post creation
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.created_by = request.user
            post.community = community  # Link the post to the community
            post.save()

            if attachment:
                post.attachments.add(attachment)  # Add attachment to the post

            # Update the user's posts count
            user = request.user
            user.posts_count += 1
            user.save()

            # Serialize and return the post
            serializer = PostSerializer(post)
            return JsonResponse(serializer.data, safe=False)

        else:
            return JsonResponse({'error': 'Invalid data in the form.'}, status=status.HTTP_400_BAD_REQUEST)

    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_community_posts(request, community_id):
    try:
        # Fetch the community
        community = Community.objects.get(id=community_id)

        # Check if the user is a member of the community
        if community not in request.user.communities.all():
            return Response({'error': 'You are not a member of this community.'}, status=status.HTTP_403_FORBIDDEN)

        # Get posts related to the community
        posts = Post.objects.filter(community=community).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    except Community.DoesNotExist:
        return Response({'error': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)