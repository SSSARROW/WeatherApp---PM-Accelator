from django.http import JsonResponse

# API endpoint for current weather and forecast
def get_weather_api(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    if not lat or not lon:
        return JsonResponse({'error': 'Missing lat/lon'}, status=400)
    from .utils import fetch_current, fetch_forecast
    try:
        current = fetch_current(float(lat), float(lon))
    except Exception as e:
        current = None
    try:
        forecast = fetch_forecast(float(lat), float(lon))
    except Exception as e:
        forecast = None

    forecast_summary = []
    if forecast:
        for item in forecast.get('list', []):
            if "12:00:00" in item.get('dt_txt',''):
                desc = item.get('weather',[{}])[0].get('description','')
                temp = item.get('main',{}).get('temp','')
                date = item.get('dt_txt','').split()[0]
                forecast_summary.append({'date': date, 'desc': desc, 'temp': temp})
    response = JsonResponse({
        'current': current,
        'forecast_summary': forecast_summary
    })
    response["Access-Control-Allow-Origin"] = "*"
    return response
from django.shortcuts import render, redirect, get_object_or_404
from .models import WeatherRequest
from .forms import WeatherRequestForm
from .utils import youtube_search

# List all weather requests
def weather_list(request):
    records = WeatherRequest.objects.all().order_by('-created_at')
    from .utils import fetch_current, fetch_forecast
    
    for r in records:
        
        if r.lat and r.lon:
            try:
                r.weather_current = fetch_current(r.lat, r.lon)
            except Exception:
                r.weather_current = None
            try:
                r.weather_forecast = fetch_forecast(r.lat, r.lon)
            except Exception:
                r.weather_forecast = None
            r.save(update_fields=["weather_current", "weather_forecast"])
        
        r.current_summary = None
        if r.weather_current:
            r.current_summary = f"{r.weather_current.get('weather',[{}])[0].get('description','')} - {r.weather_current.get('main',{}).get('temp','')}°C"
        
        r.forecast_summary = []
        if r.weather_forecast:
            for item in r.weather_forecast.get('list', []):
                if "12:00:00" in item.get('dt_txt',''):
                    desc = item.get('weather',[{}])[0].get('description','')
                    temp = item.get('main',{}).get('temp','')
                    date = item.get('dt_txt','').split()[0]
                    r.forecast_summary.append({'date': date, 'desc': desc, 'temp': temp})
    return render(request, 'weather_list.html', {'records': records})


# Create new request (form)
def weather_create(request):
    if request.method == 'POST':
        form = WeatherRequestForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            from .utils import geocode_location, fetch_current, fetch_forecast
            
            geo = geocode_location(record.location_input)
            if geo:
                record.normalized_location = geo['label']
                record.lat = geo['lat']
                record.lon = geo['lon']
                try:
                    record.weather_current = fetch_current(record.lat, record.lon)
                except Exception:
                    record.weather_current = None
                try:
                    record.weather_forecast = fetch_forecast(record.lat, record.lon)
                except Exception:
                    record.weather_forecast = None
            else:
                record.weather_current = None
                record.weather_forecast = None
            record.save()
            return redirect('weather_list')
    else:
        form = WeatherRequestForm()
    return render(request, 'weather_form.html', {'form': form})

# Update existing record
def weather_update(request, pk):
    record = get_object_or_404(WeatherRequest, pk=pk)
    if request.method == 'POST':
        form = WeatherRequestForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            from .utils import geocode_location, fetch_current, fetch_forecast
            geo = geocode_location(record.location_input)
            if geo:
                record.normalized_location = geo['label']
                record.lat = geo['lat']
                record.lon = geo['lon']
                try:
                    record.weather_current = fetch_current(record.lat, record.lon)
                except Exception:
                    record.weather_current = None
                try:
                    record.weather_forecast = fetch_forecast(record.lat, record.lon)
                except Exception:
                    record.weather_forecast = None
            else:
                record.weather_current = None
                record.weather_forecast = None
            record.save()
            return redirect('weather_list')
    else:
        form = WeatherRequestForm(instance=record)
    return render(request, 'weather_form.html', {'form': form})

# Delete record
def weather_delete(request, pk):
    record = get_object_or_404(WeatherRequest, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('weather_list')
    return render(request, 'weather_confirm_delete.html', {'record': record})

# Show YouTube videos
def weather_youtube(request, pk):
    record = get_object_or_404(WeatherRequest, pk=pk)
    videos = youtube_search(record.normalized_location)
    return render(request, 'weather_youtube.html', {'record': record, 'videos': videos.get('items', [])})

