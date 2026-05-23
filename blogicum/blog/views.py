from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

from core.constants import POSTS_BY_PAGE


def published_posts():
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    ).select_related('author', 'location', 'category')


def index(request):
    posts = published_posts()[:POSTS_BY_PAGE]
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(
        published_posts(),
        pk=pk,
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = published_posts().filter(category=category)
    return render(request, 'blog/category.html', {
        'category': category,
        'posts': posts,
    })
