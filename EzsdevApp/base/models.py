from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    bio = models.TextField(max_length=200, default="Tell us about yourself")
    is_male = models.BooleanField(default=True)
    profile_img = models.ImageField(upload_to="profile_img", default="default.png")

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_text = models.TextField(
        max_length=300,
        blank=True,
        validators=[
            MinValueValidator(
                "0",
                message="At least one of post_text, post_image, or post_video is required.",
            )
        ],
    )
    post_image = models.ImageField(upload_to="post_image", blank=True)
    post_video = models.FileField(upload_to="post_video", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not (self.post_text or self.post_image or self.post_video):
            raise ValidationError(
                "At least one of post_text, post_image, or post_video is required."
            )

    def __str__(self):
        return f"{self.author.username}'s post"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField(
        max_length=300,
        blank=True,
        validators=[
            MinValueValidator(
                "0",
                message="At least one of comment_text, comment_image, or comment_video is required.",
            )
        ],
    )
    comment_image = models.ImageField(upload_to="comment_image", blank=True)
    comment_video = models.FileField(upload_to="comment_video", blank=True)

    def clean(self):
        if not (self.comment_text or self.comment_image or self.comment_video):
            raise ValidationError(
                "At least one of comment_text, comment_image, or comment_video is required."
            )

    def __str__(self):
        return f"{self.author.username} commented on {self.post.author.username}'s post"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        if self.post is None:
            if self.comment is None:
                return "Vote"
            return f"{self.user.username} voted on {self.comment.author.username}'s comment"
        return f"{self.user.username} voted on {self.post.author.username}'s post"


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )
    followed = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="follows",
        default=None,
    )

    def __str__(self):
        return f"{self.user.username} follows {self.profile.user.username}"
