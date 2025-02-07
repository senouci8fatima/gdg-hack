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