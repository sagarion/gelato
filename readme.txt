-------------------- Prérequis --------------------
- Python installé (3.5.0)
- Django installé (1.9)
- Bootstrap installé (3.3.0)

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
	

Pour tester, vous pouvez utiliser Postgresql et le backup fournit avec des données tests.
Les informations des utilisateurs sont les suivants :
JD : JeanDupont
AT:AlainTerieur
MBR:MartinBrousse
KSM : KevinSmith
LBO : LeonieBou
MLE : MarieLeca

Admin :
Admin : TB_Gelato
	



