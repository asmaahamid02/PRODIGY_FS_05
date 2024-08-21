from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from followers.models import Follower

@login_required
def follow_view(request: HttpRequest, username:str) -> HttpResponse | JsonResponse:
    if request.method == 'POST':
        inputs = request.POST.dict()

        if "action" not in inputs:
            return HttpResponseBadRequest("Action is required to follow/unfollow")

        if inputs["action"] not in ["follow", "unfollow"]:
            return HttpResponseBadRequest("Action is invalid")
        
        try:
            other_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponseBadRequest("User not found!")    

        if request.user == other_user:
            return HttpResponseBadRequest("Cannot follow yourself")            
        
        if inputs["action"] == 'follow':
            follower, created = Follower.objects.get_or_create(
                followed_by = request.user,
                following = other_user
            )

            if created:
                return JsonResponse({
                    "status": "success",
                    "message": f"You followed {other_user.username}",
                    "data":{
                        "wording": "Unfollow"
                    }
                })
        else:
            follower = Follower.objects.filter(
                followed_by = request.user,
                following = other_user
            )
            
            if follower.exists():
                follower.delete()

                return JsonResponse({
                    "status": "success",
                    "message": f"You unfollowed {other_user.username}",
                    "data":{
                        "wording": "Follow"
                    }
                })                

        return HttpResponseBadRequest(f"An error occurred while {inputs['action']}ing {other_user.username}. Try again!")
