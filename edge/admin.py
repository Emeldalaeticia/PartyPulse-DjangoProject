from django.contrib import admin
from .models import User, Category, Location, Event, UserProfile, Booking

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Event)
admin.site.register(UserProfile)
admin.site.register(Booking)