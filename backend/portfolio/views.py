from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Client, Etape, Message, Profile, Project, Skill
from .serializers import (
    ClientSerializer,
    EtapeSerializer,
    MessageSerializer,
    ProfileSerializer,
    ProjectSerializer,
    SkillSerializer,
)


class ProfileView(APIView):
    """Retourne le profil unique du portfolio (GET seul, pas de liste)."""

    def get(self, request):
        profile = Profile.objects.first()
        if profile is None:
            return Response({})
        return Response(ProfileSerializer(profile, context={'request': request}).data)


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(en_vedette=True)
    serializer_class = ProjectSerializer


class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class EtapeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Etape.objects.all()
    serializer_class = EtapeSerializer


class MessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Formulaire de contact : uniquement en écriture (POST)."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer