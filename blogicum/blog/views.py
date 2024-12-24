from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Now
from django.db.models import Count

from .models import Post, Category
from .constants import MAX_POSTS


class PostListView(ListView):
    model = Post
    paginate_by = MAX_POSTS
    template_name = 'blog/index.html'

    def get_queryset(self):
        queryset = Post.objects.filter(
            is_published=True,
            pub_date__lte=Now(),
            category__is_published=True
        ).select_related('author').prefetch_related(
            'category', 'location').annotate(
                comment_count=Count('comments')
        )

        return queryset


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
