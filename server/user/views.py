from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

import json

# TODO:
# - we don't actually want csrf exempt,
#   DRF is probably a better solution for auth
# 
@csrf_exempt
def index(request):
    if request.user.is_authenticated:
      return JsonResponse({
          "username": request.user.username,
          "isStaff": request.user.is_staff
      })

    return JsonResponse({"error": "not authorized"})


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user = authenticate(
            username=body.get("username"), 
            password=body.get("password")
        )
    if user:
        return JsonResponse({
          "username": request.user.username,
          "isStaff": request.user.is_staff
      })

    return JsonResponse({"error": "not authorized"})


# @csrf_exempt
def logout_user(request):
    # call logout with request.user
    return JsonResponse({ "user": "logged out"})
