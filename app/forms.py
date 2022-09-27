from .models import Urecipe  
from django import forms

class RecipeForm(forms.ModelForm):
  
    class Meta:
        model = Urecipe
        fields = ['recipe_image','recipe_name',"recipe_desc","recipe_ingredients","recipe_steps"]
        labels = {'text': ''}
