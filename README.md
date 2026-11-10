# AI-Powered SOC Assistant

Détection d'attaques réseau par machine learning, pensée comme brique d'un
centre opérationnel de sécurité (SOC) : classification du trafic, évaluation
orientée risque, puis tableau de bord et explication des alertes (en cours).

## Contexte
Un analyste SOC reçoit des milliers d'alertes. Ce projet étudie jusqu'où un
modèle peut détecter les attaques tout en limitant les fausses alertes.

## Données
UNSW-NB15 : fichiers `training-set` et `testing-set` à placer dans `data/`.
Le trafic est étiqueté normal ou attaque, avec la catégorie d'attaque
(DoS, Exploits, Reconnaissance, etc.).

## Méthodologie
1. **Exploration** : répartition des classes, valeurs manquantes, doublons.
2. **Prétraitement** : suppression de `id` et des doublons, encodage ordinal de
   `proto`, `service`, `state` ajusté sur le train uniquement, exclusion de
   `label` et `attack_cat` des entrées (pas de fuite de données).
3. **Modélisation** : Random Forest et XGBoost.
4. **Évaluation** : Precision, Recall, F1, matrices de confusion, étude du
   seuil de décision.

## Résultats (seuil 0,5)

| Modèle | Precision (Attaque) | Recall (Attaque) | F1 | Accuracy |
|---|---|---|---|---|
| Random Forest | 0,71 | 0,98 | 0,82 | 0,83 |
| XGBoost | 0,71 | 0,97 | 0,82 | 0,83 |

![Matrices de confusion](docs/confusion_matrices.png)
![Importance des variables](docs/feature_importance.png)

**Lecture :** plus de 97 % des attaques sont détectées, mais environ 26 % du
trafic normal est signalé à tort. Cet écart est en partie lié à la différence
de distribution entre les fichiers train et test d'UNSW-NB15.

## Structure

    ai-soc-assistant/
    ├── notebooks/   exploration, prétraitement, entraînement
    ├── src/         preprocess.py, train.py
    ├── docs/        figures
    ├── data/        jeux de données (non versionnés)
    └── models/      modèles sauvegardés (non versionnés)

## Lancer le projet

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python src/train.py

## Limites et suite
- Faux positifs élevés : réglage du seuil et analyse par type d'attaque.
- À venir : tableau de bord Streamlit, résumé des alertes par un LLM local avec
  correspondance MITRE ATT&CK, conteneurisation Docker.

## Auteur
Mohamed Yassine Miladi, étudiant ingénieur en informatique (cloud et
cybersécurité), ESPRIT.