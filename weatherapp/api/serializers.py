from rest_framework import serializers
from .models import WeatherRequest
from datetime import date

class WeatherRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRequest
        fields = "__all__"

    def validate(self, attrs):
        start = attrs.get("start_date")
        end = attrs.get("end_date")
        if start and end and start > end:
            raise serializers.ValidationError({"date_range": "start_date cannot be after end_date"})
        # (optional) bound max range length
        if start and end:
            delta = (end - start).days
            if delta > 10:
                raise serializers.ValidationError({"date_range": "Max 10-day range for demo"})
        return attrs