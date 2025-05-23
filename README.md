# AIp2p: Pix2Pix Floorplan Tool

AIp2p est une interface graphique interactive pour dessiner des plans de bâtiments et les convertir en images réalistes à l'aide de modèles Pix2Pix basés sur l'intelligence artificielle.

![Capture d'écran de l'interface AIp2p](https://github.com/user-attachments/assets/da91b110-13ee-4903-9467-8238222f6b09)

## 🚀 Fonctionnalités principales

- **🧱 Canvas de dessin interactif** : Dessinez des rectangles en glissant-déposant pour créer vos plans
- **🎨 Système de couleurs codées** : Plusieurs couleurs disponibles pour encoder différentes classes (murs, ouvertures, pièces, etc.)
- **🖼️ Import/Export d'images** : Importez une image PNG existante ou exportez vos créations
- **🤖 Génération IA avancée** : Convertissez votre dessin en image réaliste via un modèle Pix2Pix (1 ou 2 passes)
- **🔧 Entraînement intégré** : Entraînez vos propres modèles avec vos datasets personnalisés

## 📋 Prérequis

- **Python 3.10+**
- **CUDA 12** (recommandé pour l'accélération GPU)
- **8 Go de RAM minimum** (16 Go recommandés pour l'entraînement)

## 🛠️ Installation

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

## 🎯 Utilisation

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

## 📊 Dataset recommandé

### Pix2Pix Floorplans Dataset
**Source** : [nate-peters/pix2pix-floorplans-dataset](https://github.com/nate-peters/pix2pix-floorplans-dataset)

Ce dataset contient des images de plans d'étage pour petites maisons de plain-pied, dérivées de HousePlans.com. Chaque image a été étiquetée manuellement avec Rhino et Grasshopper :

- **Image A** : Forme de contour (région noire pleine)
- **Image B** : Contour avec régions codées par couleur selon les types de pièces

![Exemple du dataset](https://github.com/user-attachments/assets/3563eb47-cd95-471a-bd30-1d79dfcc322c)

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
├── models/              # Modèles pré-entraînés (optionnel)
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

## 📝 Crédits

**Développé par** : [OBJ.WTF](https://github.com/votreutilisateur) pour un projet de génération architecturale assistée par IA

**Basé sur** :
- [Pix2Pix](https://github.com/tensorflow/examples/tree/master/tensorflow_examples/models/pix2pix) (TensorFlow Examples)
- Les travaux de [Stanislas Chaillou](https://github.com/StanislasChaillou)

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🐛 Support et Issues

Si vous rencontrez des problèmes ou avez des questions :
1. Consultez les [Issues existantes](https://github.com/votreutilisateur/AIp2p/issues)
2. Créez une nouvelle issue si nécessaire
3. Fournissez des détails sur votre environnement (OS, version Python, GPU, etc.)

---

⭐ **N'hésitez pas à donner une étoile au projet si vous le trouvez utile !**
