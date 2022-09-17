
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Urecipe(models.Model):
    recipe_image = models.ImageField(upload_to = "pics")
    recipe_name = models.CharField(max_length=100)
    recipe_desc = models.CharField(max_length=250)
    recipe_ingredients = models.TextField()
    recipe_steps = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.recipe_name