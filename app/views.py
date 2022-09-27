import re
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from app.forms import RecipeForm
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
                    messages.info(request, "Username already exists")
                elif User.objects.filter(email=email).exists():
                    messages.info(request, "Email already exists")
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

    form = RecipeForm()
    if request.method == 'POST':  
        form = RecipeForm(request.POST,request.FILES)  
        if form.is_valid(): 
            addrecipe = form.save(commit=False)  
            addrecipe.owner = request.user
            addrecipe.save()
            messages.info(request, "Successful!")
            return redirect("/") 

    
    return render(request, 'app/add_urecipe.html', {'form': form})  


def editurecipe(request,recipe_id):
    recipe = Urecipe.objects.get(id=recipe_id)
    if request.method == "POST":
        form = RecipeForm(instance=recipe, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Successful!")
            return redirect("/")
        
    else:    
        form = RecipeForm(instance=recipe)
        return render(request, "app/edit.html",{"form":form,'recipe':recipe})

def delete(request, id):
    name = Urecipe.objects.filter(id=id)
    name.delete()
    return redirect("/")
