from django.contrib import admin

from .models import Client, Etape, Message, Profile, Project, Skill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'titre', 'email')

    def has_add_permission(self, request):
        return not Profile.objects.exists()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'niveau', 'ordre')
    list_editable = ('niveau', 'ordre')
    list_filter = ('categorie',)
    search_fields = ('nom',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_realisation', 'en_vedette', 'ordre')
    list_editable = ('en_vedette', 'ordre')
    list_filter = ('en_vedette',)
    search_fields = ('titre', 'technologies')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ordre')
    list_editable = ('ordre',)
    search_fields = ('nom',)


@admin.register(Etape)
class EtapeAdmin(admin.ModelAdmin):
    list_display = ('periode', 'titre', 'ordre')
    list_editable = ('ordre',)
    search_fields = ('titre', 'description')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoi', 'lu')
    list_editable = ('lu',)
    list_filter = ('lu', 'date_envoi')
    readonly_fields = ('nom', 'email', 'sujet', 'contenu', 'date_envoi')
    search_fields = ('nom', 'email', 'contenu')