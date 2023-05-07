import googlemaps
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
#1
gmaps = googlemaps.Client(key='')
address = '1300 SE Stark Street, Portland, OR 97214'
def calculate(address1):
    geocode_result = gmaps.geocode(address1)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    print(f'The coordinates of {address1} are: ({lng}, {lat})')
    coordinate=Point(lng, lat)
    global address
    address=address1
    return coordinate

#Es muy practica la herramienta de cordenadas de google mediante una direccion, muy buena la funcionalidad
#ya que se puede aplicar en varias aplicaciones donde el usuario ingresa solo la direccion.

#2

with open('neighborhoods.json', 'r') as f:
    neighborhoods = json.load(f)

polygon_neighborhoods = []
for neighborhood in neighborhoods['features']:
    if neighborhood['geometry']['type'] == 'Polygon':
        nameNeighborhood = neighborhood['properties']['NAME']
        points = Polygon(neighborhood['geometry']['coordinates'][0])
        poligono={'name': nameNeighborhood, 'points': points}
        polygon_neighborhoods.append(poligono)

coordinate = calculate(address)
counter=0
query_neighborhood=''
query_neighborhood=''
def query(coordinate):
    for polygon_neighborhood in polygon_neighborhoods:
        if polygon_neighborhood['points'].contains(coordinate):
            #3
            global counter
            counter+=1
            print(f"The coordinate is inside the {polygon_neighborhood['name']} neighborhood.")
            if counter==1:
                global main_neighborhood
                main_neighborhood=polygon_neighborhood['name']
            global query_neighborhood
            query_neighborhood=polygon_neighborhood['name']
            break
    #4 y 5
    else:
        print("The coordinate is not inside any neighborhood.")
    if main_neighborhood != query_neighborhood:
        print("The neighborhood is different.")
    else:
        parts = address.split(' ')
        last_part = parts[0]
        new_last_part = int(last_part) + 100
        parts[0] = str(new_last_part)
        new_address = ' '.join(parts)
        coordinate = calculate(new_address)
        return query(coordinate)
        
query_neighborhood=query(coordinate)
