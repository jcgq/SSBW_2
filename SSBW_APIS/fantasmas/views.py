from cmath import log
from django.shortcuts import render
import logging
from model import *
from django.conf import *
from mongoengine import connect
from django.contrib import messages
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import *
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


logger = logging.getLogger(__name__)
try:
    connect('fantasmas_ciberneticos', host='mongo')
    logger.info("Conectado exitosamente a la base de datos")
except:
    logger.critical("No se ha podido conectar a la base de datos")

@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def inicio(request):
    logger.info("En el inicio")
    context = {
        "mensaje":"aniadir"
    }
    return render(request, "fantasmas/inicio.html", context)

def buscar(request):
    
    get_request = request.GET
    
    nom_persona = get_request.get("nombre")

    resultado_query = Persons.objects.filter(firstname__regex = nom_persona)
    if(len(resultado_query) == 0):
        logger.info("No se ha encontrado a ninguna persona")
    else:
        logger.info("Se ha obtenido resultado de la búsqueda")

    
    context = {
        "persona":resultado_query
    }
    return render(request, "fantasmas/consulta.html", context)



def editar(request, registro):
    logger.info("Editando")
    persona = Persons.objects.get(pk = registro)
    formulario = PersonForm()

    if request.method == "GET":
        print("EN el GET")
        context = {
            "formulario":formulario,
            "persona":persona
        }
        return render(request, "fantasmas/editar.html", context)

    persona = Persons.objects.get(pk=registro)
    
    if request.method == "POST":
        formulario = PersonForm(request.POST)
        if formulario.is_valid():
            persona = formulario.cleaned_data
            
            persona.update(set__firstname = persona["firstname"])
            persona.update(set__lastname = persona["lastname"])
            persona.update(set__email = persona["email"])
            persona.update(set__gender = persona["gender"])
        else:
            logger.error("Formulario inválido. Revise la información")

        persona = Persons.objects.get(pk = registro)
        print("La persona es ", persona)
        context = {
            "de":persona
        }
        return render(request, "fantasmas/detalle.html", context) 

    
            

def detalle(request, registro):
    persona = Persons.objects.get(pk=registro)
    context = {
        "de":persona
    }
    return render(request, "fantasmas/detalle.html", context)

def download(fileName):
    f = open("fantasmas/static/img/" + fileName,'wb')
    f.write(requests.get('https://thispersondoesnotexist.com/image', headers={'User-Agent': 'My User Agent 1.0'}).content)
    f.close()

def aniadir(request):
    formulario = PersonForm()

    if request.method == "POST":
        formulario = PersonForm(data = request.POST)
        print("POST", formulario)

        if formulario.is_valid():
            logger.info("Formulario valido")
            print(formulario.cleaned_data)
            ima = request.FILES

            firstname = formulario.cleaned_data.get('firstname')
            lastname = formulario.cleaned_data.get('lastname')
            email = formulario.cleaned_data.get('email')
            gender = formulario.cleaned_data.get('gender')
            p = Persons(firstname=firstname, lastname=lastname, email=email, gender=gender).save()

            if(ima):
                ff = str(p.id) + ".jpg"
                imaFile =  "fantasmas/static/img/" + ff

                fs = FileSystemStorage()
                fs.save(imaFile, ima["image"])
                p.image=str("img/" + ff)
                p.save()

            
            messages.success(request, "Resgistro añadido")

            return redirect('/consulta')
        else:
            logger.error("El formulario es erroneo")
            

    context = {
        "mensaje":"",
        "formulario":formulario
    }
    return render(request, "fantasmas/aniadir.html", context)


from django.http import JsonResponse

def eliminar(request, registro):
    persona = Persons.objects.get(id=registro)
    name = persona.firstname
    persona.delete()
    msg = "Visita " + name + " ha sido eliminada correctamente"
    messages.success(request, msg)

    data = {
        'borrado':registro
    }
    return JsonResponse(data)

@login_required
def consulta(request):
    context = {
    }
    return render(request, "fantasmas/consulta.html", context)
