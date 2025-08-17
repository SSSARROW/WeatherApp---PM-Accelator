from django.db import models

class WeatherRequest(models.Model):
    SOURCE_CHOICES = [
        ("city", "City/Town"),
        ("zip", "Zip/Postal"),
        ("coords", "Coordinates"),
        ("landmark", "Landmark/Fuzzy"),
    ]
    location_input = models.CharField(max_length=255)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="city")
    normalized_location = models.CharField(max_length=255, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    weather_current = models.JSONField(null=True, blank=True)
    weather_forecast = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.normalized_location or self.location_input} ({self.source})"