from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@csrf_exempt
def user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            email = data.get("email")

            if not all([username, password, email]):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({"message": "User created successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Missing data"}, status=400)
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            new_email = data.get("email")
            new_password = data.get("password")

            if not username:
                return JsonResponse({"error": "Username is required to update user information"}, status=400)

            user = get_object_or_404(User, username=username)

            if new_email:
                user.email = new_email
            if new_password:
                user.set_password(new_password)

            user.save()
            return JsonResponse({"message": "User information updated successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Missing data"}, status=400)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)