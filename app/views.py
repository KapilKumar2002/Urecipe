import re
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from app.models import Urecipe

def index(request):
    recipes = Urecipe.objects.all()
    loginuser = True
    if request.method == "POST":
        username = request.POST['Username']
        password1 = request.POST['Password']
        user = auth.authenticate(username=username,password=password1)
        if user is not None:
            loginuser = False
            auth.login(request,user)
            messages.info(request, "Successful!")
        else:
            messages.info(request, "Invalid credentials!")
    if loginuser:
        params = {'recipes':recipes}
    else:
        params ={ 'recipes':recipes,'user':user}
    return render(request, 'app/index.html',params)

def recipe(request,id):
    name = Urecipe.objects.get(id=id)
    return render(request, 'app/recipe.html',{"recipe":name})

def search(request):
    if request.method == "POST":
        email = request.POST['Email']
        username = request.POST['Username']
        password1 = request.POST['Password']
        password2 = request.POST['ConfirmPassword']
        if email and username and password1 and password2:
            if password1 == password2 and len(password1)>=8 and len(username)>=8:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username already exists!")
                elif User.objects.filter(email=email).exists():
                    messages.info(request, "Email already exists!")
                else:
                    user = User.objects.create_user(username=username,email=email, password=password1)
                    user.save()
                    messages.info(request, "Successful!")
                    return redirect("/")
            else:
                messages.info(request, "Password not matching!")
        else:
            messages.info(request, "Fill the credentials!")

    elif request.method == "GET":
        search = request.GET.get('query')
        if search:
            recipe1 = Urecipe.objects.filter(recipe_ingredients__icontains=search)
            recipe2 = Urecipe.objects.filter(recipe_name__icontains=search)
            recipes = (recipe1 | recipe2).distinct()
            if len(recipes) == 0:
                messages.info(request, "Result not found!")
                return render(request, 'app/search.html',{"recipes":recipes})
            else:
                return render(request, 'app/search.html',{"recipes":recipes})
        else:
            return redirect("/")

    else:
        return render(request,"app:index")

    return render(request,"app/search.html")


def logout(request):
    auth.logout(request)
    return redirect("/")


def addurecipe(request):
    if request.method == "POST":
        image = request.POST['image']
        urecipe = request.POST['recipename']
        recipe_desc = request.POST['recipedescription']
        ingredients = request.POST['ingredients']
        mechanism = request.POST['mechanism']
        if urecipe and recipe_desc and ingredients and mechanism:
            recipe = Urecipe()
            recipe.recipe_image = image
            recipe.recipe_name = urecipe
            recipe.recipe_desc = recipe_desc
            recipe.recipe_ingredients = ingredients
            recipe.recipe_steps = mechanism
            recipe.owner = request.user
            recipe.save()
            messages.info(request, "Successful!")
            return redirect("/")
    else:
        return render(request, "app/add_urecipe.html")

def editurecipe(request,recipe_id):
    name = Urecipe.objects.get(id=recipe_id)
    if request.method == "POST":
        image = name.recipe_image
        recipename = request.POST['recipename']
        desc = request.POST['recipedescription']
        ingredients = request.POST['ingredients']
        steps = request.POST['mechanism']
        if recipename and desc and ingredients and steps:
            name.recipe_image = image
            name.recipe_name = recipename
            name.recipe_desc = desc
            name.recipe_ingredients = ingredients
            name.recipe_steps = steps
            name.owner = name.owner
            name.save()
            messages.info(request, "Successful!")
            return redirect("/")
    else:    
        return render(request, "app/edit.html",{"recipe":name})

def delete(request, id):
    name = Urecipe.objects.filter(id=id)
    name.delete()
    return redirect("/")
