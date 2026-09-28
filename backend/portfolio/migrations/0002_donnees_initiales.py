from django.db import migrations


COMPETENCES = [
    ("Python", "dev", 85, 1),
    ("Django", "dev", 80, 2),
    ("JavaScript", "dev", 75, 3),
    ("PHP", "dev", 65, 4),
    ("Java", "dev", 65, 5),
    ("HTML / CSS", "dev", 85, 6),
    ("Réseaux Cisco (CCNA)", "reseau", 60, 1),
]


def creer_donnees_initiales(apps, schema_editor):
    Profile = apps.get_model('portfolio', 'Profile')
    Skill = apps.get_model('portfolio', 'Skill')

    if not Profile.objects.exists():
        Profile.objects.create(
            nom_complet="Lazaki Chelsoube",
            titre="Étudiant en Licence 2 Génie Logiciel · Développeur Full-Stack",
            bio=(
                "Développeur Full-Stack / Software Engineer. J'aime transformer "
                "des besoins en architectures propres, bien structurées et évolutives."
            ),
            processus_travail=(
                "Je pars toujours du besoin réel avant le code : je clarifie les "
                "objectifs, je découpe le problème en modules simples, puis "
                "j'avance par itérations courtes et testées."
            ),
            email="tresorchelsoube@gmail.com",
            github="https://github.com/lazakichelsoube-prog/",
            instagram="https://www.instagram.com/top_tresor/",
        )

    if not Skill.objects.exists():
        for nom, categorie, niveau, ordre in COMPETENCES:
            Skill.objects.create(nom=nom, categorie=categorie, niveau=niveau, ordre=ordre)


def annuler(apps, schema_editor):
    # Migration de donnees : on ne supprime rien automatiquement en arriere.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(creer_donnees_initiales, annuler),
    ]
