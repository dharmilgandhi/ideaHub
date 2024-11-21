from django.urls import path
from .api import (
    create_community,
    list_communities,
    join_community,
    create_community_post,
    list_community_posts
)

urlpatterns = [
    path('', list_communities, name='list_communities'),
    path('create/', create_community, name='create_community'),
    path('<uuid:community_id>/join/', join_community, name='join_community'),
    path('<uuid:community_id>/posts/', list_community_posts, name='list_community_posts'),
    path('<uuid:community_id>/posts/create/', create_community_post, name='create_community_post'),
]
