# SnipBox
SnipBox is a short note-saving app that allows users to save text snippets and organize them with tags. This project is built using Django for the backend, Django Rest Framework (DRF) for API development, and SQLite as the database.
Features:
The app uses SQLite as the database for easy setup and local development.

## Prerequisites

Before you begin, make sure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
  
## Getting Started

### Key Sections in the README:
1. **Clone the repository**: Instructions to get the code.
2. **Build Docker images**: Guide on building the Docker images for the project.
3. **Start containers**: How to bring the project up with Docker.
4. **Apply migrations**: Instructions to set up the database schema.
5. **Create a superuser**: How to create a superuser for admin access.
6. **Stopping the containers**: How to stop the containers once done.
7. **Troubleshooting**: Helpful tips for common issues like port conflicts and database errors.


### 1. Clone the repository

First, clone the repository to your local machine:

git clone <your-repository-url>
cd snipbox


### 2. Build the Docker images
    - docker-compose build
   
### 3. Start the containers
To start the containers and bring up the app, run:

    - docker-compose up
This will start the Django app on port 8000 (or another port if you change the port mapping). You should now be able to access the application at http://localhost:8000.


### 4. Apply migrations

To set up the database schema, apply the migrations:
   

    - docker-compose exec web python manage.py migrate

### 5. Create a superuser (optional)

If you want to access the Django admin interface, you need to create a superuser:

    -docker-compose exec web python manage.py createsuperuser

### 6. Access the application

Once the containers are up and running, you can access the app via:

    http://localhost:8000 (for the app)
    http://localhost:8000/admin (for the Django admin panel)

### 7. Stopping the containers

    docker-compose down
