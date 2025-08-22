# StarPhish

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-orange)
![Requests](https://img.shields.io/badge/Requests-2.x-red)
![License](https://img.shields.io/badge/License-MIT-green)

**StarPhish** est un outil **démonstratif** permettant de récupérer la localisation avec le consentement explicite de l’utilisateur via un lien web sécurisé.  

> ⚠️ **Attention** : Utiliser cet outil **uniquement à des fins légales et éducatives**.  
> L’utilisation pour espionner quelqu’un sans consentement est **illégale** et peut entraîner des sanctions civiles et pénales.

---

## Fonctionnalités

- Dashboard administrateur local pour générer des liens de partage.
- Page minimaliste et responsive pour les visiteurs.
- Demande automatique de la géolocalisation du navigateur (popup de consentement obligatoire).
- Envoi des coordonnées GPS précises à un webhook Discord.
- Stockage des événements (IP, User-Agent, lat/lon, timestamp) pour consultation via le dashboard.
- Compatible `localhost` et ngrok pour tests sécurisés et distants.

---

## Prérequis

- Python 3.10 ou supérieur
- Pip
- Git
- Navigateur moderne (Chrome, Firefox, Safari, Edge)
- Connexion internet pour ngrok si vous utilisez la version distante

---

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/codx-off/StarPhish.git
cd StarPhish

# Installer les dépendances
pip install flask requests
