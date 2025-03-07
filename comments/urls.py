from django.urls import path
from .views import blog_detail, add_comment, like_comment, delete_comment,add_reply,edit_comment
app_name = "comments"
urlpatterns = [
    path("<int:blog_id>/", blog_detail, name="blog_detail"),
    path("add_comment/<int:blog_id>/", add_comment, name="add_comment"),
    path("like_comment/<int:comment_id>/", like_comment, name="like_comment"),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('add_reply/<int:comment_id>/', add_reply, name='add_reply'),
	path("edit_comment/<int:comment_id>/", edit_comment, name="edit_comment"),

  ]
