# Working with Google Maps and Ant Colony Algorithm

The main goal of this project is to try and optimize the route of a set of given location across Aguascalientes (or any city covered by Google Maps). The intent of this document is to guide you through the process of achieveing this goal by using Python and the Google Maps API.

## Google Maps API
The Google Maps API is divided into different APIs, such as:
- Directions API
- Distance Matrix API
- Geocoding API
- Maps Static API
- Places API

All of these APIs were used in this project, but there are a lot more APIs that are offered in the Google Maps API.
## Places API
The Places API is a service that returns information about places using HTTP requests. Places are defined within this API as establishments, geographic locations, or prominent points of interest.
## Geocoding API
Geocoding is the process of converting addresses (like "1600 Amphitheatre Parkway, Mountain View, CA") into geographic coordinates (like latitude 37.423021 and longitude -122.083739), which you can use to place markers on a map, or position the map.
## Maps static API
The Maps Static API lets you embed a Google Maps image on your web page without requiring JavaScript or any dynamic page loading. The Maps Static API service creates your map based on URL parameters sent through a standard HTTP request and returns the map as an image you can display on your web page.
## Distance Matrix API
The Distance Matrix API is a service that provides travel distance and time for a matrix of origins and destinations. The API returns information based on the recommended route between start and end points, as calculated by the Google Maps API, and consists of rows containing duration and distance values for each pair.
## Directions API
The Directions API is a web service that uses an HTTP request to return JSON or XML-formatted directions between locations. You can receive directions for several modes of transportation, such as transit, driving, walking, or cycling.

Now, using these tools we can combine them with the Ant Colony Algorithm to generate optimal routes between locations and map them in Google Maps
## Setting our API key
In order to use the APIs described, we need to set our API key first:
```
gmaps = googlemaps.Client(key='YOUR_API_KEY')
```
## Getting our places
There are two main ways to get our places from google:
```
#Places API library on Python
geocode_result = gmaps.places('sushi en aguascalientes',location=[21.8828836,-102.2956243],radius=100)
#HTTP request using request module on Python
endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+loc+"&location=21.8828836,-102.2956243&radius=10&key=AIz res = requests.get(endpoint_url, params = params)
```
Both of these methods return a JSON with the results:
```
{
"html_attributions": [], "result":
{ "address_components":
[
{ "long_name": "48", "short_name": "48", "types": ["street_number"] }, {
"long_name": "Pirrama Road", "short_name": "Pirrama Rd", "types": ["route"],
}, {
"long_name": "Pyrmont", "short_name": "Pyrmont",
"types": ["locality", "political"],
}, {
"long_name": "Council of the City of Sydney", "short_name": "Sydney",
"types": ["administrative_area_level_2", "political"],
}, {
"long_name": "New South Wales",
"short_name": "NSW",
"types": ["administrative_area_level_1", "political"],
}, {
"long_name": "Australia", "short_name": "AU",
"types": ["country", "political"],
}, {
"long_name": "2009", "short_name": "2009", "types": ["postal_code"],
}, ],
"adr_address": '<span class="street-address">48 Pirrama Rd</span>, <span class="locality">Pyrmont</span> <span class="region">NSW</sp "business_status": "OPERATIONAL",
"formatted_address": "48 Pirrama Rd, Pyrmont NSW 2009, Australia",
"formatted_phone_number": "(02) 9374 4000",
"geometry": {
"location": { "lat": -33.866489, "lng": 151.1958561 }, "viewport":
{ "northeast":
{ "lat": -33.8655112697085, "lng": 151.1971156302915 }, "southwest":
{ "lat": -33.86820923029149, "lng": 151.1944176697085 }, },
},
"icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/generic_business-71.png", "icon_background_color": "#7B9EB0",
"icon_mask_base_uri": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/generic_pinlet", "international_phone_number": "+61 2 9374 4000",
"name": "Google Workplace 6",
"opening_hours":
{
"open_now": false, "periods":
Final Project: 3
[ {
"open": { "day": 1, "time": "0900" }, },
{
"close": { "day": 2, "time": "1700" }, "open": { "day": 2, "time": "0900" },
}, {
"close": { "day": 3, "time": "1700" },
"open": { "day": 3, "time": "0900" }, },
{
"close": { "day": 4, "time": "1700" }, "open": { "day": 4, "time": "0900" },
}, {
"close": { "day": 5, "time": "1700" },
"open": { "day": 5, "time": "0900" }, },
], "weekday_text":
[
"Monday: 9:00 AM – 5:00 PM", "Tuesday: 9:00 AM – 5:00 PM", "Wednesday: 9:00 AM – 5:00 PM", "Thursday: 9:00 AM – 5:00 PM", "Friday: 9:00 AM – 5:00 PM", "Saturday: Closed",
"Sunday: Closed",
], },
"status": "OK", }
"close": { "day": 1, "time": "1700" },
```
**Now that we have our place details from our resulting JSON, you can access to 'latitude' and 'longitude' parameters that will be useful later.**
## Getting our distances from Distance Matrix API
You can use your 'latitude' and 'longitud' parameters to calculate the travel distance and time from point A to B
```
result = gmaps.distance_matrix(origin, destination, mode = 'driving')
result_distance = result["rows"][0]["elements"][0]["distance"]["value"] 
result_time = result["rows"][0]["elements"][0]["duration"]["value"]
```
## Let's use Ant Colony!

Now, with all the data that we've gathered so far we can use the Ant Colony Algorithm to optimize the route between point A and point B
```
res = AC.ant_colony(n,2000,latitudes,longitudes,dis_mat,Ro=0.1,early_stopping_generations=1000)
```
in this case, the algorithm will return the optimal route, total travel time and distance. Finally we use take that route and map it into Google Maps using the Maps Static API
```
result_map = gmaps.static_map(
  center = [21.8828836,-102.2956243],#Aguascalientes downtown coordinates
  scale=2,
  zoom=12,
  size=[1280, 1280],
  format="jpg",
  maptype="roadmap",
  markers=markers,
  path="color:0x0000ff|weight:2|" + "|".join(waypoints))
```
And the final result will look like this:
