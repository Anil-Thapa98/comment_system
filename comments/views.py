from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .models import Comment, Blog


from .models import Profile, Notification, Blog, Comment
from .forms import ProfileUpdateForm

@login_required
def profile(request):
    """Display and update the user's profile."""
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    # Fetch user's blogs, comments, and notifications
    blogs = Blog.objects.filter(author=request.user)
    comments = Comment.objects.filter(user=request.user)
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    
    return render(request, 'profile/profile.html', {
        'form': form,
        'blogs': blogs,
        'comments': comments,
        'notifications': notifications
    })

@login_required
def notifications(request):
    """Display all notifications for the logged-in user."""
    notifications = request.user.notifications.order_by('-timestamp')
    return render(request, 'profile/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    """Mark a notification as read."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('comments:notifications')



def blog_list(request):
    blogs = Blog.objects.all()  # Fetch all blogs    
    # Return the full template for regular requests
    return render(request, 'blog.html', {'blogs': blogs})


# Blog Detail View
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = Comment.objects.filter(blog=blog, parent=None).order_by("-created_at")
    return render(request, "comments/blog_detail.html", {"blog": blog, "comments": comments})

# Add Comment View
@login_required
def add_comment(request, blog_id):
    if request.method == "POST":
        blog = get_object_or_404(Blog, id=blog_id)
        content = request.POST.get("content")
        if content:
            comment = Comment.objects.create(
                content=content,
                user=request.user,
                blog=blog
            )
            # Render the new comment as an HTML fragment
            comment_html = render_to_string("comments/comment.html", {"comment": comment})
            return HttpResponse(comment_html)
        return HttpResponse("Content is required", status=400)
    return HttpResponse("Invalid request method", status=400)

 
@login_required
def add_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            # Include the replied user's username in the reply content
            reply_content = f"@{parent_comment.user.username} {content}"

            # Create the reply
            reply = Comment.objects.create(
                content=reply_content,
                user=request.user,
                blog=parent_comment.blog,  # Ensure it belongs to the same blog
                parent=parent_comment  # Set parent for nested reply
            )

            # Render the reply as an HTML fragment
            reply_html = render_to_string("comments/reply.html", {"reply": reply})
            return HttpResponse(reply_html)
    return HttpResponse("Invalid request", status=400)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            comment.content = content
            comment.save()  # Ensure the comment is saved
            # Render the updated comment/reply
            template = "comments/reply.html" if comment.parent else "comments/comment.html"
            comment_html = render_to_string(template, {"comment": comment})
            return HttpResponse(comment_html)
        return HttpResponse("Content is required", status=400)
    return HttpResponse("Invalid request method", status=400)
    

# Delete Comment/Reply View
@login_required
def delete_comment(request, comment_id):
    if request.method == "POST":
        try:
            comment = Comment.objects.get(id=comment_id, user=request.user)
            comment.delete()
            return HttpResponse()  # Return empty response for deletion
        except Comment.DoesNotExist:
            return HttpResponse("Comment not found", status=404)
    return HttpResponse("Invalid request method", status=400)

# Like Comment/Reply View
@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True

    # Render the updated like button
    like_button_html = render_to_string("comments/like_button.html", {"comment": comment, "liked": liked})
    return HttpResponse(like_button_html)
