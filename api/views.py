from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Blogs
import jwt
import datetime 
import json

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username', '')
        password = data.get('password', '')
        if username and password:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username already exists'})
            else:
                user = User.objects.create_user(username=username, password=password)
                return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@csrf_exempt


def loginuser(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username', '')
        password = data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            payload = {'user_id': user.id,'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),}
            jwt_token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')
            return JsonResponse({'success': True, 'token': jwt_token})
    raise Http404('Invalid username or password.')

@csrf_exempt
def upload_data(request):
    if request.method == 'POST':
       
        user = request.user
        data = json.loads(request.body.decode('utf-8'))
       
        image_data = data.get('image', '')
       
     
        text = data.get('text', '')
      
        timestamp = datetime.datetime.utcnow()
      
        upload = Blogs(user=user, image=image_data, text=text, timestamp=timestamp)
        upload.save()
       
        return JsonResponse({'success': True})
   
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def user_posts(request):
    user = request.user
    blogs = Blogs.objects.filter(user=user)
    data = {'posts': []}
    for blog in blogs:
        post = {'id': blog.id, 'image': blog.image, 'text': blog.text, 'timestamp': blog.timestamp}
        data['posts'].append(post)
    return JsonResponse(data)

    
@csrf_exempt
def delete_post(request):
    user = request.user
    post_id = request.GET.get('id')
    blog = get_object_or_404(Blogs, id=post_id, user=user)
    blog.delete()
    return JsonResponse({'success': True})


@csrf_exempt
def edit_post(request):
    if request.method == 'POST':
       
        user = request.user
        post_id = request.GET.get('id') 
        data = json.loads(request.body.decode('utf-8'))
        
        if not post_id:
            return JsonResponse({'success': False, 'error': 'Post ID missing'})
        try: 
            blog = Blogs.objects.get(id=post_id, user=user)
        except Blogs.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found or unauthorized'})  
        image_data = data.get('image', '')
        text = data.get('text', '')
        
        if image_data:
            blog.image = image_data
        
        if text:
            blog.text = text
        
        blog.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

