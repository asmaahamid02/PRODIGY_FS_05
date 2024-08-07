# Socio

Socio is a simple social network application that allows users to create posts and follow other users.

## Pre-requisites

1. Python 3.x
2. Django
3. MySQL

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

9. Create a superuser

   ```bash
   python manage.py createsuperuser
   ```

10. Run the server

    ```bash
    python manage.py runserver
    ```
