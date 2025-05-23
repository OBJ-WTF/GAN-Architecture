AIp2p: Pix2Pix Floorplan Tool

AIp2p est une interface graphique interactive pour dessiner des plans de bâtiments et les convertir automatiquement en images réalistes à l'aide de modèles Pix2Pix entraînés avec TensorFlow.

Fonctionnalités principales

🧱 Canvas de dessin interactif : Dessinez des rectangles en glissant-déposant.

🎨 Choix de couleurs : Plusieurs couleurs disponibles pour encoder des classes (murs, ouvertures, etc.).

🖼️ Import/export d’images : Importez une image .png ou exportez vos dessins.

🤖 Génération IA : Convertissez votre dessin en image réaliste via un modèle Pix2Pix (1 ou 2 passes).

🔧 Entraînement intégré : Entraînez vos propres modèles avec vos datasets.

📋 Console de log intégrée : Affiche les sorties en temps réel dans l’interface.

🧹 Suppression intuitive : Clic droit pour supprimer un élément.

Captures d'écran

(À compléter avec des screenshots du canvas, de la génération, etc.)

Installation

Clonez ce dépôt :

git clone https://github.com/votreutilisateur/AIp2p.git
cd AIp2p

Créez et activez un environnement virtuel :

python -m venv venv
venv\Scripts\activate     # sous Windows
# source venv/bin/activate  # sous Linux/macOS

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

Cliquez sur "Générer" pour obtenir une image.

Deux modèles peuvent être enchaînés (2 passes).

Entraînement

Choisissez un dossier d’entrée et de cibles (format .png, aligné).

Spécifiez le nombre d’époques.

Lancez l’entraînement. Le modèle sera sauvegardé automatiquement.

Dépendances principales

Python 3.10+

TensorFlow 2.15

OpenCV

Pillow

tkinter

⚠️ CUDA 12 requis pour l'accélération GPU si disponible (voir requirements.txt pour détails).

Crédits

Développé par OBJ.WTF pour un projet de génération architecturale assistée par IA. S'appuie sur Pix2Pix (TensorFlow Examples).

Licence

Ce projet est sous licence MIT.

