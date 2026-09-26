# ENSA Safi - Gestion des notes

Application web développée avec Python et Streamlit pour gérer les notes des étudiants CP1 et CP2.

## 1. Installation

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Windows :

```bash
.venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## 2. Lancer l'application

```bash
streamlit run app.py
```

L'application sera disponible à l'adresse affichée par Streamlit, généralement :

`http://localhost:8501`

## 3. Connexion

Deux espaces sont disponibles :

- CP1
- CP2

Mot de passe :

`123456789`

## 4. Fonctionnalités

- Tableau de bord
- Gestion des notes
- Ajout de notes
- Recherche par étudiant
- Filtrage par module et semestre
- Statistiques
- Graphiques Matplotlib / Seaborn
- Export CSV
- Persistance des données dans `dataset.csv`

## 5. Structure

```text
ensa_notes/
├── app.py
├── requirements.txt
├── dataset.csv
└── README.md
```

## Remarque

Le mot de passe est volontairement simple pour un projet pédagogique. Pour une utilisation réelle, il faudrait utiliser un système d'authentification sécurisé avec des mots de passe hashés et une base de données.
