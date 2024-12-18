from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer
from notification.utils import create_notification

from .forms import PostForm, AttachmentForm
from .models import Post, Like, Comment, Trend, Dislike
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer
from django.utils.timezone import now

@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    posts = posts.filter(community__isnull=True)
    trend = request.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#' + trend).filter(is_private=False)

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.filter(Q(is_private=False)).get(pk=pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })


@api_view(['GET'])
def post_list_profile(request, id):   
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
    }, safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        
        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Error while creating a post'})
    
@api_view(['POST'])
def post_edit(request, pk):
    try:
        post = Post.objects.filter(created_by=request.user).get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found or you are not authorized to edit this post.'}, status=404)

    form = PostForm(request.POST, instance=post)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()



    if form.is_valid():
        updated_post = form.save(commit=False)
        updated_post.created_at = now()
        updated_post.save()

        if attachment:
            post.attachments.add(attachment)
            
        serializer = PostSerializer(updated_post)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid data provided.'}, status=400)

@api_view(['POST'])
def bookmark_post(request,pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.bookmark.all():
        post.bookmark.remove(request.user)
        return JsonResponse({'message': 'Bookmark removed'})
    else:
        post.bookmark.add(request.user)
        return JsonResponse({'message': 'Bookmark created'})
        
@api_view(['GET'])
def get_user_bookmarks(request):

    posts = Post.objects.all()
    posts = Post.objects.filter(bookmark = request.user)
    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by=request.user):
        if post.dislikes.filter(created_by=request.user):
            post.dislikes_count = post.dislikes_count - 1
            post.save()
            Dislike.objects.filter(created_by=request.user).delete()
        like = Like.objects.create(created_by=request.user)

        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        notification = create_notification(request, 'post_like', post_id=post.id)

        return JsonResponse({'message': 'like created'})
    else:
        return JsonResponse({'message': 'post already liked'})
    
@api_view(['POST'])
def post_dislike(request, pk):
    post = Post.objects.get(pk=pk)

    if not post.dislikes.filter(created_by=request.user):
        if post.likes.filter(created_by=request.user):
            post.likes_count = post.likes_count - 1
            post.save()
            Like.objects.filter(created_by=request.user).delete()
        dislike = Dislike.objects.create(created_by=request.user)

        post = Post.objects.get(pk=pk)
        post.dislikes_count = post.dislikes_count + 1
        post.dislikes.add(dislike)
        post.save()

        notification = create_notification(request, 'post_dislike', post_id=post.id)

        return JsonResponse({'message': 'Post Dislike'})
    else:
        return JsonResponse({'message': 'post already disliked'})


@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    notification = create_notification(request, 'post_comment', post_id=post.id)

    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)


@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()

    return JsonResponse({'message': 'post deleted'})


@api_view(['POST'])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by_users.add(request.user)
    post.save()

    return JsonResponse({'message': 'post reported'})


@api_view(['GET'])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)

    return JsonResponse(serializer.data, safe=False)