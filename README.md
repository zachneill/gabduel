# The Gab/Duel Folks
Created by Zach Neill.

## Description
The Gab/Duel Folks allows people with opinions to gab with and duel 
each other online. 

## Installation 
Only Docker is needed. This is great news for anyone with a Linux kernel...  

### Development Environment 
To run this app in a development setting:
- ```docker compose up -d db```
  - This command starts the postgres database on port 5432

#### If you want the nginx layer... 
- ```docker compose up -d nginx```
- Set the docker-compose.yaml web-->build-->dockerfile to Dockerfile.dev
- Make sure web-->volumes: ['./flask:/app'] is uncommented 
- ```docker compose up web```
  - For extra measure, you can run ```docker compose up web --build```
- Navigate to _**localhost:8080**_

#### If you don't need nginx... 
- ```source setup.sh```
- ```flask run```
  - ```ctrl+c``` to stop the server, ```flask run``` to rerun it
- Navigate to _**localhost:5000**_

### Production Environment 
To run this app in production-mode:
- Set the docker-compose.yaml web-->build-->dockerfile to Dockerfile
- Comment out ```web-->volumes: ['./flask:/app'] ```
- ```docker compose up```
  - If it fails, just run it again. Sometimes the database isn't ready in time. 
- Navigate to _**localhost:8080**_

To take down any of the layers, run ```docker compose down```. To 
remove a specific layer like the database, run ```docker compose down db```

Sometimes on startup on Windows, Docker throws a docker-credential-desktop
error. Fix it with `source docker-credential-fix.sh`

## Tech stack 
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

## Checklist
- Fix tests
- Edit profile
- Request friends
