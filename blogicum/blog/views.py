from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Now

from .models import Post, Category
from .constants import MAX_POSTS


def get_posts(post_objects):
    """Посты из БД по условиям ТЗ."""
    return post_objects.filter(
        pub_date__lte=Now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    """Главная страница проекта."""
    template = 'blog/index.html'
    post_list = get_posts(Post.objects)[:MAX_POSTS]
    context = {
        'post_list': post_list
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """Страница отдельной публикации."""
    template = 'blog/detail.html'
    posts = get_object_or_404(
        get_posts(Post.objects),
        id=post_id
    )
    context = {
        'post': posts
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    """Страница категории."""
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = get_posts(category.posts)
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)
