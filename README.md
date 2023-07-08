# PartyPulse-DjangoProject
PartyPulse
PartyPulse is a web application built with Django that allows users to discover and book events. It provides a platform for event organizers to manage and promote their events while allowing users to browse and book tickets for their favorite events.

Features

User Registration and Login: Users can create an account and log in to access additional features.
Event Listing: Users can view a list of upcoming events with details such as title, description, date, time, and location.
Event Creation: Event organizers can create new events by providing relevant information like title, description, category, location, date, time, and ticket price.
Event Management: Organizers can update event details, manage ticket pricing, track sales, and manage venue information.
Event Booking: Users can book tickets for events by selecting the desired quantity and providing payment details.
User Profile: Users have a profile page where they can view and update their profile information and contact number.
API Endpoints: API endpoints are available to access event and booking data programmatically.

Installation
Clone the repository: git clone https://github.com/your-username/PartyPulse.git
Navigate to the project directory: cd PartyPulse
Install dependencies: pip install -r requirements.txt
Apply database migrations: python manage.py migrate
Start the development server: python manage.py runserver

Usage
Access the application in your web browser: http://localhost:8000
Register a new user account or log in with an existing account.
Browse the list of events and click on an event to view its details.
Book tickets for events by specifying the quantity and providing payment details.
Organizers can access additional features by navigating to the Organizer Dashboard.
Explore the API endpoints for programmatic access to event and booking data.

Acknowledgements
PartyPulse makes use of the following open-source libraries and frameworks:

Django: https://www.djangoproject.com/
Bootstrap: https://getbootstrap.com/
Django Rest Framework: https://www.django-rest-framework.org/
