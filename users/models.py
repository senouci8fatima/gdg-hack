import json
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.decorators import login_required


class Reward(models.Model):
    REWARD_TYPES = [
        ('double_coins', 'Double Coins Earned'),
        ('meet_discount', 'Discount on Meet'),
        ('create_study_group', 'Create a Study Group'),
        ('create_challenge', 'Create a Challenge'),
        ('access_jobs', 'Access Job Offers & Internships'),
        ('free_courses', 'Access Free Courses'),
    ]

    name = models.CharField(max_length=255)  # Name of the reward
    description = models.TextField()  # Description of the reward effect
    reward_type = models.CharField(max_length=50, choices=REWARD_TYPES)  # Type of reward
    cost = models.IntegerField(default=0)  # Cost in coins to unlock this reward
    duration_days = models.IntegerField(null=True, blank=True)  # Duration in days (for temporary effects)
    locked = models.BooleanField(default=True)  

    def __str__(self):
        return f"Reward: {self.name} - {self.get_reward_type_display()}"
    

# Proxy models for different roles
class Etudiant(AbstractUser):
    rate = models.FloatField(default=0.0)  # Note ou score de l'étudiant
    level = models.IntegerField(default=1)  # Niveau de l'étudiant
    coins = models.IntegerField(default=5)  # Monnaie virtuelle ou points de l'étudiant
    rewards = models.ManyToManyField(Reward, related_name="students", blank=True)  # Récompenses de l'étudiant

    def update_rating(self):
        """Calculate instructor's new rating based on courses they hosted"""
        hosted_meets = Meet.objects.filter(host=self)
        all_ratings = [meet.rating for meet in hosted_meets if meet.rating > 0]

        if all_ratings:
            self.rate = sum(all_ratings) / len(all_ratings)
        else:
            self.rate = 0.0
        self.save()

    def __str__(self):
        return f"Étudiant: {self.first_name} {self.last_name}"

    
    
  
class Demande(models.Model):
    description = models.TextField()  # Description de la réunion
    titre = models.CharField(max_length=255)  # Nom du module associé à la réunion
    demandeur = models.ForeignKey(Etudiant, on_delete=models.CASCADE)  # or another field type, if appropriate

def __str__(self):
        return f"Titre: {self.titre} - Description: {self.description} )"
  

class Challenge(models.Model):
    description = models.TextField()  # Description du challenge
    titre = models.CharField(max_length=255)  # Titre du challenge
    module = models.CharField(max_length=255)  # Module associé
    niveau = models.IntegerField(default=1)  # Niveau requis
    coins = models.IntegerField(default=0)  # Récompense en coins

    def __str__(self):
        return f"Titre: {self.titre} - Description: {self.description}"


class QCM(Challenge):  # Question à Choix Multiples
    qst = models.TextField()  # Énoncé de la question
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255, blank=True, null=True)
    option4 = models.CharField(max_length=255, blank=True, null=True)
    correct_answers = models.JSONField()  # Liste des bonnes réponses (ex: ["option1", "option3"])

    def is_correct(self, answers):
        """Vérifie si les réponses fournies sont correctes"""
        return set(answers) == set(self.correct_answers)

    def __str__(self):
        return f"QCM: {self.qst}"


class QCU(Challenge):  # Question à Choix Unique
    qst = models.TextField()  # Énoncé de la question
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255, blank=True, null=True)
    option4 = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=255)  # Une seule bonne réponse

    def is_correct(self, answer):
        """Vérifie si la réponse fournie est correcte"""
        return answer == self.correct_answer

    def __str__(self):
        return f"QCU: {self.qst}"
    
class StudyGroup(models.Model):    
  link = models.URLField()  # Lien de la réunion (ex: Zoom, Google Meet)
  description = models.TextField()  # Description de la réunion
  niveau = models.IntegerField(default=1)  # Niveau requis pour rejoindre la réunion
  host = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="study_groups_host") 
  titre = models.CharField(max_length=255)  # Titre du challenge
  members = models.ManyToManyField(Etudiant, related_name="joined_study_groups", blank=True)  # Étudiants ayant rejoint le groupe

  def __str__(self):
        return f"Study Group: {self.titre} - Host: {self.host.first_name} {self.host.last_name} - Niveau: {self.niveau}"
    
class Reponse(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name="reponses")  # Question
    repondeur = models.ForeignKey(Etudiant, on_delete=models.CASCADE)  # User who answered
    content = models.TextField()  # Answer content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"Réponse by {self.repondeur.username} on {self.demande.titre}"
class Question(models.Model):
    TYPE_CHOICES = [
        ('QCM', 'Question à choix multiple'),
        ('QCU', 'Question à choix unique'),
        ('VF', 'Vrai ou Faux'),
    ]

    question_text = models.TextField() 
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
class Meet(models.Model):
    link = models.URLField()  # Lien de la réunion (ex: Zoom, Google Meet)
    description = models.TextField()  # Description de la réunion
    coins = models.IntegerField(default=0)  # Coût en coins pour rejoindre la réunion
    maxParticipants = models.IntegerField(default=10)  # Nombre max de participants
    nbJoined = models.IntegerField(default=0)  # Nombre max de participants
    public = models.BooleanField(default=True)  # Indique si la réunion est publique ou privée
    date = models.DateField()  # Date de la réunion
    heure = models.TimeField()  # Heure de la réunion
    categorie = models.CharField(max_length=255)  # Nom du module associé à la réunion
    titre = models.CharField(max_length=255)  # Nom du module associé à la réunion
    niveau = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])  # Restrict niveau to 1-5
    host = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="meets") 
    comingSoon = models.BooleanField(default=False)  # Indique si la réunion est publique ou privée
    membersInAgenda = models.ManyToManyField(Etudiant, related_name="added_to_their_agendas", blank=True)  # Étudiants ayant rejoint le groupe
    rating = models.FloatField(default=0.0)  # Average rating of the course
    ratings_count = models.IntegerField(default=0)  # Number of people who rated

    def save(self, *args, **kwargs):
        """Automatically update 'comingSoon' if the meeting is tomorrow"""
        if self.date == (now().date() + timedelta(days=1)):
            self.comingSoon = True
        else:
            self.comingSoon = False
        super().save(*args, **kwargs)

    def add_rating(self, new_rating):
        """Update the course rating and update the instructor's rating"""
        total_score = self.rating * self.ratings_count
        self.ratings_count += 1
        self.rating = (total_score + new_rating) / self.ratings_count
        self.save()

        # Update the instructor's rating
        self.host.update_rating()

    def __str__(self):
        return f"Meet: {self.categorie} - {self.date} at {self.heure} ({'Public' if self.public else 'Private'})"


from django.db import models