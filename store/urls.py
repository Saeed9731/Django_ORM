from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_data),
    path('order/', views.show_oderitem),
    path('invent/', views.show_product_with5inventory),
    path('comment/', views.show_comment),
]
