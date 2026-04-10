from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.Overview, name='overview'),
    path('add-car/', views.Add_car, name='add-car'),
    path('slot-booking/', views.SlotBooking, name='slot-booking'),
    path('service-history/', views.ServiceHistory, name='service-history'),
    path('add-slots/', views.AddSlots, name='add-slots'),
    path('all-slots/', views.AllSlots, name='all-slots'),
]
