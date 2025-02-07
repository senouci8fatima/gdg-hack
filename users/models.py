from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, timedelta

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('admin', 'Administrateur'),
    ]
   
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')

    def __str__(self):
        return f"{self.username}"

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
class Etudiant(CustomUser):
    rate = models.FloatField(default=0.0)  # Note ou score de l'étudiant
    level = models.IntegerField(default=1)  # Niveau de l'étudiant
    coins = models.IntegerField(default=0)  # Monnaie virtuelle ou points de l'étudiant
    rewards = models.ManyToManyField(Reward, related_name="students", blank=True)  # Récompenses de l'étudiant

    def __str__(self):
        return f"Étudiant: {self.first_name} {self.last_name}"

class AdminSuper(CustomUser):
    def __str__(self):
        return f"Admin: {self.first_name} {self.last_name}"
    
class Meet(models.Model):
    link = models.URLField()  # Lien de la réunion (ex: Zoom, Google Meet)
    description = models.TextField()  # Description de la réunion
    coins = models.IntegerField(default=0)  # Coût en coins pour rejoindre la réunion
    maxParticipants = models.IntegerField(default=10)  # Nombre max de participants
    public = models.BooleanField(default=True)  # Indique si la réunion est publique ou privée
    date = models.DateField()  # Date de la réunion
    heure = models.TimeField()  # Heure de la réunion
    module = models.CharField(max_length=255)  # Nom du module associé à la réunion
    niveau = models.IntegerField(default=1)  # Niveau requis pour rejoindre la réunion
    host = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="meets") 
    comingSoon = models.BooleanField(default=False)  # Indique si la réunion est publique ou privée

    def save(self, *args, **kwargs):
        """ Met à jour automatiquement comingSoon si la réunion est demain """
        if self.date == (now().date() + timedelta(days=1)):  
            self.comingSoon = True  
        else:
            self.comingSoon = False  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Meet: {self.module} - {self.date} à {self.heure} ({'Public' if self.public else 'Privé'})"
  
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

from django.db import models

