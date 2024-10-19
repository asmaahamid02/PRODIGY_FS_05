# Socio

Socio is a simple social network application that allows users to seamlessly connect with each other. Users can create an account, post images, follow other users, comment on posts, like posts, and view their posts. The application is built using Django, MySQL and JQuery for dynamic content.

## Pre-requisites

1. Python 3.x
2. Django
3. MySQL

## Features

1. User registration
2. User login
3. User profile
4. User posts
5. Follow users
6. Like posts
7. Comment on posts
8. Image optimization and caching

## Technologies

1. Django
2. MySQL
3. HTML
4. Tailwind CSS
5. JQuery

## Demo

![Demo](./readme/demo1.gif)
![Demo](./readme/demo2.gif)
![Demo](./readme/demo3.gif)
![Demo](./readme/demo4.gif)

## Installation

1. Clone the repository

   ```bash
   git clone https://github.com/asmaahamid02/socio-django.git
   ```

2. Create virtual environment (optional)

   ```bash
   python -m venv venv
   #or
   pip install pipenv
   pipenv shell
   ```

3. Enter virtual environment (optional)

   ```bash
   source venv/bin/activate #for linux
   venv\Scripts\activate #for windows
   #or
   pipenv shell
   ```

4. Install dependencies

   ```bash
   pip install -r requirements.txt
   npm install
   ```

5. Create a database in MySQL

   ```sql
   CREATE DATABASE socio;
   ```

6. Copy the `.env.example` file to `.env` and update the database settings

   ```bash
   cp .env.example .env
   ```

7. Generate a new secret key and update the `SECRET_KEY` in the `.env` file with the generated secret key

   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

8. Run the migrations

   ```bash
   python manage.py migrate
   ```

9. Collect static files

   ```bash
   python manage.py collectstatic
   ```

10. Create a superuser (optional)

    ```bash
    python manage.py createsuperuser
    ```

11. Run the server

    ```bash
    python manage.py runserver
    ```

12. Run the watcher for tailwind css

    ```bash
    npm run dev
    ```
