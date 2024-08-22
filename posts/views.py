from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from followers.models import Follower

@login_required
def index_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    posts = Post.objects.order_by('-created_at').annotate(
        is_followed = Exists(
            Follower.objects.filter(
                followed_by = user,
                following = OuterRef('author')
            )
        )
    )[:30]
    return render(request, 'posts/index.html', {"posts": posts})

@login_required
def post_create_view(request: HttpRequest) -> HttpResponse | JsonResponse:
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return render(request, 'components/post-card.html', {"post": post}, content_type='application/html')
        else:
            return JsonResponse({'errors': list(form.errors.values())}, status=400)
    else:
        return JsonResponse({'errors': ['Invalid request method']}, status=405)


        