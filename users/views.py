from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model, login  
from django.shortcuts import redirect, render
from django.db import IntegrityError

# Create your views here.

import json
import logging

logger = logging.getLogger(__name__)
Customuser = get_user_model()  # Récupération du modèle d'utilisateur personnalisé


@csrf_exempt
def sign_in(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                return render(request, 'SignIn.html', {'error': "Nom d'utilisateur et mot de passe requis."})

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # ✅ This logs in the user
                return redirect('HomePage')  

            return render(request, 'SignIn.html', {'error': "Identifiants incorrects."})

        except Exception as e:
            return render(request, 'SignIn.html', {'error': "Une erreur s'est produite."})

    return render(request, 'SignIn.html')

def sign_up(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not password or not email:
            return render(request, 'SignUp.html', {'error': "Tous les champs sont requis."})
        if password != password2:
            return render(request, 'SignUp.html', {'error': "Les mots de passe ne correspondent pas."})

        try:
            user = get_user_model().objects.create_user(username=username, email=email, password=password)
            user = authenticate(request, username=username, password=password)
            return redirect('HomePage')  # Rediriger vers la page de connexion après inscription réussie
        except IntegrityError:
            return render(request, 'SignUp.html', {'error': "Le nom d'utilisateur ou l'e-mail existe déjà."})
        except Exception as e:
            return render(request, 'SignUp.html', {'error': f"Une erreur s'est produite: {str(e)}"})

    return render(request, 'SignUp.html') 




@csrf_exempt

def LandingPage(request):
    return render(request, 'LandingPage.html')

def HomePage(request):
    print(f" failed: {request.user}")
    return render(request, 'HomePage.html', {'user': request.user})
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Demande, Reponse, Etudiant

@login_required
def create_response(request, demande_id):
    """ Allows an authenticated student to respond to a Demande """
    demande = get_object_or_404(Demande, id=demande_id)

    if request.method == "POST":
        content = request.POST.get("content")
        etudiant = get_object_or_404(Etudiant, id=request.user.id)  # Ensure only students can respond

        response = Reponse.objects.create(
            demande=demande,
            repondeur=etudiant,
            content=content
        )

        return redirect("demande_detail", demande_id=demande.id)

    return render(request, "responses/add_response.html", {"demande": demande})


def list_responses(request, demande_id):
    """ Retrieves all responses for a specific Demande """
    demande = get_object_or_404(Demande, id=demande_id)
    responses = demande.reponses.all()

    return render(request, "responses/list_responses.html", {"demande": demande, "responses": responses})

import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Demande

@login_required
def add_demande(request):
    if request.method == "POST":
        try:
            titre = request.POST.get("titre")  # ✅ Get form data
            description = request.POST.get("description")
            user = request.user  

            if not titre or not description:
                return JsonResponse({"error": "Titre and description are required"}, status=400)

            demande = Demande.objects.create(
               titre=titre,
               description=description,
               demandeur=user
               )

            demande.save()

            return JsonResponse({"message": "Demande added successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def list_demandes(request):
    """ Display all demandes """
    demandes = Demande.objects.all().values("id", "titre", "description", "demandeur__first_name", "demandeur__last_name")
    return JsonResponse({"demandes": list(demandes)}, safe=False)

def add_demande_page(request):
    """ Render the page to add a demande """
    return render(request, "add_demande.html")

def list_demandes_page(request):
    """ Render the page to list all demandes """
    return render(request, "list_demandes.html")

