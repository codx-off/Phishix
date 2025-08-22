# StarPhish

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-orange)
![Requests](https://img.shields.io/badge/Requests-2.x-red)
![License](https://img.shields.io/badge/License-MIT-green)

**StarPhish** est un outil **démonstratif** pour récupérer la localisation d’un utilisateur **avec consentement** via un lien web sécurisé.  

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
cd StarPhish

# Installer les dépendances
pip install flask requests
Utilisation
1️⃣ Lancer ngrok (HTTPS requis pour la géolocalisation)
bash
Copier
Modifier
ngrok http 5000
Ngrok fournira un lien HTTPS du type :

arduino
Copier
Modifier
https://abcd-1234.ngrok-free.app
2️⃣ Lancer l’application StarPhish
bash
Copier
Modifier
python starphish.py
L’application démarre sur localhost:5000.

3️⃣ Accéder au dashboard admin
Ouvrir dans le navigateur :

arduino
Copier
Modifier
https://<lien_ngrok>/admin
Remplir les champs :

Label (optionnel)

Discord webhook URL

Cliquer sur Générer le lien.

Le lien généré ressemblera à :

bash
Copier
Modifier
https://<lien_ngrok>/go/<id>
4️⃣ Partager le lien avec un utilisateur consentant
Lorsqu’un utilisateur ouvre le lien /go/<id> :

La page affiche un écran de loading minimaliste et responsive.

Le navigateur demande la permission de partager la géolocalisation.

Si l’utilisateur accepte, les coordonnées sont envoyées au webhook configuré.

La page devient blanche après l’envoi.

5️⃣ Consulter les événements
Dashboard des événements :

arduino
Copier
Modifier
https://<lien_ngrok>/events
Affiche :

Timestamp

Label

IP

User-Agent

Latitude / Longitude + précision

Lien Google Maps

OS compatibles
Windows (recommandé)

Linux

macOS

Pour tests mobiles, utiliser le lien ngrok HTTPS.

Sécurité & éthique
Les informations collectées ne doivent être obtenues qu’avec le consentement explicite de l’utilisateur.

Les webhooks sont configurés côté serveur, jamais exposés dans le lien.

La page /go/<id> utilise la popup officielle du navigateur pour demander la localisation.

Contribuer
Fork le dépôt

Crée une branche :

bash
Copier
Modifier
git checkout -b feature/ma-fonctionnalité
Commit tes changements :

bash
Copier
Modifier
git commit -m "Ajout d'une fonctionnalité"
