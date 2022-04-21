import os
import requests
import time
from io import BytesIO
from dotenv import load_dotenv
from mongoengine import connect
from model import Address, Persons

load_dotenv()
API_DE_DATOS = os.getenv("URL_API")

connect('fantasmas_ciberneticos', host='mongo')
r = requests.get(API_DE_DATOS)

data = r.json().get('data')

import requests
def download(fileName):
    f = open("fantasmas/static/img/" + fileName,'wb')
    f.write(requests.get('https://thispersondoesnotexist.com/image', headers={'User-Agent': 'My User Agent 1.0'}).content)
    f.close()


contador = 0
for dato in data:

    nombre_imagen = str(contador)+'.jpg'
    download(nombre_imagen)
    time.sleep(1)
    ruta = "img/" + nombre_imagen

    dire_1 = Address(street = dato["address"]["street"], streetName = dato["address"]["streetName"],
        buildingNumber = dato["address"]["buildingNumber"], city = dato["address"]["city"],
        zipcode = dato["address"]["zipcode"], country = dato["address"]["country"], county_code = dato["address"]["county_code"],
        location=(dato["address"]["latitude"], dato["address"]["longitude"]))

    person_1 = Persons(firstname = dato["firstname"], lastname = dato["lastname"], 
        email = dato["email"], phone = dato["phone"], birthday = dato["birthday"],
        gender = "male", website = dato["website"], image = ruta, address = dire_1)

    person_1.save()
    contador = contador + 1