from mongoengine import Document, EmbeddedDocument	
from mongoengine.fields import GeoPointField, URLField, EmailField, LongField, StringField, IntField, DateTimeField, EmbeddedDocumentField
from datetime import datetime
from django import forms
from rest_framework import serializers

CHOISES = [('male', 'hombre'), ('female', 'mujer')]

class Address(EmbeddedDocument):
    street              = StringField(max_length = 100, required = True)
    streetName          = StringField(max_length = 100, required = False)
    buildingNumber      = IntField(required = False)
    city                = StringField(max_length = 100, required = False)
    zipcode             = StringField(required = False)
    country             = StringField(max_length = 100, required = False)
    county_code        = StringField(max_length = 100, required = False)
    location            =  GeoPointField(required = False)

class Persons(Document):
    firstname           = StringField(max_length = 50, required = True)
    lastname            = StringField(max_length = 50, required = True)
    email               = EmailField(required = True)
    phone               = LongField(required = False)
    birthday            = DateTimeField(required = False)
    gender              = StringField(required = True, choices=["male", "female"])
    website             = URLField(required = False)
    image               = StringField(required = False)
    address             = EmbeddedDocumentField(Address, required = False)


class PersonForm(forms.Form):
    firstname = forms.CharField(label="Nombre",max_length=50)
    lastname  = forms.CharField(label="Apellido", max_length = 50)
    email  = forms.CharField(label="Correo", required = True)
    gender = forms.CharField(label="Genero", widget=forms.RadioSelect(choices=CHOISES))
    image = forms.FileField(label='Foto', required=False, widget=forms.FileInput())


class SnippetSerializer(serializers.Serializer):
    id = serializers.CharField()
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    email = serializers.EmailField()
    gender = serializers.ChoiceField(choices=CHOISES)
    image = serializers.FilePathField()