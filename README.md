# AIp2p: Pix2Pix Floorplan Tool

AIp2p est une interface graphique interactive pour dessiner des plans de bâtiments à l'aide de modèles Pix2Pix.

![Capture d’écran 2025-05-23 113515](https://github.com/user-attachments/assets/c7e5a24d-5ee7-4ecc-b08f-26c991d6964f)

##  Fonctionnalités principales

- **🖼️ Canvas de dessin interactif** : Dessinez des rectangles en glissant-déposant pour créer vos plans
- **🎨 Système de couleurs codées** : Plusieurs couleurs disponibles pour encoder différentes classes (murs, ouvertures, pièces, etc.)
- **↕️ Import/Export d'images** : Importez une image PNG existante ou exportez vos créations
- **🪄 Génération IA avancée** : Convertissez votre dessin en image réaliste via un modèle Pix2Pix (1 ou 2 passes)
- **🔧 Entraînement intégré** : Entraînez vos propres modèles avec vos datasets personnalisés

##  Prérequis

- **Python 3.10+**
- **CUDA 12** (recommandé pour l'accélération GPU)
  
##  Tableau des besoins mémoire

|  **Taille image** |  **Inférence – RAM** |  **Inférence – VRAM** |  **Entraînement – RAM** |  **Entraînement – VRAM** |
|----------------------|------------------------|---------------------------|-----------------------------|------------------------------|
| **256×256**          | 0.5 – 1 Go             | 0.5 – 1 Go                | 8 – 12 Go                   | 4 – 6 Go                     |
| **512×512**          | 1 – 2 Go               | 1 – 2 Go                  | 12 – 16 Go                  | 6 – 8 Go                     |
| **768×768**          | 2 – 3.5 Go             | 3 – 5 Go                  | 16 – 24 Go                  | 8 – 12 Go                    |
| **1024×1024**        | 4 – 6 Go               | 6 – 8 Go                  | 24 – 32 Go                  | 10 – 14 Go                   |


##  Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/votreutilisateur/AIp2p.git
cd AIp2p
```

### 2. Créer un environnement virtuel
```bash
# Créer l'environnement
python -m venv venv

# Activer l'environnement
# Sur Windows :
venv\Scripts\activate
# Sur Linux/macOS :
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

##  Utilisation

### Lancement de l'application
```bash
python AIp2p.py
```

### Guide d'utilisation rapide

#### **Dessin**
1. **Créer des rectangles** : Cliquez et glissez sur le canvas pour dessiner
2. **Supprimer des éléments** : Clic droit sur un rectangle pour le supprimer
3. **Changer de couleur** : Sélectionnez une couleur dans la palette pour encoder différents types d'éléments

#### **Génération IA**
1. **Charger les modèles** : Utilisez les boutons dédiés pour charger vos fichiers `.h5`
   - **1er modèle** : Conversion Masse → Couleur
   - **2ème modèle** : Conversion Couleur → Dessin détaillé
2. **Générer** : Lancez la génération pour obtenir votre plan réaliste

#### **Entraînement de modèles**
1. **Préparer les données** : Organisez vos images d'entraînement dans des dossiers séparés
2. **Configuration** : Spécifiez le dossier d'entrée, le dossier cible et le nombre d'epochs
3. **Lancer** : Le modèle sera automatiquement sauvegardé à la fin de l'entraînement

##  Dataset recommandé

### Pix2Pix Floorplans Dataset
**Source** : [nate-peters/pix2pix-floorplans-dataset](https://github.com/nate-peters/pix2pix-floorplans-dataset)

Ce dataset contient des images de plans d'étage pour petites maisons de plain-pied, dérivées de HousePlans.com. Chaque image a été étiquetée manuellement avec Rhino et Grasshopper :

- **Image A** : Forme de contour (région noire pleine)
- **Image B** : Contour avec régions codées par couleur selon les types de pièces

![Exemple du dataset](https://github.com/user-attachments/assets/3563eb47-cd95-471a-bd30-1d79dfcc322c)

## 🧠 Recommandations d'entraînement Pix2Pix

Ce tableau vous aide à calibrer votre entraînement selon la taille de votre dataset et vos ressources disponibles (RAM / VRAM).

| 📂 **Taille du dataset** | 🔁 **Epochs recommandées** | ⏱️ **Durée estimée (CPU)** | 🎯 **Objectif / Niveau**            |
|--------------------------|-----------------------------|-----------------------------|-------------------------------------|
| ~100 paires              | 200 – 400                   | Longue (4–8 h)              | Test rapide / prototype             |
| 500 paires               | 150 – 300                   | Moyenne (8–16 h)            | Projet perso solide                 |
| 1 000 paires             | 100 – 200                   | Moyenne (6–12 h avec GPU)   | Bon équilibre qualité               |
| 5 000+ paires            | 50 – 150                    | Longue (12–24 h)            | Projet pro / dataset varié          |
| 10 000+ paires           | 30 – 100                    | Très long (24 h+)           | Qualité publication / recherche     |

---

## 📝 Conseils d'entraînement

- **Surveillez la perte (`loss`)** mais jugez aussi **visuellement** la qualité des sorties.
- Plus le **dataset est petit**, plus vous aurez besoin de **nombreux epochs** pour une bonne généralisation.
- **Sauvegardez votre modèle régulièrement** (`checkpoint`) pour ne rien perdre.
- **Commencez toujours en 256×256 px** pour tester la stabilité avant de passer à plus grand.

## 🔧 Dépendances techniques

### Principales librairies
- **TensorFlow 2.15** - Framework d'apprentissage automatique
- **OpenCV** - Traitement d'images
- **Pillow** - Manipulation d'images
- **tkinter** - Interface graphique

### Configuration GPU (optionnelle mais recommandée)
Pour une performance optimale, assurez-vous d'avoir :
- **CUDA 12** installé
- **GPU compatible CUDA** avec au moins 4 Go de VRAM

Consultez `requirements.txt` pour la liste complète des dépendances.

## 🏗️ Architecture du projet

```
AIp2p/
├── AIp2p.py              # Script principal
├── requirements.txt      # Dépendances Python
├── models/              # Modèles entraînés 
├── datasets/            # Vos datasets d'entraînement
└── exports/             # Images générées et exportées
```

## 🤝 Contribuer

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

##  Crédits

**Développé par** : [OBJ.WTF](https://github.com/votreutilisateur) pour un projet de génération architecturale assistée par IA ( https://www.obj.wtf/ )

**Basé sur** :
- [Pix2Pix](https://github.com/tensorflow/examples/tree/master/tensorflow_examples/models/pix2pix) (TensorFlow Examples)
- Les travaux de [Stanislas Chaillou](https://github.com/StanislasChaillou)

## 📄 Licence

Ce projet est sous licence MIT. 


⭐ **N'hésitez pas à donner une étoile au projet si vous le trouvez utile !**
