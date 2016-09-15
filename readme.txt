-------------------- Prérequis --------------------
- Python installé (3.5.0)
- Django installé (1.9)
- Bootstrap installé (3.3.0)

-------------------- Dézipper le projet --------------------
- Dézipper le projet dev_v2 à l'endroit souhaité.

-------------------- Configurer la base de données --------------------
- Editer le fichier settings.py (..\gelato-dev_v2\TB_Gelato\settings.py)
- Edite la configuration selon votre base de données (lignes 84-93) :
	Exemple avec une base de données postgresql :
	
	DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST':'localhost',
        'PORT': '5432',
        'NAME': 'TB_Gelato',
        'USER': 'postgres',
        'PASSWORD': 'TB_Gelato',
    }
}

- Les moteurs de base de données intégrés à Django sont :

'django.db.backends.postgresql'
'django.db.backends.mysql'
'django.db.backends.sqlite3'
'django.db.backends.oracle'

- pour utiliser Postgresql, installer psycopg2. Lancer la commande suivante dans un invité de commande :
pip install psycopg2

-------------------- Création de la base de données --------------------
- Dans un invité de commande (Windows) se déplacer à la racine du projet :
	cd ..\gelato-dev_v2
- exécuter les commandes suivantes:
python manage.py makemigrations
python manage.py migrate

-------------------- Créer un superutilisateur --------------------
- Dans un invité de commande (Windows) se déplacer à la racine du projet :
	cd ..\gelato-dev_v2
- exécuter la commande suivante et suivez les instructions :
	python manage.py createsuperuser
	
-------------------- Lancer l'application --------------------
- Dans un invité de commande (Windows) se déplacer à la racine du projet :
	cd ..\gelato-dev_v2
- exécuter la commande suivante :
	python manage.py runserver

-------------------- Administration --------------------
- Pour administrer le logiciel, se rendre à l'adresse suivante et entrer les crédentiales du superuser créé :
	http://localhost:8000/admin

-------------------- Tableaux de bord --------------------
Vous trouvez en annexes les différentes requêtes créées pour les tableaux de bord présents dans la feuille Excel.
Ne pas oublier de créer une source ODBC vers la base de données choisies.
	

Pour tester, vous pouvez utiliser Postgresql et le backup (TB_Gelato.backup) fournit avec des données tests.
Les informations des utilisateurs sont les suivants :
JD : JeanDupont
AT : AlainTerieur
MBR : MartinBrousse
KSM : KevinSmith
LBO : LeonieBou
MLE : MarieLeca

Administrateur :
Admin : TB_Gelato


-------------------- Mise en production --------------------
Pour la mise en production, ne pas oublier de changer la variable DEBUG dans settings.py :
DEBUG = False

Changer la clé secrête également avec l'outil à la page : http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY =
	



