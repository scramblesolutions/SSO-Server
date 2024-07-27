# SSO Server using django-oidc-provider

This repository contains the implementation of a Single Sign-On (SSO) server using `django-oidc-provider`. This document provides a clear guide for setting up, deploying, and integrating the SSO server.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Server](#running-the-server)
- [Deployment](#deployment)
- [Integration Guide](#integration-guide)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Requirements

- Python 3.8+
- Django 3.2+
- django-oidc-provider 1.2.0+
- MySQL (recommended) or SQLite (for development)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/knowndir/SSO-Server.git
    cd SSO-Server
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

**Update Django settings:**

Ensure the `settings.py` file is correctly configured to use `django-oidc-provider` and other required settings.
    
visit `https://djecrety.ir/` to get secret key

   ```
   SECRET_KEY = 'b(fyxs*xwj56c=_p_b@yb+@tlukv4lc9vgqzl61#k%33i3wt7g'
   ```

## Database Setup

1. **Configure your database:**
   
   Settings for MySql
   ```
   DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'scramblesolutions',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',  # Set to 'localhost' or your DB server IP
            'PORT': '3306',  # Set to the port number (default is 3306)
        }
    }
   ```
   Settings for SQLite if you want to test
   ```
   DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR + '/db.sqlite3',
        }
    }
   ```
2. **Run migrations to set up the database:**

    ```bash
    python manage.py migrate
    ```

2. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```
3. **Create RSA Key:**
    ```bash
    python manage.py creatersakey
    ```
## Running the Server

1. **Start the development server:**
    
    ```bash
    python manage.py runserver
    ```
   Service will start on 3000 port or use custom port i.e. 7000
    ```bash
    python manage.py runserver 0.0.0.0:7000
    ```

    Access the server at `http://127.0.0.1:8000`.

## Deployment

1. **Collect static files:**

    ```bash
    python manage.py collectstatic
    ```

2. **Configure your web server (e.g., Nginx) and WSGI server (e.g., Gunicorn or uWSGI) for deployment.**

    Example configuration for Gunicorn:

    ```bash
    gunicorn sso_server.wsgi:application --bind 0.0.0.0:8000
    ```
3. **Configure environment variables for production.**

## Integration Guide

1. **Register a new client:**

    Go to the Django admin panel and register a new OIDC client with the required redirect URIs and scopes.


2. **Postman Requests**

      1. Get Token
         ```bash
         curl --location 'http://auth-server.com:8000/token/' \
         --header 'Cache-Control: no-cache' \
         --header 'Content-Type: application/x-www-form-urlencoded' \
         --data-urlencode 'client_id=129843' \
         --data-urlencode 'client_secret=98e55e9fa295958080584d03b025ae8f53ab376d3376d8a5b731b8d4' \
         --data-urlencode 'redirect_uri=http://auth-client.com:8081/callback/' \
         --data-urlencode 'grant_type=authorization_code'
         ```
            Go to Authorization Tab in Postman and provide 

            1. client_id

            2. client_secret

            3. redirect_uri

            4. scope (multiple space delimited)
         
               Scope option are as below:
   
               "openid" -> just for user id like. 

                ```bash
                {
                  "sub": "3"
                 }
                 ```
               "openid email" -> For user id and email like. 

                ```bash
                {
                "sub": "3",
                "email": "user@abc.com"
                }
                 ```
               "openid email profile" -> For user id, email and profile i.e. name, profile picture etc. 

                ```bash
                {
                "sub": "3",
                "email": "bhzahir@abc.com",
                "name": "Burhan Ul Haqq Zahir",
                "given_name": "Burhan Ul Haqq",
                "family_name": "Zahir",
                "nickname": "bhzahir",
                "profile": "Nice bio updated.",
                "picture": "BASE64 IMAGE",
                }
                 ```

               Above Scop will help you to get customer info in next step
       
      2. Get Client Info

         ```bash
            curl --location 'http://auth-server.com:8000/userinfo/' \
         --header 'Cache-Control: no-cache' \
         --header 'grant_type: client_credentials' \
         --header 'Authorization: Bearer Code_here'
         ```
         
         replace Code_here with Access Token you received in Get Token call
            
         You will get information as per scope defined in getting access token.
      
      3. Refresh Token
    
         ```bash
         curl --location 'http://auth-server.com:8000/token/' \
         --header 'Cache-Control: no-cache' \
         --header 'Content-Type: application/x-www-form-urlencoded' \
         --data-urlencode 'client_id=011326' \
         --data-urlencode 'client_secret=0cded52c6f98e9843ae1b4ffc363deccdb74653e5ab0d830b04712a7' \
         --data-urlencode 'grant_type=refresh_token' \
         --data-urlencode 'refresh_token=472c4ab2a75a4f6eb0a631788ef2245e'
         ```
         Change parameters accordingly 

            1. client_id

            2. client_secret

            3. refresh_token (you received in Get Token API Call)
         
3. **Integration Code Guide**
   
   Here are some links for OICD integration guide
   
   1. PHP
   2. Python
      
      

## Troubleshooting

- **Common Issues:**
  - Ensure environment is set correctly and installation is completed.
  - Check the Django logs for any errors and resolve them accordingly.
  - Verify client registration details (client ID, secret, redirect URIs) are correct.

- **Useful Commands:**
  - `python manage.py check` - Check for any configuration issues.
  - `python manage.py showmigrations` - Display the status of migrations.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
