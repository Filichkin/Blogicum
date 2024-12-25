from django.db.models.functions import Now
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import User


def posts_queryset(objects_manager):
    queryset = objects_manager.filter(
        is_published=True,
        pub_date__lte=Now(),
        category__is_published=True
    ).select_related('author').prefetch_related(
        'category', 'location').order_by('-pub_date').annotate(
            comment_count=Count('comments')
    )
    return queryset


def get_user(username):
    return get_object_or_404(User, username=username)
