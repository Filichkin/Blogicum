from django.views.generic import ListView, CreateView
from django.views.generic import UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .constants import MAX_POSTS
from .forms import CommentForm, PostForm, UserProfileForm
from .mixins import CommentMixin, OnlyAuthorMixin
from .models import Post, Category, Comment
from .utils import get_user, get_user_posts, posts_queryset


class PostListView(ListView):
    model = Post
    paginate_by = MAX_POSTS
    template_name = 'blog/index.html'

    def get_queryset(self):
        return posts_queryset(Post.objects)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.object.author.username
        return reverse('blog:profile', args=[username])


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        if not self.test_func():
            return redirect(reverse(
                'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
            ))

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PostForm(instance=self.get_object())
        context['form'] = form
        return context

    def get_success_url(self):
        return reverse_lazy(
            'blog:index'
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        if (post.author == self.request.user or (post.is_published
           and post.category.is_published)):
            return post
        raise Http404('Страница не найдена')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.all().order_by('created_at')
        context['form'] = CommentForm()
        context['comments'] = comments
        return context


class CategoryPostsView(ListView):
    model = Post
    paginate_by = MAX_POSTS
    template_name = 'blog/category.html'

    def get_category(self, **kwargs):
        return get_object_or_404(
            Category, slug=self.kwargs['category_slug'],
            is_published=True
        )

    def get_queryset(self):
        return posts_queryset(self.get_category().posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        post_id = self.kwargs.get('post_id')
        return reverse('blog:post_detail', kwargs={'post_id': post_id})

    def form_valid(self, form):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditCommentView(CommentMixin, UpdateView):
    form_class = CommentForm
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comment, id=comment_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs.get('post_id')
        return context


class DeleteCommentView(CommentMixin, DeleteView):
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        post_id = self.kwargs.get('post_id')
        return reverse_lazy('blog:post_detail', kwargs={'post_id': post_id})


class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = MAX_POSTS

    def get_queryset(self):
        profile = get_user(self.kwargs.get('username'))
        return get_user_posts(profile.posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile' not in context:
            context['profile'] = get_user(self.kwargs.get('username'))
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'blog/user.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.object.username}
        )

    def get_object(self):
        return self.request.user


@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Post.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})
