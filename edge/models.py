
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth import get_user_model



class UserType(models.TextChoices):
    ORGANIZER = 'organizer', 'Organizer'
    USER = 'user', 'User'


class User(AbstractUser):
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.USER
    )

    def is_admin(self):
        return self.user_type == UserType.ADMIN

    def is_organizer(self):
        return self.user_type == UserType.ORGANIZER

    def is_user(self):
        return self.user_type == UserType.USER

    groups = models.ManyToManyField(
        Group,
        related_name='user_set_custom',  # Unique related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_set_custom',  # Unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    date = models.DateField()
    time = models.TimeField()
    image = CloudinaryField('image')

    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events',
        default='Unknown'
    )
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    venue_name = models.CharField(max_length=100, default='Venue name not yet listed')
    venue_address = models.CharField(max_length=100, default='Address not yet listed')

    def __str__(self):
        return self.title





class Booking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    payment_details = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
