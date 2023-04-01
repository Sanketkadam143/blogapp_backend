from django.contrib import admin
from django.urls import path
from api.views import signup, loginuser, upload_data,user_posts,delete_post,edit_post
from api.middleware import TokenDecodeMiddleware

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup', signup, name='signup'),
    path('api/login', loginuser, name="login"),
    path('api/addblog', TokenDecodeMiddleware(upload_data), name="upload_blog"),
    path('api/allblog',TokenDecodeMiddleware(user_posts),name="posts"),
    path('api/delete',TokenDecodeMiddleware(delete_post),name="delete_posts"),
     path('api/edit',TokenDecodeMiddleware(edit_post),name="edit")
]
