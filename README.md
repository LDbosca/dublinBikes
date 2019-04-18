Readme file for Team One's Dublin Bikes Software Engineering project.

Team members:

- Ivan Wahlrab
- Patrick Malatesta Tomasini
- Luke Deaton

The application can be accessed at: <a href="https://on-yerbike.com">on-yerbike.com</a>

The main goal of the application is to allow the users to plan their journey with Dublin Bikes.

The application web interface shows the current occupancy of the various Dublin Bikes stations. <br>
The user can then select the desired pick up and drop off times and stations and the application, using a machine learning model, predicts the bikes available and return stands available at the given times and locations, based on the weather conditions.
These features enable users of the bikerental scheme to plan their journeys ahead of time.



The application back-end consists of a Flask application that runs on a remote server. <br>
Weather data and Dublin Bikes stations information are constantly collected and stored in a SQL database. This data is used to periodically retrain the machine learning model.


Installation instructions:

- The application can be accessed at: <a href="https://on-yerbike.com">on-yerbike.com</a>

- To run the application locally

1) Create virtual environment using the requirements.txt (optional)

2) Pull git repository

3) Run flask application web/app.py

4) Access the web application from your browser using the local address given by flask

- To run the scrapers and collect data on weather and bikes stations

Set up crontab job for /src/combinedScraper.py to scrape data at 10 minute intervals

- To train and update the machine learning model

Set crontab job for /web/modelGenerator.py to regenerate ML models once per week
