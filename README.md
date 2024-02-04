# The Gab/Duel Folks
-Zach Neill.

## Description
The Gab/Duel Folks allows people with opinions to gab with and duel 
each other online. 

## Installation 
Only Docker is needed. This is great news for anyone with a Linux kernel
(or we lucky few who got Docker Desktop for Windows to work). 


### Production Environment 
To run this app in production-mode:
- Set the docker-compose.yaml _**services-->web-->build-->dockerfile**_ 
to ```Dockerfile```
- Comment out _**services-->web-->**_```volumes: ['./flask:/app'] ```
- ```docker compose up```
  - If it fails, just run it again. Sometimes the database isn't ready in time, 
even in spite of ```depends_on```. 
- Navigate to _**localhost:8080**_
  - Not to be confused with _**localhost:5000**_!!!

To take down any of the layers, run ```docker compose down```. To 
remove a specific layer like the database, run ```docker compose down db```

Sometimes on startup on Windows, Docker throws a docker-credential-desktop
error. Fix it with `source docker-credential-fix.sh`


### Development Environment 
To run this app in a development setting:
- ```docker compose up -d db```
  - This command starts the postgres database on port 5432

#### If you want the nginx layer... 
- ```docker compose up -d nginx```
- Set the docker-compose.yaml _**web-->build-->dockerfile**_ to ```Dockerfile.dev```
- Make sure ***services-->web-->***```volumes: ['./flask:/app']``` is uncommented 
- ```docker compose up web```
  - For extra measure, you can run ```docker compose up web --build```
- Navigate to _**localhost:8080**_
#### If you don't need nginx... 
- ```source setup.sh```
- ```flask run```
  - ```ctrl+c``` to stop the server, ```flask run``` to rerun it
- Navigate to _**localhost:5000**_
  - Not to be confused with _**localhost:8080**_!!!


## Testing 
Pytest is the testing framework. The unit and functional tests are in the 
tests directory in _**flask-->tests**_. 

The app uses Coverage.py. For a coverage report, ```cd``` into the 
flask directory and run ```source run_coverage.sh```. Or, run 
```coverage run -m pytest``` followed by 
```coverage report --omit="*/test*,*/__init__.py,database.py,*/conftest.py"```

For a linting test, run ```python -m pylint flask/app``` or 
```python -m pylint app``` if you are in the flask directory. 

A Travis CI pipeline is currently being set up. 

## Technologies 
- _**Flask**_
  - Front end and api
- _**Gunicorn/Flask**_
  - Server
- _**nginx**_
  - Load balancing/server
- _**PostgreSQL**_
  - Database
- _**Flask-SQLAlchemy**_
  - ORM
- _**Docker**_
  - Containerization
- _**Pytest/Pylint**_
  - Testing
- _**Travis CI**_
  - CI/CD pipeline

## Dev Checklist
- Fix tests
- Travis CI
- Edit profile
- Request friends
