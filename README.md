# Analyse de la corruption des bits dans les trames


## Structure du projet

Le projet est organisé de la manière suivante :

BITS-CORRUPTION-PY
├───data
│   ├───BIT_CSV
│   └───DATA_CSV
└───dev

### Dossier `data`

Ce dossier contient deux sous-dossiers :

- **BIT_CSV** : Contient les fichiers CSV relatifs aux bits corrompus pour chaque trame dans les différentes expériences (IUT-1 à IUT-8).
- **DATA_CSV** : Contient les fichiers CSV relatifs aux informations générales des trames (ex: pktId, SNR, longueur, statut, etc.) pour les expériences IUT-1 à IUT-8.

### Dossier `dev`

Ce dossier contient les scripts Python utilisés pour l'analyse et la visualisation des données de corruption des bits.

- **corruption_frequency.py** : Ce script calcule la fréquence d'apparition des bits corrompus dans chaque trame pour chaque expérience.
- **histo_longueur.py** : Ce script trace un histogramme représentant la longueur maximale de la séquence de bits consécutifs corrompus dans chaque trame.
- **histo_sans_fft.py** : Ce script trace un histogramme du nombre total de bits corrompus par trame, sans appliquer de transformée de Fourier.
- **histo_fft.py** : Ce script trace le même histogramme du nombre total de bits corrompus par trame, mais applique une transformée de Fourier pour extraire des motifs périodiques dans la série de données.

#### Auteurs

Akram EL HADHOUDI
Mahmoud KHOUBJI

