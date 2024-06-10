# MiniBloggingApp-test

[![Build Status](http://localhost:8080/buildStatus/icon?job=miniblog)](http://localhost:8080/job/miniblog/)

**Version 1.0.0**

A dockerized mini blogging flask api application that allows you to create,access, update and delete blogposts.

## Documentation

Before you get started, there are several things you need to get hold of before spinning up the application.

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
    - get
    - put
    - delete
/blogposts
    - post
    - get

```

**Authentication**

with regards to authentication, token based authentication is implemented with cookies being the JWT token location. So to access a protected endpoint, make sure to attach a cookie named access_token_cookie with the JWT as value in the cookie header.

**Running the App**

Fork the repository and clone it in your local machine. Navigate into the root folder and open a terminal there and run the following command.

```
docker compose up

```

**Running Tests**

To run tests using pytest, run the app in detached mode, then open an interactive terminal in the flask api container and run pytest

```
docker compose -f docker-compose.test.yml up --build -d

docker exec -it $FlaskApiContainername/ID pytest

```
