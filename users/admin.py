from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Etudiant

class EtudiantAdmin(UserAdmin):  # Change class name from CustomUserAdmin to EtudiantAdmin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rate', 'level', 'coins', 'rewards')}),  # Make sure these fields exist in the model
    )

admin.site.register(Etudiant, EtudiantAdmin)  # Register Etudiant instead of CustomUser