from django.urls import path
from django.contrib.auth.views import LogoutView
from .forms import CustomLoginView, RegisterPage
from .views import (
ProfileView, PostListView, CreatePostView, CreateCommentView, VotePostView,
VoteCommentView, FollowUserView, UnfollowUserView, PostDetailView,
EditPostView, EditCommentView, DeletePostView, DeleteCommentView
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', PostListView.as_view(), name='posts'),
    path('post/create/', CreatePostView.as_view(), name='create_post'),
    path('post/<int:post_id>/comment/create/', CreateCommentView.as_view(),name='create_comment'),
    path('post/<int:post_id>/vote/', VotePostView.as_view(), name='vote_post'),
    path('comment/<int:comment_id>/vote/', VoteCommentView.as_view(),name='vote_comment'),
    path('user/<str:username>/follow/', FollowUserView.as_view(),name='follow_user'),
    path('user/<str:username>/unfollow/', UnfollowUserView.as_view(),name='unfollow_user'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/edit/', EditPostView.as_view(), name='edit_post'),
    path('comment/<int:comment_id>/edit/', EditCommentView.as_view(),name='edit_comment'),
    path('post/<int:post_id>/delete/', DeletePostView.as_view(),name='delete_post'),
    path('comment/<int:comment_id>/delete/', DeleteCommentView.as_view(), name='delete_comment'),
]