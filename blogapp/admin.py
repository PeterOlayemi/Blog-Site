from django.contrib import admin
from .models import BlogModel, CommentModel, User

admin.site.register(BlogModel)
admin.site.register(CommentModel)
admin.site.register(User)