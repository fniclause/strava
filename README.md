# strava

########################################

The project is to gather my sport data from strava in order to monitor my training for triathlon.

I will add the health data (sleep, heart rate, etc) from garmin connect. But there is no free API for that. That will be done via scrapping.

The data (sport and health) is made by a garmin Fenix 6.


########################################
Version 1.

Scheduler => crontab

activities.py => retrieve the data of physical activities from strava API.
The python file retrieved API token via selenium package and then get all the data activities from the Strava API.
The data is written down locally in a CSV file

activities_d.py => get the all the activities and aggregate it by day
The python file read the csv file of activities and aggregate the data by day for the "running", "cycling" and "swimming"
The data is written down locally in a CSV file


# TO DO
=> get the data on a cloud database (GCP or AWS)
=> schedule with Airflow
=> get the health data from garmin
