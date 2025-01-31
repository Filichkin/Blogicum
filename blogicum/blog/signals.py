from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post, Comment


@receiver(m2m_changed, sender=Post.users_like.through)
def post_users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()


@receiver(m2m_changed, sender=Comment.users_like.through)
def comment_users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()
