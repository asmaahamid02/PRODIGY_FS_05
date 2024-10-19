from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import Comment
from posts.models import Post
from .forms import CommentForm
from interactions.models import Like



@login_required
def comment_list_view(request: HttpRequest, post_id: int) -> HttpResponse:
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        post = None

    if post:
        comments = Comment.objects.filter(post=post)

        if not comments:
            comments = []

        return render(request, 'components/comments-list.html', {"comments": comments}, content_type='application/html')

    return JsonResponse({'errors': ['Post not found']}, status=400)


@login_required
def comment_create_view(request: HttpRequest, post_id: int) -> HttpResponse:
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                post = None

            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            return render(request, 'components/comment-card.html', {"comment": comment}, content_type='application/html')    
        return JsonResponse({'errors': list(form.errors.values())}, status=400)    
    return JsonResponse({'errors': ['Comment could not be created, try again']}, status=405)

@login_required
def comment_delete_view(request: HttpRequest, comment_id: int) -> HttpResponse:
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            comment = None

        if comment and comment.author == request.user:
            comment.delete()
            return JsonResponse({'success': True}, status=200)

    return JsonResponse({'errors': ['Comment could not be deleted, try again']}, status=405)

@login_required
def like_dislike_view(request: HttpRequest, post_id: int) -> HttpResponse:
    if request.method == 'POST':
        inputs = request.POST.dict()

        if "action" not in inputs:
            return HttpResponseBadRequest("Action is required to like/unlike")

        if inputs["action"] not in ["like", "unlike"]:
            return HttpResponseBadRequest("Action is invalid")
    
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            post = None

        if post:
            if inputs["action"] == 'like':
                like , created = Like.objects.get_or_create(post=post, user=request.user)

                if created:
                    return JsonResponse({'success': True}, status=200)
            else:
                like = Like.objects.filter(post=post, user=request.user).first()
                if like:
                    like.delete()
                    return JsonResponse({'success': True}, status=200)
        
    return JsonResponse({'errors': [f'Could not {inputs["action"]} the post']}, status=400)
