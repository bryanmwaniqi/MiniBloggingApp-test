# MiniBloggingApp-test

**Version 1.0.0**

A dockerized mini blogging flask api application that allows you to create,access, update and delete blogposts.

## Documentation

Before you get started, there are several things you need to get hold of before spinning the application.

**Tech Stack**

- Flask micro-framework for building API.
- Postgresql for database.
- Pytest for tests implementation.
- Docker and Docker compose for containerization.

Make sure to checkout the API documentation YAML file in the root folder of this repo.

**Features**

- Containerized with docker
- Tests implementation
- Token based authentication

Here is a list of the endpoints and operations allowed:

```
/register
    - post
/login
    - post
/logout
    - get
/blog/<int:blog_id>
    - post
    - get
    - delete
/blogposts
    - post
    - get

```

**Authentication**

with regards to authentication, token based authentication is implemented with cookies being the JWT token location

To run just the flask app, navigate to the backend directory and open the terminal and do a issue a docker container run command in the terminal to install the dependencies, start the container and run the app. You can also use a virtual environment should you feel like so.

## Running the App

```
docker compose up

```

## Running Tests

To run tests using pytest, run the app in detached mode then open an interactive terminal in the flask api container and run pytest

```
docker compose -f docker-compose.test.yml up --build -d

docker exec -it $FlaskApiContainername/ID pytest

```
