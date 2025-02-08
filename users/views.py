from urllib import request
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model, login  
from django.shortcuts import redirect, render
from django.db import IntegrityError
from django.utils.timezone import now

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
            if user is not None:
                login(request, user)  # ✅ This logs in the user
                return redirect('HomePage')
        except IntegrityError:
            return render(request, 'SignUp.html', {'error': "Le nom d'utilisateur ou l'e-mail existe déjà."})
        except Exception as e:
            return render(request, 'SignUp.html', {'error': f"Une erreur s'est produite: {str(e)}"})

    return render(request, 'SignUp.html') 





def HomePage(request):
    print(f" failed: {request.user}")
    return render(request, 'HomePage.html', {'user': request.user})
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Choice, Demande, Meet, Question, Reponse, Etudiant

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
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Demande

@login_required
def askHelp(request):
    """ Display all demandes and handle form submission """
    
    if request.method == "POST":
        titre = "nothing"
        description = request.POST.get("description")

        if not titre or not description:
            return render(request, 'askHelp.html', {
                "demands": Demande.objects.all(),
                "user": request.user,
                "error": "Titre and description are required."
            })

        # Create and save new demande
        demande = Demande.objects.create(
            titre=titre,
            description=description,
            demandeur=request.user
        )

        return redirect('help')  # Redirect to refresh the page

    demands = Demande.objects.all()  # Fetch all demandes
    return render(request, 'askHelp.html', {"demands": demands, "user": request.user})


def help(request):
    demands = Demande.objects.all()  # Fetch all demands (questions)
    return render(request, 'help.html', {"demands": demands, "user": request.user})

def home(request):
    return render(request, 'Lpage.html')
def Classement(request):
    mentors = [
        {
            'name': 'Alice',
            'skills': 'Python, Machine Learning',
            'coins': 1500,
            'badges': 'Gold, Silver',
        },
        {
            'name': 'Bob',
            'skills': 'Web Development, JavaScript',
            'coins': 1200,
            'badges': 'Silver',
        },
        {
            'name': 'Charlie',
            'skills': 'Data Science, SQL',
            'coins': 900,
            'badges': 'Bronze',
        },
    ]
    return render(request, 'Classement.html' , {'mentors': mentors})


def Rewards(request):
    return render(request, 'Rewards.html')



def challenges(request):  # 🔹 Nom en minuscule
    questions = Question.objects.prefetch_related('choices').all()
    data = []

    for question in questions:
        data.append({
            "id": question.id,
            "question": question.question_text,
            "type": question.type,
            "choices": [{"text": choice.text, "is_correct": choice.is_correct} for choice in question.choices.all()]
        })

    return render(request, "Challenges.html", {"questions": data})  # 🔹 Assurez-vous que "questions" est bien utilisé dans le template


def add_question(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Charger les données JSON
            question_text = data.get("question")
            question_type = data.get("type")
            module = data.get("module")
            choices = data.get("choices", [])

            if not question_text or not choices:
                return JsonResponse({"message": "Données invalides !"}, status=400)

            # Sauvegarde en base de données (exemple simple)
            question = Question.objects.create(question_text=question_text, type=question_type ,module=module )
            for choice in choices:
                Choice.objects.create(question=question, text=choice["text"], is_correct=choice["is_correct"])

            return JsonResponse({"message": "Question ajoutée avec succès !"})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Méthode non autorisée"}, status=405)



@login_required
def add_coins(request):
    if request.method == "POST":
        user=request.user
        user.coins += 2  # Ajouter 2 coins
        user.save()
        return JsonResponse({"coins": user.coins})
    return JsonResponse({"error": "Invalid request"}, status=400)
@login_required
def create_meet(request):
    if request.method == "POST":
        description = request.POST.get("description")
        coins = int(request.POST.get("coins"))
        maxParticipants = int(request.POST.get("maxParticipants"))
        public = request.POST.get("public") == "on"
        date = request.POST.get("date")
        heure = request.POST.get("heure")
        categorie = request.POST.get("categorie")
        niveau = int(request.POST.get("niveau"))
        if niveau < 1 or niveau > 5:
            return HttpResponseBadRequest("Le niveau doit être entre 1 et 5.")
        
        # Create the Meet instance
        meet = Meet.objects.create(
            link="https://meet.google.com/new",  # Placeholder, user can modify later
            description=description,
            coins=coins,
            maxParticipants=maxParticipants,
            public=public,
            date=date,
            heure=heure,
            categorie=categorie,
            niveau=niveau,
            host=request.user,  # The logged-in user
        )

        return redirect("HomePage")  # Redirect after creation

    return render(request, "create_meet.html")




def LandingPage(request):
    return render(request, 'LandingPage.html')

def HomePage(request):
    print(f" failed: {request.user}")
    return render(request, 'HomePage.html', {'user': request.user})
@csrf_exempt

def CoursesPage(request):
    return render(request, 'CoursesPage.html')
@csrf_exempt

def filter_courses(request, category):
    if category == "Explore Courses":
        host = request.user
        courses = Meet.objects.filter(host=host) | Meet.objects.filter(public=True)
    
    elif category == "Active Courses":
        user = request.user
        courses = Meet.objects.filter(membersInAgenda=user)  # Show only meets where user is in the agenda
    
    elif category == "Completed Courses":
        current_time = now()
        user = request.user


        courses = Meet.objects.filter(
            membersInAgenda=user,  # Only show courses where user was in the agenda
        ).filter(
            # Courses that were on a past date
            date__lt=current_time.date()
        ) | Meet.objects.filter(
            membersInAgenda=user,
            date=current_time.date(),  # Course is today
            heure__lt=current_time.time()  # Course has already ended
        )
    return render(request, "_courses_partial.html", {"courses": courses, "category": category})


@login_required
@csrf_exempt

def join_course(request, course_id):
    user = request.user  
    course = get_object_or_404(Meet, id=course_id)
    meet_link = course.link  # Assuming this is the Google Meet URL
    print(f'meet link : {meet_link}')


    # ✅ Host auto-joins without coin checks
    if course.host == user:
        if not course.membersInAgenda.filter(id=user.id).exists():
            course.membersInAgenda.add(user)
            user.coins += course.coins
            print(f'host')
            user.save()
        return JsonResponse({'message': 'Joining course...', 'meetLink': meet_link})

    # ❌ Prevent joining if max participants reached
    if course.nbJoined >= course.maxParticipants:
        return JsonResponse({"error": "Max participants already reached!"}, status=400)

    # 🚨 Check if user already joined
    already_joined = course.membersInAgenda.filter(id=user.id).exists()

    # 🚨 First join: Verify coins
    if not already_joined and user.coins < course.coins:
        return JsonResponse({"error": "Not enough coins to join!"}, status=403)

    # ✅ Deduct coins only on first join
    if not already_joined:
        user.coins -= course.coins
        user.save()

    # ✅ Add user to meet
    course.membersInAgenda.add(user)
    course.nbJoined += 1
    course.save()
    return JsonResponse({'message': 'Joining course...', 'meetLink': meet_link})
    

@login_required
@csrf_exempt

def add_to_agenda(request, course_id):
    user = request.user
    course = get_object_or_404(Meet, id=course_id)

    # ✅ Host auto-adds to agenda
    if course.host == user:
        if not course.membersInAgenda.filter(id=user.id).exists():
            course.membersInAgenda.add(user)
        return JsonResponse({"message": "Host added to agenda successfully!"})

    # ❌ Prevent adding if max participants reached
    if course.nbJoined >= course.maxParticipants:
        return JsonResponse({"error": "Max participants already reached!"}, status=400)

    # 🚨 Ensure enough coins to add (but don’t deduct)
    if user.coins < course.coins:
        return JsonResponse({"error": "Not enough coins to add to agenda!"}, status=403)

    # ✅ Add user to agenda
    course.membersInAgenda.add(user)
    course.nbJoined += 1
    course.save()

    return JsonResponse({"message": "Meet added to agenda successfully!"})


@login_required
@csrf_exempt

def rate_course(request, course_id):
    """Handles user rating submissions for a course"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            rating = int(data.get("rating"))

            if rating < 1 or rating > 5:
                return JsonResponse({"error": "Invalid rating!"}, status=400)

            course = Meet.objects.get(id=course_id)

            # Add rating to course and update instructor's rating
            course.add_rating(rating)

            return JsonResponse({"message": "Rating added successfully!", "new_rating": course.rating})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request!"}, status=400)


