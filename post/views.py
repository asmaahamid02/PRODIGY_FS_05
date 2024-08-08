from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Post

# Create your views here.
def index_view(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.order_by('-created_at').all()[:30]
    return render(request, 'posts/index.html', {"posts": posts})
