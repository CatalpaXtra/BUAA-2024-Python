from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import BlogCategory, Blog, BlogComment, LikeBlog
from .forms import PubBlogForm
from django.db.models import Q


# Create your views here.
def blog_detail(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    category = BlogCategory.objects.filter(id=blog.category_id).first
    like_blog = blog.likes.filter(user=request.user).exists()
    context = {
        'blog': blog,
        'category': category,
        'like_blog': like_blog,
    }
    return render(request, 'blog/blog_detail.html', context=context)


@require_http_methods(['GET', 'POST'])
@login_required()
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'blog/blog_pub.html', context={"categories": categories})
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({"code": 200, "message": "帖子发布成功！", "data": {"blog_id": blog.id}})
        else:
            print(form.errors)
            return JsonResponse({'code': 400, "message": "帖子信息不全！"})


@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(content=content, blog_id=blog_id, author=request.user)
    return redirect(reverse("blog:blog_detail", kwargs={'blog_id': blog_id}))


@require_GET
def search(request):
    # /search?q=xxx
    q = request.GET.get('q')
    blogs = Blog.objects.filter(Q(title__icontains=q)|Q(content__icontains=q)|Q(category__name__exact=q)).all()
    context = {
        "blogs": blogs,
        'username': request.user.username,
    }
    return render(request, 'blog/blog_search.html', context=context)


def home(request):
    blogs = Blog.objects.all()
    context = {
        "blogs": blogs,
        'username': request.user.username,
    }
    return render(request, 'blog/blog_home.html', context=context)


@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    like, created = LikeBlog.objects.get_or_create(user=request.user, blog=blog)
    if not created:
        like.delete()
    return redirect(reverse("blog:blog_detail", kwargs={'blog_id': blog_id}))


@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    return redirect(reverse("user:history_like"))
    
    