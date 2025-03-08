from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-One link to the User model
    bio = models.TextField(max_length=500, blank=True)  # Optional bio field
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Optional profile picture
    location = models.CharField(max_length=100, blank=True)  # Optional location field
    verified = models.BooleanField(default=False)  # Verified or not

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_blogs", blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def add_like(self, user):
        """Adds a like to the blog and creates a notification."""
        self.likes.add(user)
        Notification.objects.create(
            user=self.author,
            message=f"{user.username} liked your blog: {self.title}"
        )


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name="liked_comments", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.username} - {self.content[:30]}"

    def is_reply(self):
        return self.parent is not None  

    def add_reply(self, user, content):
        """Creates and returns a reply to this comment."""
        reply = Comment.objects.create(user=user, blog=self.blog, parent=self, content=content)
        # Create a notification for the parent comment's author
        Notification.objects.create(
            user=self.user,
            message=f"{user.username} replied to your comment: {self.content[:30]}"
        )
        return reply

    def save(self, *args, **kwargs):
        """Override save to create notifications."""
        is_new = self.pk is None  # Check if the comment is new
        super().save(*args, **kwargs)
        if is_new and not self.is_reply():  # Only notify for new top-level comments
            Notification.objects.create(
                user=self.blog.author,
                message=f"{self.user.username} commented on your blog: {self.blog.title}. Comment: {self.content[:30]}"
            )


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()  # Store the notification message
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"