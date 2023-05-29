import pandas as pd
import requests
url='https://api.edamam.com/api/food-database/v2/parser?app_id=4266f351&app_key=79aa66139c2a9634e000f5435120f3e6&ingr='+'Singori'

response = requests.get(url)
nutri=response.json()
print(nutri)