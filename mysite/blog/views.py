from django.shortcuts import render
from .models import Post

def Index(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})




# Create your views here.
