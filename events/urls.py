from django.urls import path, include
from . import views


app_name = 'events'

urlpatterns = [
    # Events Urls
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/update/', views.event_update, name='event_update'),
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),

    # Booking URLs
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('booking/<int:pk>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
    
    # Organizer URLs
    path('organizer/dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
    path('organizer/events/create/', views.event_create, name='organizer_event_create'),
    path('organizer/events/<int:pk>/update/', views.event_update, name='organizer_event_update'),
    path('organizer/events/<int:pk>/pricing/', views.ticket_prices, name='organizer_ticket_pricing'),
    path('organizer/events/<int:pk>/sales/', views.sales_report, name='organizer_sales_tracking'),
    path('organizer/events/<int:pk>/venue/', views.venue_management, name='organizer_venue_management'),

    # Payment Urls
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment/completed/', views.payment_completed, name='payment_completed'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
    path('process-payment/', views.process_payment, name='process_payment'),
    
   
]
