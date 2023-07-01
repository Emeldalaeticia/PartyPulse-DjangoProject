from django import forms
from edge.models import Event, Booking

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'date', 'location', 'category', 'description', 'price')

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('quantity', 'payment_details')

class TicketPriceForm(forms.Form):
    ticket_price = forms.DecimalField(label='Ticket Price', decimal_places=2, min_value=0)

class VenueForm(forms.Form):
    venue_name = forms.CharField(label='Venue Name', max_length=100)
    venue_address = forms.CharField(label='Venue Address', max_length=200)
    venue_city = forms.CharField(label='City', max_length=100)