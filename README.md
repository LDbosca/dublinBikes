This is the readme file for Team One's Dublin Bikes Software Engineering project.

Team members:
Ivan Wahlrab
Patrick Malatesta Tomasini
Luke Deaton

This application consists of a Flask web application that enables users to plan journeys
on the Dublin Bike rental scheme by inputting journey times and stations into the web interface.
This information is passed to a predicitive model and the user is returned the expected bike
station occupancy for that time.

As well as the Flask application, this product consists of a web scraper that scrapes weather
and Dublin bikes information and stores it in a MySQL database. This is used to periodically
retrain our maching learning model.

Installation instructions:

1) Create virtual environment (optional)

2) Pull git repository

3) Conda install requirements from requirements.txt

4) Set chrontab job for /src/combinedScraper.py to scrape data at 10 minute intervals

5) Set chrontab job for /web/modelGenerator.py to regenerate ML models once per week

6) Run app.py to access locally or setup web server such as Nginx to host application

7) Get on-yerbike
