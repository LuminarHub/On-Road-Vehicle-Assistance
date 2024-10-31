from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Bill)
admin.site.register(CarReserve)
admin.site.register(MechanicProfile)
admin.site.register(CarRenterProfile)
admin.site.register(RentCar)