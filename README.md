# Reading Time Accounting System
Web application in Django according to the technical specifications

## Description
The system tracks the time spent by the user on reading books. 
Users can start and end reading sessions, and the system stores 
the duration of each session and the total reading time for each book.

## Basic Requirements
- API for accounting for reading time
  - View a list of books with information
  - Book details with reading statistics
  - Management of book reading sessions
  - Total reading time per book
  - Daily statistics of reading time
  - API for user management

---
## Installation
**1. Clone the repository:**

   ```shell
   git clone https://github.com/AlexGrig23/rtas_backend.git
   ```

  Create virtual env.

   ```shell
   python -m venv venv
   ```
  
   Activate virtual env.
   
   on Windows: 
   ```shell
   cd venv/Scripts
   ```
   ```shell
   ./activate
   ```
  on Linux or Mac
   ```shell
   source venv/bin/activate
   ```

**2. In order to run the application, you need a Docker desktop**

Navigate to the project directory:
   ```shell
   cd rtas_backend (root)
   ```

   ```shell
   docker compose build --no-cache
   ```
   
**3. After that you have to execute the following command. 
   It creates the images if they are not located locally and starts the containers and configures 
   all the connections and networking between the containers**


   ```shell
   docker compose up
   ```
Be sure to make sure that all containers are running. 
If the containers do not rise for some reason, follow the instructions in the notes
with the help of the command: 
   ```shell
    docker ps
  ```
    
   - rtas_backend-web-1
   - rtas_backend-redis-1
   - rtas_backend-db-1
   - rtas_backend-worker-1
   - rtas_backend-celery-beat-1

Starting development server at  http://127.0.1:8000/
  
	
## Usage

**1. API Documentations**

You can familiarize yourself with the documents in detail at URL
The documentation was created for informational purposes only, so authorization using the header is not configured. 
To test authorization using the JWT token, you can use the terminal and CURL or Postman or any other convenient tool
 http://127.0.1:8000/swagger/

**For interactive testing of the application, 
I also recommend using the API, since testing in the admin panel can lead to unexpected results**


## Testing

**1. Tests can be run in a docker container so as not to set up an additional database:**

```shell
cd rtas_backend (root)
```

```shell
docker exec -it rtas_backend-web-1 /bin/bash
```
Run pytest coverage in docker container for all directories where the code is covered with tests

pytest --cov=auth_api --cov=library --cov=statistic

Or you can just run the test command in the container

pytest

## Notes
- sometimes, for various reasons such as RAM being overloaded, etc., containers may not start the first time, just try the docker "compose build --no-cache" and "docker compose up" again
- the .env file was added to the main project files, although this is considered bad practice, but since the project is of a test nature, it made it a little easier to launch
- the time interval for celery beats is used in seconds so that it is guaranteed to be executed once a day without additional time zone settings


## Technologies

- Python 3.11
- Django REST Framework 3.14.0
- Docker 
- Docker-compose
- PostgreSQL
- Redis
- Celery
- Swagger
- Pytest
- Coverage

## License
MIT License

Created by Alex Grig
email:alexgrig.cyber@gmail.com
