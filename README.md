
# Project_DjangoRest
# _API rest_framework
___
##
## Installation Python 3.12.2
___
_Téléchargement de Python_ :  
Rendez-vous sur la page de téléchargement officielle de Python : Télécharger Python1.
Choisissez la version de Python que vous souhaitez installer (par exemple, Python 3.12.2).
Sélectionnez votre système d’exploitation (Windows, Linux/UNIX, macOS, ou autre).
Cliquez sur le lien de téléchargement correspondant.
####
_Installation de Python_ :  
Une fois le téléchargement terminé, exécutez le fichier d’installation.
Suivez les instructions à l’écran pour installer Python sur votre système.
Assurez-vous d’ajouter Python à votre chemin d’accès système (cochez la case “Add Python to PATH” lors de l’installation sur Windows).
####
> **_Vérification de l’installation, Ouvrez votre terminal et Tapez :_** 
> 
>       python --version 

Et appuyez sur Entrée. Vous devriez voir la version de Python installée **_" Python 3.12.2. Ou plus "_**  
##
## Installation du projet sur votre machine 
___
####
### Récuperer le dossier du projet
_Clone du projet_ :
####
```bash
https://github.com/Gunther-C/Project_DjangoRest.git

```
###
_(download ZIP)_ :
####
```bash
https://github.com/Gunther-C/Project_DjangoRest/archive/refs/heads/master.zip
```
##
### Installer l'environement virtuel

_(Si vous avez fait le choix de télécharger le Dossier zip Décompresser ce dernier sur votre bureau)_

_Ouvrez votre terminal, Taper_

>        cd < Le chemin du dossier >  

>        python -m venv .venv  
_(n'oubliez pas le '.' au deuxième .venv)_

>_(pour la ligne de commande qui suit, selon votre système)_
> 1.     .venv\Scripts\activate.bat   
> 2.     source .venv/Scripts/Activate
> 3.     source .venv/bin/activate  
>_(Vous trouverez plus d'informations sur le site de [Stackoverflow](https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows/18713789#18713789))_  
####

_Résultat_  
>- (.venv) doit apparaitre dans le chemin du project de l'invité de commande  
>
> 
>- taper la commande " _pip freeze_ " , pip doit ètre vide
##
### Installation de poetry
####
> **_Vous trouverez les informations nécéssaire a la mise en place de Poetry sur votre projet ici :_** [Poetry](https://python-poetry.org/docs/)  

**_Suivez les instructions pour installer les modules nécessaires inclus dans requirements.txt:_**  


##
## Lancez _Django_
**_N'oubliez pas de lancer "poetry shell" dans votre terminal avant tout,_**  
___
####
> **_Créer un administrateur si besoin :_**  
> 
>       python manage.py createsuperuser 
> Renseignez les champs qui suivent.
> ###
**_Lancez le serveur :_**  

>       python manage.py runserver 
> Copiez, coller le lien qui s'affiche dans l'URL de votre navigateur,  
> ou  
> un click directement sur le lien.
###
## _Vous pouvez utiliser Postman ou autre pour tester vos requets_  
##
### 🔗 Links 
[![linkedin](https://www.linkedin.com/in/gunther-chevestrier-813344255?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/)
##