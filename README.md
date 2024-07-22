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
- PostgreSQL (recommended) or SQLite (for development)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
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

1. **Copy the example environment file and update it with your settings:**

    ```bash
    cp .env.example .env
    ```

    Edit the `.env` file with your preferred editor and update the database settings, secret key, and other configurations.

2. **Update Django settings:**

    Ensure the `settings.py` file is correctly configured to use `django-oidc-provider` and other required settings.

    ```python
    INSTALLED_APPS = [
        ...
        'django.contrib.sites',
        'oidc_provider',
        ...
    ]

    SITE_ID = 1

    OIDC_USERINFO = 'path.to.your.userinfo'
    ```

## Database Setup

1. **Run migrations to set up the database:**

    ```bash
    python manage.py migrate
    ```

2. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

## Running the Server

1. **Start the development server:**

    ```bash
    python manage.py runserver
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
    gunicorn yourproject.wsgi:application --bind 0.0.0.0:8000
    ```

3. **Set up your database server (e.g., PostgreSQL) and ensure it's properly configured in your `settings.py` file.**

4. **Configure environment variables for production.**

## Integration Guide

1. **Register a new client:**

    Go to the Django admin panel and register a new OIDC client with the required redirect URIs and scopes.

2. **Client Configuration:**

    In your client application, configure the OpenID Connect (OIDC) settings to use the SSO server. Example for a Python client:

    ```python
    from authlib.integrations.requests_client import OAuth2Session

    client = OAuth2Session(
        client_id='your-client-id',
        client_secret='your-client-secret',
        scope='openid profile email',
        redirect_uri='https://your-client-app/callback'
    )

    authorization_url, state = client.create_authorization_url('https://your-sso-server/authorize')
    print('Visit this URL to authorize:', authorization_url)
    ```

3. **Handle the callback and exchange the authorization code for tokens:**

    ```python
    token = client.fetch_token(
        'https://your-sso-server/token',
        authorization_response='https://your-client-app/callback?code=authorization_code'
    )
    ```

4. **Use the tokens to access protected resources:**

    ```python
    protected_url = 'https://your-sso-server/protected-resource'
    response = client.get(protected_url)
    print(response.json())
    ```

## Troubleshooting

- **Common Issues:**
  - Ensure all environment variables are set correctly.
  - Check the Django logs for any errors and resolve them accordingly.
  - Verify client registration details (client ID, secret, redirect URIs) are correct.

- **Useful Commands:**
  - `python manage.py check` - Check for any configuration issues.
  - `python manage.py showmigrations` - Display the status of migrations.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
