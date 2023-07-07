from django.contrib import admin
from .models import User, Category, Location, Event, Booking

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Event)
admin.site.register(Booking)