from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from app.models import Painting, PaintingSize
from django.template import loader

def home(request):
    template = loader.get_template("home.html")
    paintings = Painting.objects.all()
    context = {"paintings": paintings}
    return HttpResponse(template.render(context, request))
