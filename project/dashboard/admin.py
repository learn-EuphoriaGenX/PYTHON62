from django.contrib import admin
from .models import Car, ChargingStation,ChargingPort, ChargingSession, Booking, Payment
# Register your models here.
admin.site.register(Car)
admin.site.register(ChargingStation)
admin.site.register(ChargingPort)   
admin.site.register(Booking)
admin.site.register(ChargingSession)
admin.site.register(Payment)


