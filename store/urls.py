from django.urls import path
from . import views

urlpatterns = [
    path('<str:name>', views.say_welcome),
    path('bye/', views.say_goodby),
    path('123/', views.say_number),
    path('something/<int:num>/', views.say_something),
]
