from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from app.constants import NAME_MAX_LENGTH, PAINTING_DESCRIPTION_MAX_LENGTH, PAINTING_TITLE_MAX_LENGTH

class PaintingSize(models.Model):
    height = models.PositiveIntegerField(validators=[MaxValueValidator(500)]) # In cm
    width = models.PositiveIntegerField(validators=[MaxValueValidator(500)]) # In cm
    

class User(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)


class Artist(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)

class PaintingCategory(models.TextChoices):
    ABSTRACT = "Abstract"
    GENRE = "Genre"
    HISTORICAL = "Historical"
    LANDSCAPE = "Landscape"
    PROTRAIT = "Protrait"
    Religious = "Religious"

class Painting(models.Model):
    title = models.CharField(max_length=PAINTING_TITLE_MAX_LENGTH)
    description = models.CharField(max_length=PAINTING_DESCRIPTION_MAX_LENGTH, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category =  models.CharField(choices=PaintingCategory.choices)
    image = models.ImageField(upload_to="paintings")
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100_000_000)])
    size = PaintingSize()
    year = models.PositiveIntegerField(null=True)
