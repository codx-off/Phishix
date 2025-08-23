# 🐟 Phishix

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-2.x-orange?style=for-the-badge)
![Requests](https://img.shields.io/badge/Requests-2.x-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Phishix** est un outil **démonstratif** pour récupérer la localisation d’une personne via une url web.

> ⚠️ **Attention** : Utilisez cet outil uniquement à des fins **légales et éducatives**.  
> L’utilisation pour espionner quelqu’un sans consentement est **illégale**.

---

## ✨ Fonctionnalités

- Dashboard pour générer des url piégé.
- Page minimaliste moderne et intuitive.
- Demande automatique de géolocalisation (popup du navigateur).
- Envoi des coordonnées GPS précises à un **webhook Discord**.
- Stockage des événements (**IP, User-Agent, latitude/longitude, timestamp**) consultables depuis le dashboard.
- Compatible **localhost** et **ngrok**
- 🔐 **Login par défaut** :  
  - **USERNAME** = `Phishix`  
  - **PASSWORD** = `Phishix2025`

---

## ⚙️ Prérequis

- Python 3.10+
- Pip
- Git
- Navigateur moderne (Chrome, Firefox, Safari, Edge)
- Connexion internet pour ngrok (HTTPS obligatoire pour mobile)

---

## 🚀 Installation

```bash
# Cloner le dépôt
git clone https://github.com/codx-off/Phishix.git
cd Phishix

# Installer les dépendances
pip install flask requests

# Lancer le serveur
python phishix.py
```
# 🖥️ En local
Ouvrir :
```bash
http://127.0.0.1:5000/admin
```

# 🌐 Avec Ngrok
1. Installer ngrok  
2. Ouvrir un terminal et taper :  
```bash
ngrok http 5000
```
Ouvrir :
```bash
https://<ton_url_ngrok>/admin
```

