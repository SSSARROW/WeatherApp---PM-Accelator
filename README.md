# WeatherApp - PM Accelerator

WeatherApp is a Django-based web application that provides weather information for various locations. The project demonstrates RESTful API design, form handling, and integration with external weather data sources.

## Features

- Search for weather by city
- REST API endpoints for weather data
- User-friendly web interface
- Django admin for managing data

## Project Structure

```
weatherapp/
    manage.py
    db.sqlite3
    requirements.txt
    api/
        models.py
        views.py
        urls.py
        serializers.py
        forms.py
        utils.py
        templates/
        migrations/
    weatherapp/
        settings.py
        urls.py
        wsgi.py
        asgi.py
```

## Setup Instructions

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd weatherapp
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Apply migrations**
   ```sh
   python manage.py migrate
   ```
4.**Create and Add API KEYS to a .env file
  ```sh
   OPENWEATHER_API_KEY="OPENWEATHER_API_KEY"
   YOUTUBE_API_KEY="YOUTUBE_API_KEY"
   DEBUG=true
    ```
5. **Run the development server**
   ```sh
   python manage.py runserver
   ```

## Usage

- Visit `http://127.0.0.1:8000/` in your browser to access the web interface.
- Use the search form to get weather information for a city.
- API endpoints are available under `/api/` (see below).

## API Endpoints

- **GET /api/weather/**  
  Returns weather data for all cities.

- **GET /api/weather/<city_name>/**  
  Returns weather data for the specified city.

## URLs

- Main app: [`weatherapp/urls.py`](weatherapp/weatherapp/urls.py)
- API: [`api/urls.py`](weatherapp/api/urls.py)

## What I Did

- Designed Django models for weather data ([`api/models.py`](weatherapp/api/models.py))
- Built RESTful API with Django REST Framework ([`api/views.py`](weatherapp/api/views.py), [`api/serializers.py`](weatherapp/api/serializers.py))
- Created forms for user input ([`api/forms.py`](weatherapp/api/forms.py))
- Implemented utility functions for fetching weather data ([`api/utils.py`](weatherapp/api/utils.py))
- Set up templates for the web interface
- Configured project settings and URLs ([`weatherapp/settings.py`](weatherapp/weatherapp/settings.py), [`weatherapp/urls.py`](weatherapp/weatherapp/urls.py))

