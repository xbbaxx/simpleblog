from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required



def Index(request):
    postAll = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    paginator = Paginator(postAll, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts':posts, 'page':True})



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form}) 


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog.views.post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog.views.Index')


def post_search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            return redirect('blog.views.Index')
        else:
            postAll = Post.objects.filter(title__icontains = q).order_by('-published_date')
            if len(postAll) == 0 :
                return render(request,'blog/post_search.html', {'posts' : postAll, 'error' : True})
            else :
                paginator = Paginator(postAll, 10)
                page = request.GET.get('page')
                try:
                    posts = paginator.page(page)
                except PageNotAnInteger:
                    posts = paginator.page(1)
                except EmptyPage:
                    posts = paginator.page(paginator.num_pages)
                return render(request,'blog/post_search.html', {'posts' : posts, 'page' : True, 'q' : q, 'error' : False})
    return redirect('blog.views.Index')




def search_tag(request, tag):
    postAll = Post.objects.filter(tag__iexact=tag).order_by('-published_date')   
    if len(postAll) == 0 :
        return render(request,'blog/search_tag.html', {'posts' : postAll, 'error' : True})
    else :
        paginator = Paginator(postAll, 10)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
                posts = paginator.page(1)
        except EmptyPage:
                posts = paginator.page(paginator.num_pages)
        return render(request,'blog/search_tag.html', {'posts' : posts, 'page' : True, 'error' : False})

