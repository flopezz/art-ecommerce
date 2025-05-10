from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from app.models import Painting, PaintingSize
from django.template import loader


@csrf_exempt
def painting(request):
    if request.method == "GET":
        painting_id = request.GET.get("id")
        if not painting_id:
            return JsonResponse({"error": "Painting ID is required"}, status=400)

        painting = get_object_or_404(Painting, id=painting_id)
        painting_data = {
            "id": painting.id,
            "title": painting.title,
            "description": painting.description,
            "category": painting.category,
            "image": painting.image.url if painting.image else None,
            "artist": painting.artist.username,
            "price": painting.price,
            "year": painting.year,
            "size": {
            "height": painting.size.height if painting.size else None,
            "width": painting.size.width if painting.size else None,
            } if painting.size else None,
        }
        return JsonResponse(painting_data, status=200)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            description = data.get("description")
            category = data.get("category")
            image = data.get("image")  # Assuming the image is provided as a URL or path
            artist_username = data.get("artist_username")
            price = data.get("price")
            size = data.get("size", {})
            year = data.get("year")

            if not all([title, category, artist_username, price]):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Validate artist
            artist = get_object_or_404(User, username=artist_username)

            # Validate user is in artist group

            # Create Painting instance
            painting = Painting.objects.create(
                title=title,
                description=description,
                category=category,
                image=image,
                artist=artist,
                price=price,
                year=year,
            )

            # If size is provided, set it
            height = size.get("height")
            width = size.get("width")
            if height and width:
                painting.size = PaintingSize.objects.create(height=height, width=width)
                painting.save()

            return JsonResponse({"message": "Painting created successfully", "id": painting.id}, status=201)

        except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON body"}, status=400)

    elif request.method == "DELETE":
        try:
            painting_id = request.GET.get("id")

            if not painting_id:
                return JsonResponse({"error": "Painting ID is required"}, status=400)

            painting = get_object_or_404(Painting, id=painting_id)
            painting.delete()

            return JsonResponse({"message": "Painting deleted successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)