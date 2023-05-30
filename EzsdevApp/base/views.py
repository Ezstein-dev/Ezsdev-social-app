from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Profile, Post, Comment, Vote, Follow
from django.urls import reverse_lazy

class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'base/profile.html'
    context_object_name = 'profile'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.request.user)
        return context
    
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "posts"
    template_name = "post_list.html"
    ordering = ["-created_at"]
    paginate_by = 10
    
class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create_post.html'
    fields = ['post_text', 'post_image', 'post_video']
    success_url = reverse_lazy('posts')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'create_comment.html'
    fields = ['comment_text', 'comment_image', 'comment_video']
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.kwargs['post_id']})
        
class VotePostView(LoginRequiredMixin, CreateView):
    model = Vote
    fields = ['post']
    template_name = 'vote_post.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.kwargs['post_id']})
        
class VoteCommentView(LoginRequiredMixin, CreateView):
    model = Vote
    fields = ['comment']
    template_name = 'vote_comment.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.comment = get_object_or_404(Comment,
        pk=self.kwargs['comment_id'])
        return super().form_valid(form)
    def get_success_url(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        return reverse_lazy('post_detail', kwargs={'post_id': comment.post.id})
    
class FollowUserView(LoginRequiredMixin, CreateView):
    model = Follow
    fields = []
    template_name = 'follow_user.html'
    def form_valid(self, form):
        form.instance.follower = self.request.user
        form.instance.followed = get_object_or_404(User,
        username=self.kwargs['username'])
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('profile')
    
class UnfollowUserView(LoginRequiredMixin, DeleteView):
    model = Follow
    template_name = 'unfollow_user.html'
    def get_object(self):
        follower = self.request.user
        followed_user = get_object_or_404(User, username=self.kwargs['username'])
        return get_object_or_404(Follow, follower=follower, followed=followed_user)
    def get_success_url(self):
        return reverse_lazy('profile')
    
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        return context
    
class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'edit_post.html'
    fields = ['post_text', 'post_image', 'post_video']
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.kwargs['post_id']})
        
class EditCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'edit_comment.html'
    fields = ['comment_text', 'comment_image', 'comment_video']
    def get_success_url(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        return reverse_lazy('post_detail', kwargs={'post_id': comment.post.id})
    
class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('posts')
    
class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'delete_comment.html'
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.object.post.id})