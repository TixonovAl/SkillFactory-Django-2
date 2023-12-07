from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import *


class PostsList(ListView):
    queryset = Post.objects.order_by('-date_of_creation')
    template_name = 'news/posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'