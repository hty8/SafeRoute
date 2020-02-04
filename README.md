# SafeRoute (v0.2 - 12/18/19)

![alt text](https://raw.githubusercontent.com/hty8/SafeRoute/master/SafeRouteDemo.png)
This project was prepared as part of the Decision Support Systems course MIS 463 at Boğaziçi University and includes an application designed for companies carrying valuable loads in the city of Chicago. Users can find the safest routes to their destinations with this application.

Technologies such as Django, Google Maps API, Chicago City Data API, PostGIS, Postgresql were used when developing the application.

When the user chooses the start and end points, the application requests three maps from the Google Maps API and then calculates the safety scores of these roads by using Chicago Crime Data and presents them to the user.

# Installation
Docker must be installed on your machine for a quicker installation.
To install without using Docker, all libs and modules must be installed for Python 3 within requirements.txt.
For installation with Docker, the following should be done at the machine's terminal respectively:

Clone the project to your local machine
```
git clone git@github.com:hty8/SafeRoute.git
```
Go to project's directory
```
cd SafeRoute
```
Run the following command to start the service.
```
docker-compose up --build -d
```
After the service gets up, the following commands should be run in order to add crime data to the database.
```
docker exec -it saferoute_db_1 bash
```
```
shp2pgsql -I -s 4326 scores.shp scores | psql -d postgres -U postgres -h db -p 5432
```
```
exit
```
# Running the Service

To run the service, the following commands should be run in order (if a different port is to be used, the corresponding port should be opened to external traffic via Docker.)
```
docker exec -it saferoute_app_1 bash
```
```
python manage.py runserver 0.0.0.0:8000
```

You can access the application by going to http://0.0.0.0:8000 in your browser.
