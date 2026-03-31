from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.Overview, name='overview'),
    path('add-car/', views.Add_car, name='add-car'),
]
