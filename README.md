# Ticket Please - A web application for booking movie tickets
This application was developed with Django, MongoDB, HTML and CSS and is used for booking movie tickets.

Users can:
1. Sign up and login/logout
2. Update first name, last name, email, and password in profile settings
3. View the theatres’ program and the movies playing the current and next week
4. View details for each movie such as trailer, description, genre, director, cast, year, IMDB rating, duration, and suggestions for related movies 
5. Select a movie theatre and view the movies that are currently playing in that theater
6. Select a movie and view the movie theatres that are currently playing that movie
7. Book tickets for chosen date and select seats
8. Pay by card
9. View the history of all booked tickets

## Screenshots

Homepage
![homepage](img/homepage.png)

When users click on a movie, they can see information about it
![movie](img/movie_details.png)

When unauthenticated users click "Book movie ticket", they are redirected to this page where they are asked to sign up or login
![register or log in](img/register_login.png)

Sign up
![sign up](img/registration.png)

Login
![login](img/login.png)

Users can either select a movie and view the theaters where the movie is playing or select a theater and view the movies playing at it
![choose by movie or by theater](img/book_by_movie_or_theater.png)

Movie selection
![movie selection](img/movie_selection_1.png)

List of theaters where the selected movie is playing
![theater selection for movie](img/theater_selection_2.png)

Theater selection
![theater selection](img/theater_selection_1.png)

List of movies that are playing in the selected theater
![store register menu](img/movie_selection_2.png)

Date selection
![date selection](img/date_selection.png)

Seat selection page before user's seat reservation (Seat 4,1 is already reserved by another user)
![seat selection](img/seat_selection_1.png)

User selects seats 1,1 and 1,2
![date selection](img/seat_selection_2.png)

Seat selection page after user's seat reservation (Seats 1,1 and 1,2 are now red as they have been reserved by the user)
![date selection](img/seat_selection_3.png)

Payment
![payment](img/payment.png)

After the payment, the user is redirected to a booking confirmation page that displays the booked tickets
![booked tickets](img/booked_tickets.png)

Users can view their order history by clicking "My Orders" on the right
![order history](img/order_history.png)

The website visitors can view the movies schedule of all theaters by clicking "Movie Program"
![schedule](img/schedule.png)

Users can update their profile information
![profile update](img/profile_update.png)

Users can also update their password
![password update](img/password_update.png)
