import json
import re
import regex
def limpiarJSON(text):
    #text = 'Entendido, José. Aquí te dejo una opción de desayuno de aproximadamente 658 calorías que puedes consumir para ayudarte a bajar de peso:```json{  "desayuno": [    {      "alimento": "Huevos revueltos con espinacas",      "porcion": "2 huevos",      "calorias": 200    },    {      "alimento": "Pan integral tostado con aguacate",      "porcion": "2 rebanadas de pan",      "calorias": 458    }  ]}```Este desayuno incluye huevos revueltos con espinacas, que son ricos en proteínas y fibra, y pan integral tostado con aguacate, que proporciona gras'

    pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
    result=pattern.findall(text)
    data = json.loads(result[0])
    '''if "desayuno" in data:
        return data['desayuno']
    if "comida" in data:
        return data['comida']
    if "cena" in data:
        return data['cena']'''
    return data

text='Entendido, José. Aquí te dejo una opción de desayuno de aproximadamente 658 calorías que puedes consumir para ayudarte a bajar de peso:json{  "desayuno": [    {      "alimento": "Huevos revueltos con espinacas",      "porcion": "2 huevos",      "calorias": 200    },    {      "alimento": "Pan integral tostado con aguacate",      "porcion": "2 rebanadas de pan",      "calorias": 458    }  ]}Este desayuno incluye huevos revueltos con espinacas, que son ricos en proteínas y fibra, y pan integral tostado con aguacate, que proporciona gras'
data=limpiarJSON(text)
print(data)