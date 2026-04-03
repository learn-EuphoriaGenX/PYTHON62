from django.db import models
from django.conf import settings

class Car(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cars")

    name = models.CharField(max_length=100)  # Tesla Model Y
    image = models.ImageField(upload_to='cars/')

    max_speed = models.IntegerField()  # 340 km/h
    engine = models.CharField(max_length=100)  # En12 87
    charging_port = models.CharField(max_length=100)  # A3 EV 883
    maintenance_cycle = models.CharField(max_length=50)  # Every 1 month
    seat_capacity = models.IntegerField()  # 10+
    audio_system = models.CharField(max_length=100)  # Sony 325i

    battery_percentage = models.IntegerField(default=0)  # 56%
    is_charging = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.user.username}'

class ChargingStation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)

    lat = models.FloatField()
    lng = models.FloatField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name    

class ChargingPort(models.Model):
    station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE, related_name='ports')

    port_number = models.IntegerField()
    charger_type = models.CharField(max_length=100)  # Type 2, CCS, CHAdeMO

    price_per_kwh = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.station.name} - Port {self.port_number}"

class Booking(models.Model):

    status_choices = [
        ('booked', 'Booked'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    port = models.ForeignKey(ChargingPort, on_delete=models.CASCADE)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    status = models.CharField(max_length=20, choices=status_choices, default='booked')

    def __str__(self):
        return f"{self.port} | {self.start_time} - {self.end_time}"
    
class ChargingSession(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    energy_used = models.FloatField(null=True, blank=True)
    total_cost = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=[
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed')
    ], default='ongoing')

    def __str__(self):
        return f"Session {self.id}"
    
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    amount = models.FloatField()

    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ])

    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature  = models.CharField(max_length=255, null=True, blank=True)

    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.amount} - {self.payment_status}"