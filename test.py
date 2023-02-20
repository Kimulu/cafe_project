import requests
import json
from math import radians, sin, cos, sqrt, atan2

# Google Places API endpoint
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# API key for Google Places API
api_key = "YOUR API KEY"

# User's location (latitude and longitude)
def get_user_location():
    url = 'https://ipinfo.io/json'
    response = requests.get(url)
    data = json.loads(response.text)
    location = data.get('loc')
    if location:
        lat, lon = location.split(',')
        return (float(lat), float(lon))
    return None


user_location =get_user_location()

# Search parameters
radius = 5000  # search radius in meters
type = "cafe"  # type of place to search for

# Make request to Google Places API
response = requests.get(url, params={
    "key": api_key,
    "location": f"{user_location[0]},{user_location[1]}",
    "radius": radius,
    "type": type
})

# Parse response JSON to get list of places
places = response.json()["results"]


# Calculate distance to each place using Haversine formula
for place in places:
    place_location = (
        place["geometry"]["location"]["lat"],
        place["geometry"]["location"]["lng"]
    )
    lat1, lon1 = user_location
    lat2, lon2 = place_location
    R = 6371  # radius of the earth in km
    dLat = radians(lat2-lat1)
    dLon = radians(lon2-lon1)
    a = sin(dLat/2) * sin(dLat/2) + cos(radians(lat1)) \
        * cos(radians(lat2)) * sin(dLon/2) * sin(dLon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c  # distance in km
    place["distance"] = round(distance,2)

# Sort places by distance
places = sorted(places, key=lambda x: x["distance"])

# Display list of places to user
#for place in places:
#    print(f"{place['name']}: {round(place['distance'],2)} km")
