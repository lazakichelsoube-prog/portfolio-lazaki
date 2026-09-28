from django.core.exceptions import ValidationError
from django.db import models


class Profile(models.Model):
    """
    Informations personnelles affichees dans le Hero et la section 'A propos'.
    Un seul enregistrement est autorise (singleton).
    """
    nom_complet = models.CharField(max_length=100, default="Lazaki Chelsoube")
    titre = models.CharField(
        max_length=150,
        default="Étudiant en Licence 2 Génie Logiciel · Développeur Full-Stack",
    )
    bio = models.TextField(
        default=(
            "Développeur Full-Stack / Software Engineer. J'aime transformer "
            "des besoins en architectures propres, bien structurées et évolutives."
        )
    )
    processus_travail = models.TextField(
        blank=True,
        help_text="Comment vous travaillez : méthode, outils, étapes.",
        default=(
            "Je pars toujours du besoin réel avant le code : je clarifie les "
            "objectifs, je découpe le problème en modules simples, puis "
            "j'avance par itérations courtes et testées."
        ),
    )
    email = models.EmailField(default="tresorchelsoube@gmail.com")
    telephone = models.CharField(max_length=30, blank=True)
    github = models.URLField(blank=True, default="https://github.com/lazakichelsoube-prog/")
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True, default="https://www.instagram.com/top_tresor/")
    behance = models.URLField(blank=True)
    photo = models.ImageField(upload_to='profile/', blank=True, null=True)
    cv = models.FileField(upload_to='cv/', blank=True, null=True, help_text="CV en PDF (optionnel)")

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profil"

    def __str__(self):
        return self.nom_complet

    def save(self, *args, **kwargs):
        if not self.pk and Profile.objects.exists():
            raise ValidationError("Un seul profil est autorisé. Modifiez celui existant.")
        return super().save(*args, **kwargs)


class Skill(models.Model):
    CATEGORIE_CHOICES = [
        ('dev', 'Développement'),
        ('reseau', 'Réseau & Systèmes'),
        ('outil', 'Outils & Autres'),
    ]

    nom = models.CharField(max_length=60)
    categorie = models.CharField(max_length=10, choices=CATEGORIE_CHOICES, default='dev')
    niveau = models.PositiveSmallIntegerField(
        default=70,
        help_text="Niveau de maîtrise de 0 à 100.",
    )
    ordre = models.PositiveSmallIntegerField(default=0, help_text="Ordre d'affichage (plus petit = en premier).")

    class Meta:
        ordering = ['categorie', 'ordre', 'nom']
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"

    def __str__(self):
        return f"{self.nom} ({self.get_categorie_display()})"


class Project(models.Model):
    titre = models.CharField(max_length=120)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    technologies = models.CharField(
        max_length=200,
        help_text="Liste séparée par des virgules, ex : Django, JavaScript, PostgreSQL",
    )
    lien_demo = models.URLField(blank=True)
    lien_code = models.URLField(blank=True, help_text="Lien vers le dépôt GitHub")
    en_vedette = models.BooleanField(default=True, help_text="Afficher ce projet sur le site")
    date_realisation = models.DateField(blank=True, null=True)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordre', '-date_realisation']
        verbose_name = "Réalisation"
        verbose_name_plural = "Réalisations"

    def __str__(self):
        return self.titre

    @property
    def technologies_list(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]


class Client(models.Model):
    """Collaborations / clients / structures avec qui l'auteur a travaillé."""
    nom = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='clients/', blank=True, null=True)
    temoignage = models.TextField(blank=True)
    lien = models.URLField(blank=True)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = "Collaboration"
        verbose_name_plural = "Collaborations"

    def __str__(self):
        return self.nom


class Message(models.Model):
    """Messages envoyés depuis le formulaire de contact du site."""
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=150, blank=True)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_envoi']
        verbose_name = "Message reçu"
        verbose_name_plural = "Messages reçus"

    def __str__(self):
        return f"{self.nom} — {self.sujet or 'sans sujet'}"


class Etape(models.Model):
    """Une étape du parcours (formation, apprentissage...) affichée dans la timeline."""
    periode = models.CharField(
        max_length=60,
        help_text="Ex : '2025 — Aujourd'hui', '2024 — 2025', 'En continu'",
    )
    titre = models.CharField(max_length=150)
    description = models.TextField()
    ordre = models.PositiveSmallIntegerField(
        default=0,
        help_text="Ordre d'affichage (plus petit = affiché en premier).",
    )

    class Meta:
        ordering = ['ordre']
        verbose_name = "Étape du parcours"
        verbose_name_plural = "Parcours"

    def __str__(self):
        return f"{self.periode} — {self.titre}"