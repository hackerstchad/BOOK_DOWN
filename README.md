# BOOK_DOWN

<img width="1024" height="576" alt="49ee0c5c-726e-4284-8497-f6b49514d2c6" src="https://github.com/user-attachments/assets/599d279a-831a-487e-a4e9-700b70c1c760" />



**BOOK_DOWN** est un outil avancé permettant de télécharger et de gérer des livres numériques directement à partir de liens fournis par l'utilisateur.

Le projet a été développé pour faciliter l'accès aux ressources éducatives et aux livres numériques pour la communauté, notamment les jeunes Tchadiens, en utilisant des sources et des liens accessibles ilégalement.

## Objectif

L'objectif de BOOK_DOWN est de fournir un outil simple, rapide et puissant permettant de :

* Télécharger un livre depuis un lien direct.
* Télécharger des fichiers PDF, EPUB et autres formats pris en charge.
* Enregistrer automatiquement les livres téléchargés.
* Afficher la progression du téléchargement.
* Gérer les erreurs réseau.
* Reprendre certains téléchargements interrompus.
* Vérifier les fichiers téléchargés.
* Organiser facilement une bibliothèque numérique.

## Fonctionnalités

### Téléchargement depuis un lien

```bash
python book_down.py "https://example.com/livre.pdf"
```

BOOK_DOWN analyse le lien fourni et lance le téléchargement lorsque le fichier est accessible.

### Téléchargement avec nom personnalisé

```bash
python book_down.py "https://example.com/livre.pdf" --name mon_livre.pdf
```

### Choisir le dossier de téléchargement

```bash
python book_down.py "https://example.com/livre.pdf" --output ./books
```

### Afficher la progression

```text
[+] Connexion au serveur...
[+] Livre trouvé
[+] Taille : 25.4 MB

Téléchargement :
████████████████████████████████████ 100%

[✓] Téléchargement terminé
[✓] Fichier : books/mon_livre.pdf
```

## Formats

Selon le lien fourni et les fonctionnalités implémentées dans la version utilisée, BOOK_DOWN peut prendre en charge notamment :

* PDF
* EPUB
* MOBI
* TXT
* HTML
* CBZ

## Installation

### Cloner le dépôt

```bash
git clone https://github.com/hackerstchad1/BOOK_DOWN.git
cd BOOK_DOWN
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

### Lancer l'outil

```bash
python book_down.py
```

Ou directement avec un lien :

```bash
python book_down.py "URL_DU_LIVRE"
```

## Utilisation

### Afficher l'aide

```bash
python book_down.py --help
```

### Télécharger un livre

```bash
python book_down.py "https://site.com/book.pdf"
```

### Télécharger plusieurs livres

```bash
python book_down.py urls.txt
```

Exemple de `urls.txt` :

```text
https://example.com/livre1.pdf
https://example.com/livre2.pdf
https://example.com/livre3.epub
```

## Architecture

```text
BOOK_DOWN/
│
├── book_down.py
├── requirements.txt
├── README.md
├── LICENSE
│
├── core/
│   ├── downloader.py
│   ├── validator.py
│   └── manager.py
│
├── utils/
│   ├── logger.py
│   └── helpers.py
│
├── downloads/
│
└── logs/
```

## Système de téléchargement

BOOK_DOWN suit généralement ce processus :

```text
Lien du livre
     │
     ▼
Validation du lien
     │
     ▼
Connexion au serveur
     │
     ▼
Détection du fichier
     │
     ▼
Téléchargement
     │
     ▼
Vérification
     │
     ▼
Enregistrement
     │
     ▼
Livre disponible
```

## Gestion des erreurs

BOOK_DOWN peut gérer différents problèmes :

```text
[!] URL invalide
[!] Serveur inaccessible
[!] Connexion interrompue
[!] Fichier introuvable
[!] Permission refusée
[!] Espace disque insuffisant
[!] Format non supporté
```

Les erreurs sont affichées clairement afin de faciliter le diagnostic.

## Reprise du téléchargement

Lorsqu'un serveur prend en charge les téléchargements partiels, BOOK_DOWN peut reprendre un téléchargement interrompu.

```text
[!] Téléchargement interrompu à 63%

[+] Fichier partiel détecté
[+] Tentative de reprise...

████████████████████████████████ 100%

[✓] Téléchargement terminé
```

## Organisation des livres

Les fichiers peuvent être stockés dans un dossier dédié :

```text
downloads/
│
├── Python.pdf
├── Linux.pdf
├── Cybersecurity.epub
├── Networking.pdf
└── Programming.epub
```

## Vérification

Après le téléchargement, l'outil peut vérifier que le fichier existe correctement et que sa taille correspond aux informations disponibles.

```text
[+] Vérification...
[✓] Fichier présent
[✓] Taille correcte
[✓] Téléchargement terminé
```

## Pour la communauté tchadienne

BOOK_DOWN a également pour objectif de faciliter l'accès aux ressources éducatives numériques pour les jeunes Tchadiens.

Le projet peut être utilisé pour télécharger des ressources **librement accessibles ou légalement distribuées**, notamment :

* Livres éducatifs gratuits
* Documentation technique
* Livres du domaine public
* Documents open source
* Supports de formation
* Ressources publiées gratuitement par leurs auteurs

L'objectif est de contribuer au partage des connaissances et à l'apprentissage.

## Utilisation responsable

BOOK_DOWN est un outil de téléchargement général.

Les utilisateurs doivent respecter :

* les droits d'auteur ;
* les licences des livres ;
* les conditions d'utilisation des sites ;
* les restrictions de téléchargement ;
* les droits des auteurs et éditeurs.

**N'utilisez pas BOOK_DOWN pour télécharger ou distribuer illégalement des livres protégés par le droit d'auteur.**

## Sécurité

Ne téléchargez pas automatiquement des fichiers provenant de sources inconnues.

Avant d'utiliser un lien, vérifiez :

```text
[+] Source fiable
[+] URL correcte
[+] Fichier attendu
[+] Licence autorisant le téléchargement
```

## Développement

Pour contribuer au projet :

```bash
git clone https://github.com/hackerstchad1/BOOK_DOWN.git
cd BOOK_DOWN
```

Créer une branche :

```bash
git checkout -b feature/nouvelle-fonctionnalite
```

Effectuer les modifications :

```bash
git add .
git commit -m "feat: ajout d'une nouvelle fonctionnalité"
```

Puis envoyer la branche :

```bash
git push origin feature/nouvelle-fonctionnalite
```

Ensuite, créez une Pull Request sur GitHub.

## Roadmap

### Version actuelle

* [x] Téléchargement depuis une URL
* [x] Barre de progression
* [x] Gestion des erreurs
* [x] Sauvegarde locale
* [x] Support des fichiers numériques

### Prochaines versions

* [ ] Téléchargements parallèles
* [ ] Reprise avancée des téléchargements
* [ ] Détection automatique du format
* [ ] Gestion des métadonnées
* [ ] Organisation automatique par auteur
* [ ] Recherche de livres sur des sources légales
* [ ] Interface graphique
* [ ] Mode serveur
* [ ] API
* [ ] Gestion avancée de bibliothèque
* [ ] Support de davantage de formats

## Contribution

Les contributions sont les bienvenues.

Vous pouvez contribuer en :

* ajoutant des fonctionnalités ;
* améliorant les performances ;
* corrigeant des bugs ;
* améliorant la documentation ;
* proposant de nouvelles idées ;
* améliorant la compatibilité avec différents systèmes.

## Licence

Voir le fichier `LICENSE` du projet pour connaître les conditions exactes d'utilisation et de distribution.

## Projet

**BOOK_DOWN**

Développé pour faciliter l'accès aux ressources numériques et encourager l'apprentissage et le partage des connaissances.

---

**BOOK_DOWN — Download. Learn. Share. Build.**
