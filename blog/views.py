from django.shortcuts import render
from django.db.models import Count, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, redirect, reverse
from django.contrib import messages
from .models import Post
from .forms import CommentForm, PostForm
from users.models import Profile


# Create your views here.


def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories'))
    return queryset


def get_author(user):
    qs = Profile.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(author__user__username__icontains=query)
        ).distinct()

    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:4]
    paginator = Paginator(queryset, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count
    }
    return render(request, 'blog.html', context=context)


def blog(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:4]
    post = Post.objects.order_by('-timestamp')
    paginator = Paginator(post, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count
    }
    return render(request, 'blog.html', context)


def blog_single(request, id):
    post = get_object_or_404(Post, id=id)
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:4]
    form = CommentForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            messages.success(request, 'Comment Posted')
            return redirect(request.META['HTTP_REFERER'])
    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form': form
    }

    return render(request, 'blog-single.html', context=context)


def blog_create(request):
    title = "Create"
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.POST:
        if form.is_valid():
            form.instance.author = author
            form.save()
            messages.info(request, "Your Post has created!")
            return redirect(reverse("blog-detail", kwargs={'id': form.instance.id}))
    context = {
        "title": title,
        'form': form
    }
    return render(request, "post-create.html", context)


def blog_update(request, id):
    title = "Update"
    blog_instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None,
                    request.FILES or None,
                    instance=blog_instance
                    )

    if request.POST and request.user.profile == form.instance.author:
        if form.is_valid():
            form.save()
            return redirect(reverse("blog-detail", kwargs={'id': form.instance.id}))
    else:
        context = {
            "title": title,
            'form': form
        }
        return render(request, "post-create.html", context)


def blog_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user.profile == post.author:
        post.delete()
        messages.success(request, "Your Post has been deleted")
        return redirect(reverse("blog"))
    else:
        messages.error(request, "Your not authorised to delete others Post")
        return redirect(reverse("blog"))
