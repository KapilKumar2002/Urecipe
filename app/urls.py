from django.urls import path
from app import views
app_name= "app"
urlpatterns = [
    path('',views.index,name="index"),
    path('<int:id>/', views.recipe, name='recipe'),
    path('signup',views.signup, name="signup"),
    path('logout/',views.logout, name="logout"),
    path('search/', views.search, name='search'),
    path('addurecipe/',views.addurecipe, name="addurecipe"),
    path('editurecipe/<int:recipe_id>',views.editurecipe, name="editurecipe"),
    path('delete/<int:id>',views.delete, name="delete")
]
