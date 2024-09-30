# The Gab/Duel Folks
-Zach Neill.

## Description
The Gab/Duel Folks allows people with opinions to gab with and duel 
each other online. 

## Installation 
Only Docker is needed. This is great news for anyone with a Linux kernel. 


### Production Environment 
To run this app in production-mode:
- ```docker compose up```
  - If it fails, just run it again. Sometimes the database isn't ready in time, 
even in spite of ```depends_on```. 

To take down the layers, run ```docker compose down```. To 
remove a specific layer like the database, run ```docker compose down db```

Add `--build` to rebuild a layer/see any changes you made. This flag works with any single layer, or all at once

Sometimes on startup on Windows, Docker throws a docker-credential-desktop
error. Fix it with `source docker-credential-fix.sh`


### Development Environment 
- ```docker compose up -d db```
  - This command starts the postgres database on port 5432. Naturally, the host is called db. The -d flag means detached mode
- ```docker compose up web```
  - Runs the Angular front end on port 4200
  - You can also `cd frontend`, run `npm i`, then `ng serve` for live reloading and quicker development at the consequence of running things locally
  - npm install takes ~5 minutes, but when this is in a working state, only dist/browser will be copied, so the 5 minute wait won't be in the image forever
- `docker compose up api` 
  - Runs the Flask backend on port 5000
  - This layer depends on the db being up, since Flask immediately requests a connection to db when spun up
  - Everything is prefixed with /api/ so localhost:5000 won't work but localhost:5000/api will
  - To see the old Flask front end, remove `url_prefix='/api'` in the blueprints and go to port 5000. This breaks proxy_pass on the nginx layer
- ```docker compose up -d nginx```
  - Runs the nginx layer on port 8081
  - This will proxy_pass traffic prefixed with /api/ to the api's port 5000 and non-prefixed traffic (front-end) to the web/frontend layer's port 80
  - nginx reads it as web:80. That's just localhost:4200, since web, the front end's container name in the docker compose file, is run on 4200

## Testing 
Pytest is the testing framework. The unit and functional tests are in the 
tests directory in _**flask-->tests**_. 

The backend uses Coverage.py. For a coverage report, ```cd``` into the 
api directory and run ```source run_coverage.sh```. Or, run 
```coverage run -m pytest``` followed by 
```coverage report --omit="*/test*,*/__init__.py,database.py,*/conftest.py"```

For a linting test, run ```python -m pylint api/app``` or 
```python -m pylint app``` if you are in the api directory. 

## Technologies 
- _**Flask**_
  - API
- _**Angular**_
  - Front end
- _**Gunicorn**_
  - Server
- _**nginx**_
  - Reverse proxy
- _**PostgreSQL**_
  - Database
- _**Flask-SQLAlchemy**_
  - ORM
- _**Docker**_
  - Containerization
- _**Pytest/Pylint**_
  - Testing

## Dev Checklist
- Fix tests
- Edit profile
- Request friends
