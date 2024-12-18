from django.urls import path

from . import api


urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('<uuid:pk>/', api.post_detail, name='post_detail'),
    path('<uuid:pk>/like/', api.post_like, name='post_like'),
    path('<uuid:pk>/dislike/', api.post_dislike, name='post_dislike'),
    path('<uuid:pk>/comment/', api.post_create_comment, name='post_create_comment'),
    path('<uuid:pk>/delete/', api.post_delete, name='post_delete'),
    path('<uuid:pk>/report/', api.post_report, name='post_report'),
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    path("bookmark/<uuid:pk>/", api.bookmark_post, name="bookmark_post"),
    path("bookmarks/", api.get_user_bookmarks, name="get_user_bookmarks"),
    path('create/', api.post_create, name='post_create'),
    path('edit/<uuid:pk>/', api.post_edit, name='post_edit'),
    path('trends/', api.get_trends, name='get_trends'),
]