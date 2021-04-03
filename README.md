# Zenatix-Order-Managemet


# Normal Setup
 - Clone the code from github.
 - Create the envrionment using the requirement.txt and python module 'venv'
 > - cmd - python3 -m venv env_name
 > -  Activate  Env - source env_name/bin/actvate
 - Move to project folder where manage.py present
 - Create the migrations.
 > - cmd - python3 manage.py makemigrations app_name or python3 manage.py makemigrations
 - Migrate the migrations.
 > - cmd - python3 manage.py migrate app_name or python3 manage.py migrate
 - Craete the SuperUser.
 >- python3 manage.py createsuperuser
 >- Enter username, email, password 
- Run the Server.
 >- python3 manage.py runserver


- PostMan Collection Link - https://www.getpostman.com/collections/18ca754d9f162bea1501


# Docker Setup
- Clone the code from github.
- Move to project folder where manage.py present.
- Delete Existing makemigrations if database shifted.
    <br>
    `find . -path "*/migrations/*.py" -not -name "__init__.py" -delete`
    <br>
    `find . -path "*/migrations/*.pyc"  -delete`

- Docker command :
    <br>
    -   sudo docker-compose -f docker-compose.yml up -d --build
    -   makemigrations :
        -- sudo docker-compose -f docker-compose.yml run migration python3 manage.py makemigrations app_name
    
    -   migrate :
        -- sudo docker-compose -f docker-compose.yml run migration python3 manage.py migrate app_name
