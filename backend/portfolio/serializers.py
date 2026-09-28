from rest_framework import serializers

from .models import Client, Etape, Message, Profile, Project, Skill


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'nom_complet', 'titre', 'bio', 'processus_travail',
            'email', 'telephone', 'github', 'linkedin', 'instagram',
            'behance', 'photo', 'cv',
        ]


class SkillSerializer(serializers.ModelSerializer):
    categorie_affichage = serializers.CharField(source='get_categorie_display', read_only=True)

    class Meta:
        model = Skill
        fields = ['id', 'nom', 'categorie', 'categorie_affichage', 'niveau']


class ProjectSerializer(serializers.ModelSerializer):
    technologies_list = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = [
            'id', 'titre', 'description', 'image', 'technologies',
            'technologies_list', 'lien_demo', 'lien_code', 'date_realisation',
        ]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'nom', 'logo', 'temoignage', 'lien']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'nom', 'email', 'sujet', 'contenu', 'date_envoi']
        read_only_fields = ['id', 'date_envoi']


class EtapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etape
        fields = ['id', 'periode', 'titre', 'description']