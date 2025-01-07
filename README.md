# Système de Contrôle Multimédia par Reconnaissance de Gestes

Ce projet est un **système de contrôle multimédia** en temps réel utilisant la reconnaissance de gestes à partir d'une webcam. Il permet de contrôler des actions telles que la lecture/pause, l'augmentation ou la diminution du volume, et le changement de vidéo en utilisant des gestes simples de la main.

## Fonctionnalités

- **Lecture/Pause** : Contrôle la lecture d'une vidéo en utilisant un geste spécifique.
- **Augmentation/Diminution du volume** : Ajuste le volume grâce à des gestes vers le haut ou vers le bas.
- **Changement de vidéo** : Permet de passer à la vidéo suivante ou précédente avec des mouvements latéraux de la main.
- **Interface propre et intuitive** : L'affichage se fait sans superposition de points ou d'annotations inutiles sur la main, offrant une interface claire.

## Technologies utilisées

- **Python 3.9**
- **OpenCV** : Pour capturer et afficher les images de la webcam.
- **Mediapipe** : Pour la détection des mains et l'extraction des points clés.
- **TensorFlow/Keras** : Pour le modèle de classification des gestes.
- **PyAutoGUI** : Pour simuler les actions multimédias (espace, volume, etc.).
- **Tkinter** : Pour l'interface graphique.

## Installation

1. Clonez le dépôt Git :
   ```bash
   git clone https://github.com/Hamdaoui1/Systeme_de_Controle.git
   cd Systeme_de_Controle
   ```

2. Créez un environnement virtuel et activez-le :
   ```bash
   python -m venv env
   source env/bin/activate  # Pour Linux/Mac
   env\Scripts\activate     # Pour Windows
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. Exécutez le fichier principal :
   ```bash
   python main.py
   ```

2. Une fenêtre s'ouvrira, affichant la vidéo en temps réel de la webcam.
3. Réalisez les gestes suivants pour contrôler les actions multimédias :
   - **Lecture/Pause** : Geste de la main ouverte.
   - **Augmenter le volume** : Geste avec un doigt pointé vers le haut.
   - **Diminuer le volume** : Geste avec un doigt pointé vers le bas.
   - **Vidéo suivante** : Mouvement latéral de la main vers la droite.
   - **Vidéo précédente** : Mouvement latéral de la main vers la gauche.

## Structure du projet

```
Systeme_de_Controle/
├── data/                      # Données utilisées pour l'entraînement
├── main.py                    # Script principal
├── collecte.py                # Script de collecte des données
├── entrainement.py            # Script d'entraînement du modèle
├── test.py                    # Script de test
├── requirements.txt           # Fichier des dépendances
└── README.md                  # Documentation du projet
```

## Améliorations possibles

- Ajouter des gestes supplémentaires pour d’autres actions multimédias.
- Améliorer l’algorithme de détection pour une reconnaissance plus rapide et plus précise.
- Ajouter la prise en charge de plusieurs langues pour l'interface.

## Auteurs

- **Hamdaoui1** - [GitHub](https://github.com/Hamdaoui1)

## Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, le modifier et le distribuer.
```

