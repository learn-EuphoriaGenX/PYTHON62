from django.shortcuts import render, redirect
from .models import Car
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Car

# Create your views here.
@login_required(login_url='login')
def Overview(request):
    id = request.GET.get('id')
    car = None
    if id:
        car = Car.objects.filter(id=id, user=request.user).first()
    else:
        car = Car.objects.filter(user=request.user).first()
    

    if not car:
        messages.info(request, "No cars found. Please add a car to view the overview.")
        return redirect('add-car')
    return render(request, 'overview.html', {'car': car})

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
       
    return render(request, 'add-car.html')

def SlotBooking(request):
    pass

def ServiceHistory(request):
    pass

def Notifications(request):
    pass

def Settings(request):
    pass
