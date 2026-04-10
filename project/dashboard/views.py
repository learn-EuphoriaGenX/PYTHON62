from django.shortcuts import render, redirect
from .models import Car
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Car, Booking, ChargingPort, ChargingStation

# Create your views here.
@login_required(login_url='login')
def Overview(request):
    id = request.GET.get('id')
    car = None
    
    if request.user.is_superuser:
        if id:
            car = Car.objects.filter(id=id).first()
        else:
            car = Car.objects.first()
    else:
        if id:
            car = Car.objects.filter(id=id, user=request.user).first()
        else:
            car = Car.objects.filter(user=request.user).first()
    

    if not car:
        messages.info(request, "No cars found. Please add a car to view the overview.")
        return redirect('add-car')
    
    if request.user.is_superuser:
        prev_car = Car.objects.filter(id__lt=car.id).order_by('-id').first()
        next_car = Car.objects.filter(id__gt=car.id).order_by('id').first()
    else:
        prev_car = Car.objects.filter(user=request.user, id__lt=car.id).order_by('-id').first()
        next_car = Car.objects.filter(user=request.user, id__gt=car.id).order_by('id').first()

    total_bookings = Booking.objects.filter(user = request.user).count()
    total_cars = Car.objects.filter(user = request.user).count()

    return render(request, 'overview.html', {'car': car, 'o_is_active':True ,'prev_car': prev_car, 'next_car': next_car, 'total_bookings': total_bookings, 'total_cars': total_cars})

@login_required(login_url='login')
def Add_car(request):
    if request.method == 'POST':
        car_name = request.POST.get('car_name')
        car_image = request.FILES.get('car_image')
        max_speed = request.POST.get('max_speed')
        car_engine = request.POST.get('car_engine')
        charging_port = request.POST.get('charging_port')
        maintenance_cycle = request.POST.get('maintenance_cycle')
        seat_capacity = request.POST.get('seat_capacity')
        audio_system = request.POST.get('audio_system')

        if car_name and car_image and max_speed and car_engine and charging_port and maintenance_cycle and seat_capacity and audio_system:
            new_car = Car(
                user=request.user,
                name=car_name,
                image=car_image,
                max_speed=max_speed,
                engine=car_engine,
                charging_port=charging_port,
                maintenance_cycle=maintenance_cycle,
                seat_capacity=seat_capacity,
                audio_system=audio_system
            )
            new_car.save()
            messages.success(request, "Car added successfully!")
            return redirect('overview')
        else:
            print("Please fill in all fields.")
            messages.error(request, "Please fill in all fields.")
            return redirect('add-car')
       
    return render(request, 'add-car.html', {'o_is_active':True})

def SlotBooking(request):
    return render(request, 'slot-bookings.html', {'sb_is_active':True})

def ServiceHistory(request):
    return render(request, 'service-history.html', {'sh_is_active':True})

def Notifications(request):
    pass

def AddSlots(request):
    if request.method == 'POST':
        station_name = request.POST.get('station_name')
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        city = request.POST.get('city')
        port_number = request.POST.get('port')
        charger_type = request.POST.get('chargerType')
        charging_type = request.POST.get('chargingType')
        price = request.POST.get('price')

        if station_name and address and latitude and longitude and city and port_number and charger_type and charging_type and price:
            
            new_station = ChargingStation(
                name=station_name,
                address=address,
                city=city,
                lat=latitude,
                lng=longitude
            )
            new_station.save()
            new_port = ChargingPort(
                station=new_station,
                port_number=port_number,
                charger_type=charger_type,
                charging_type=charging_type,
                price_per_kwh=price
            )
            new_port.save()
            messages.success(request, "Slot added successfully!")
            return redirect('add-slots')
        else:
            messages.error(request, "Please fill in all fields.")
            return redirect('add-slots')

      
    return render(request, 'add-slot.html', {'as_is_active':True})

def AllSlots(request):
    return render(request, 'all-slots.html', {'vs_is_active':True})
