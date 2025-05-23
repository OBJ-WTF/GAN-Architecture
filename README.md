# AIp2p: Pix2Pix Floorplan Tool

AIp2p est une interface graphique interactive pour dessiner des plans de bâtiments à l'aide de modèles Pix2Pix.


![Capture d’écran 2025-05-23 105628](https://github.com/user-attachments/assets/da91b110-13ee-4903-9467-8238222f6b09)




# Fonctionnalités principales

🧱 Canvas de dessin interactif : Dessinez des rectangles en glissant-déposant.

🎨 Choix de couleurs : Plusieurs couleurs disponibles pour encoder des classes (murs, ouvertures, etc.).

🖼️ Import/export d’images : Importez une image .png ou exportez vos dessins.

🤖 Génération IA : Convertissez votre dessin en image réaliste via un modèle Pix2Pix (1 ou 2 passes).

🔧 Entraînement intégré : Entraînez vos propres modèles avec vos datasets.




# Installation

Clonez ce dépôt :

git clone https://github.com/votreutilisateur/AIp2p.git
cd AIp2p

Créez et activez un environnement virtuel :

python -m venv venv
venv\Scripts\activate     # sous Windows
source venv/bin/activate  # sous Linux/macOS

Installez les dépendances :

pip install -r requirements.txt

Lancement

python AIp2p.py

Utilisation

Dessin

Cliquez-glissez pour dessiner un rectangle.

Clic droit sur un rectangle pour le supprimer.

Génération

Chargez un modèle .h5 via les boutons dédiés.

1er modèle : Masse vers Couleur
2eme modèle : Couleur vers Dessin 


# Entraînement

Choisissez un dossier d’entrée et de cibles (format .png, aligné).

⚠️ DATA SET : https://github.com/nate-peters/pix2pix-floorplans-dataset ⚠️ 

Ce jeu de données est dérivé d'images de plans d'étage pour de petites maisons de plain-pied provenant de HousePlans.com. Chaque image a été étiquetée manuellement à l'aide de Rhino et Grasshopper, puis exportée sous forme de paire d'images A/B pour une utilisation avec pix2pix. L'image A contient la forme de contour de chaque plan d'étage représentée comme une région noire pleine. L'image B contient le même contour, mais avec des régions codées par couleur qui correspondent aux différents types de pièces dans le plan

![2f764551a999](https://github.com/user-attachments/assets/3563eb47-cd95-471a-bd30-1d79dfcc322c)

Spécifiez le nombre d’epochs.

Lancez l’entraînement. Le modèle sera sauvegardé automatiquement.

# Dépendances principales

Python 3.10+

TensorFlow 2.15

OpenCV

Pillow

tkinter

⚠️ CUDA 12 requis pour l'accélération GPU si disponible (voir requirements.txt pour détails).

# Crédits

Développé par OBJ.WTF pour un projet de génération architecturale assistée par IA. 
S'appuie sur Pix2Pix (TensorFlow Examples) and basé sur les travaux de Stanislas Chaillou : https://github.com/StanislasChaillou

# Licence

Ce projet est sous licence MIT.

