from django.shortcuts import render, get_object_or_404, redirect
from edge.models import Event, Booking
from .forms import EventForm, BookingForm, VenueForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import EventSerializer, BookingSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class EventListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetailAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class BookingDetailAPIView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def organizer_dashboard(request):
    
    # Get the events created by the logged-in user (organizer)
    events = Event.objects.filter(organizer=request.user)
    return render(request, 'organizer/organizer_dashboard.html', {'events': events})

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'events/event_create.html', {'form': form})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user:
        return redirect('events:event_detail', pk=event.pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_update.html', {'form': form})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user:
        return redirect('events:event_detail', pk=event.pk)

    if request.method == 'POST':
        event.delete()
        return redirect('events:event_list')
    return render(request, 'events/event_delete.html', {'event': event})

@login_required
def ticket_prices(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user:
        return redirect('events:event_detail', pk=event.pk)

    if request.method == 'POST':
        ticket_price = request.POST.get('ticket_price')
        event.ticket_price = ticket_price
        event.save()
        return redirect('events:event_detail', pk=event.pk)

    return render(request, 'events/ticket_prices.html', {'event': event})

@login_required
def venue_management(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user:
        # Organizer permission check
        return redirect('events:event_detail', pk=event.pk)
    
    if request.method == 'POST':
        # Process form submission and update venue information
        form = VenueForm(request.POST)
        if form.is_valid():
            event.venue_name = form.cleaned_data['venue_name']
            event.venue_address = form.cleaned_data['venue_address']
            # ... update other venue fields as needed
            event.save()
            return redirect('events:event_detail', pk=event.pk)
        else:
            # Render the venue management form
            form = VenueForm(instance=event)
        # Assuming you have fields in the Event model for venue_name, venue_address, etc.
        venue_name = request.POST.get('venue_name')
        venue_address = request.POST.get('venue_address')
        # ... extract other form data as needed
        event.venue_name = venue_name
        event.venue_address = venue_address
        # ... update other venue fields as needed
        event.save()
        return redirect('events:event_detail', pk=event.pk)
    else:
        # Render the venue management form
        return render(request, 'organizer/venue_management.html', {'event': event})

@login_required
def sales_report(request):
    events = Event.objects.all()
    total_sales = Booking.objects.aggregate(total_sales=Sum('total_price')).get('total_sales', 0)
    
    report_data = []
    for event in events:
        event_sales = Booking.objects.filter(event=event).aggregate(event_sales=Sum('total_price')).get('event_sales', 0)
        report_data.append({
            'event': event,
            'event_sales': event_sales,
            'event_percentage': (event_sales / total_sales) * 100 if total_sales else 0,
        })
    
    return render(request, 'organizer/sales_report.html', {'report_data': report_data})

@login_required
def book_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            user = User.objects.get(pk=request.user.pk)  # Retrieve the User instance from the database
            booking.user = user
            booking.event = event
            booking.save()

            send_mail(
                'Booking Confirmation',
                'Thank you for booking!',
                'sender@example.com',
                [booking.user.email],
                fail_silently=True,
            )

            return redirect('events:booking_confirmation', pk=booking.pk)
    else:
        form = BookingForm()

    return render(request, 'events/book_event.html', {'form': form, 'event': event})

@login_required
def booking_confirmation(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'events/booking_confirmation.html', {'booking': booking})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'events/booking_list.html', {'bookings': bookings})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('events:booking_list')
    return render(request, 'events/delete_booking.html', {'booking': booking})