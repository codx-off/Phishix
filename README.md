# Phishix

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-orange)
![Requests](https://img.shields.io/badge/Requests-2.x-red)
![License](https://img.shields.io/badge/License-MIT-green)

**Phishix** est un outil **démonstratif** pour récupérer la localisation d’un utilisateur **avec consentement** via un lien web sécurisé.  

> ⚠️ **Attention** : Utilisez cet outil uniquement à des fins légales et éducatives.  
> L’utilisation pour espionner quelqu’un sans consentement est **illégale**.

---

## Fonctionnalités

- Dashboard administrateur local pour générer des liens de partage.
- Page minimaliste responsive pour les visiteurs.
- Demande automatique de géolocalisation (popup de consentement obligatoire).
- Envoi des coordonnées GPS précises à un webhook Discord.
- Stockage des événements (IP, User-Agent, lat/lon, timestamp) consultables depuis le dashboard.
- Compatible **localhost** et **ngrok** pour tests sécurisés et distants.

---

## Prérequis

- Python 3.10+
- Pip
- Git
- Navigateur moderne (Chrome, Firefox, Safari, Edge)
- Connexion internet pour ngrok (HTTPS obligatoire pour mobile)

---

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/codx-off/StarPhish.git
cd Phishix

# Installer les dépendances
pip install flask requests


