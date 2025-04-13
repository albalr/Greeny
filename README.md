# Greeny

Sustainable Mobility App

## Table of Contents

  - [CI/CD Status](#cicd-status)
    - [main branch status](#main-branch-status)
    - [development branch status](#development-branch-status)
  - [Team Members](#team-members)
  - [Conception of the Project](#conception-of-the-project)
  - [Greeny Demo Video](#greeny-demo-video)
  - [How Are Your Points Calculated?](#how-are-your-points-calculated)
  - [Install Release APK on ANDROID Devices](#install-release-apk-on-android-devices)
  - [Instructions to Run the Project](#instructions-to-run-the-project)
    - [Backend](#backend)
      - [Startup](#startup)
      - [Run the corresponding dockers](#run-the-corresponding-dockers)
      - [To apply migrations](#to-apply-migrations)
      - [To create migrations](#to-create-migrations)
    - [Frontend](#frontend)
      - [Setup](#setup)
      - [Run app](#run-app)
      - [Install the app](#install-the-app)

## CI/CD Status

#### main branch status
[![Docker Image CI](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/docker-image.yml) [![Pylint](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/pylint.yml/badge.svg)](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/pylint.yml) [![Django CI](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/django.yml/badge.svg)](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/django.yml) [![Flutter](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/flutter.yml/badge.svg)](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/flutter.yml)

#### development branch status
[![Docker Image CI](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/docker-image.yml/badge.svg?branch=develop)](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/docker-image.yml) [![Pylint](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/pylint.yml/badge.svg?branch=develop)](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/pylint.yml) [![Django CI](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/django.yml/badge.svg?branch=develop)](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/django.yml) [![Flutter](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/flutter.yml/badge.svg?branch=develop)](https://github.com/pes2324q2-gei-upc/Greeny/actions/workflows/flutter.yml)

## Team Members

- Amorín Díaz, Miquel
- Costabella Moreno, Agustí
- López Buira, Iván
- López Ruiz, Alba 
- Mostazo Gonzalez, Marc
- Tajahuerce Brulles, Arnau
- Vega Centeno, Javier

<a href="https://github.com/pes2324q2-gei-upc/Greeny/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=pes2324q2-gei-upc/Greeny" />
</a>

## Conception of the project

<p align="center">
  <img src="https://github.com/pes2324q2-gei-upc/Greeny/blob/develop/App/greeny/assets/icons/appicon.png?raw=true" alt="Greeny Logo" width="200"/>
</p>

El nostre projecte consisteix en una aplicació mòbil que té com a idea principal un concepte innovador: un joc interactiu orientat en la sostenibilitat urbana, centrat en l'objectiu de descontaminar una ciutat. Mitjançant una aplicació mòbil, els usuaris tindran l'oportunitat de participar activament en aquest desafiament ambiental. A través de mecàniques de joc inspiradores i educatives, els jugadors seran responsables de prendre decisions sobre els seus desplaçaments diaris i, al mateix temps, contribuir a la reducció de la contaminació i al creixement de la sostenibilitat urbana.

La proposta del nostre projecte ofereix una experiència lúdica única, on els usuaris no només reben informació sobre punts de recàrrega elèctrica, estacions de Bicing i parades de transport públic, sinó que també es converteixen en protagonistes de la transformació d'una ciutat contaminada en un entorn més saludable i sostenible. Amb una combinació de gamificació, geolocalització i interacció social, aspirem a crear una plataforma que no només entretingui, sinó que també eduqui i motivi els usuaris a adoptar hàbits de vida més respectuosos amb el medi ambient. Així, el nostre projecte no només és una aplicació mòbil, sinó una iniciativa per a la conscienciació i la millora de la sostenibilitat urbana.

---

Our project consists of a mobile application whose main idea is based on an innovative concept: an interactive game focused on urban sustainability, centered on the goal of decontaminating a city. Through a mobile application, users will have the opportunity to actively participate in this environmental challenge. Through inspiring and educational game mechanics, players will be responsible for making decisions about their daily commutes while contributing to pollution reduction and the growth of urban sustainability.

The proposal of our project offers a unique playful experience, where users not only receive information about electric charging points, Bicing stations, and public transport stops, but also become the protagonists of transforming a polluted city into a healthier and more sustainable environment. With a combination of gamification, geolocation, and social interaction, we aim to create a platform that not only entertains but also educates and motivates users to adopt more environmentally friendly lifestyles. Thus, our project is not just a mobile application, but an initiative for raising awareness and improving urban sustainability.

## Greeny Demo Video

El següent vídeo conté una **demostració de totes les funcionalitats** de l'aplicació Greeny:

---

The following video demonstrates **all the features** of the Greeny app:

https://github.com/pes2324q2-gei-upc/Greeny/assets/105717367/43e15f08-8ca2-4931-bd7d-539c0da111dd

## How Are Your Points Calculated?

Using this formula:
```py
def calculate_points(co2_consumed, car_co2_consumed):
    # Calculate the points earned by the user
    alpha = 1 if co2_consumed == 0 else car_co2_consumed / co2_consumed
    co2_saved = max(0, car_co2_consumed - co2_consumed)
    total_points = co2_saved * alpha

    multiplier = 20

    return int(round(total_points * multiplier))
```
La fórmula calcula la **diferència entre el CO2 consumit i el CO2 que hauries consumit** fent la ruta en un cotxe de combustió.
> En conseqüència en fer una ruta en cotxe de combustió no es guanyaran punts, ja que no s'ha estalviat CO2.

---

The formula calculates the **difference between the CO₂ consumed and the CO₂ that would have been consumed** if the route had been taken using a combustion car.  
> As a result, taking a route with a combustion car will not earn points, since no CO₂ has been saved.

## Install Release APK on ANDROID Devices

Instalar l'aplicació [Greeny.apk](https://github.com/pes2324q2-gei-upc/Greeny/releases/latest/download/Greeny-release.apk) de la [Última Release](https://github.com/pes2324q2-gei-upc/Greeny/releases/latest) al teu dispositiu.

---

Install the app [Greeny.apk](https://github.com/pes2324q2-gei-upc/Greeny/releases/latest/download/Greeny-release.apk) from [Last Release](https://github.com/pes2324q2-gei-upc/Greeny/releases/latest) in your device.

## Instructions to Run the Project

### Backend
#### Startup:

1. Baixarse el repo

2. Instal·lar-se docker

3. Situarse a la carpeta backend

---

1. Clone the repo

2. Install Docker

3. Navigate to the backend folder

#### Run the corresponding dockers

```sh
docker-compose build
docker compose up
```

#### To apply migrations

```sh
docker compose run backend python manage.py migrate
```


#### To create migrations

```sh
docker compose run backend python manage.py makemigrations
```

> **Note:** Assegurat de posar al `./Backend/.env` les variables d'entorn necessaries:
>```
>POSTGRES_NAME=
>POSTGRES_USER=
>POSTGRES_PASSWORD=
>POSTGRES_DB=
>DB_HOST=
>API_KEY=
>API_KEY_ID=
>APP_TOKEN=
>APP_ID=
>API_TOKEN_AJT=
>```

### Frontend
> **Macos:** Descarregar `cocoapod`

#### Setup
1. Instal·lar extensió flutter a vscode (potser també instalar flutter)
2. Instal·lar emulador mobil (Xcode/Android Studio)

#### Run app
1. A baix a la dreta de vscode seleccionar un dispositiu per executar el front end
2. Seleccionar l'arxiu `./App/greeny/lib/main.dart`
3. Donar-li a `Start debugging`.

#### Install the app
```sh
flutter run --release
```

> **Note:** Assegurat de posar al `./App/greeny/.env` el `BACKEND_URL=` necessari:
>
> `BACKEND_URL = 'url o IP del backend'`
>
> Per defecte: `BACKEND_URL = 'nattech.fib.upc.edu:40351'`

## Folder Sctructure

```
.
├── App
│   └── greeny
│       ├── analysis_options.yaml
│       ├── android
│       ├── assets          # App assets directory
│       ├── build
│       ├── greeny.iml
│       ├── ios
│       ├── lib             # Main code of the app
│       ├── linux
│       ├── macos
│       ├── pubspec.lock
│       ├── pubspec.yaml    # Dart package manager config (dependencies, etc.)
│       ├── test            # Frontend test directory
│       ├── web
│       └── windows
├── Backend
│   ├── Dockerfile          # Docker instructions to build backend image
│   ├── api                 # Backend API code
│   ├── docker-compose.yml  # Docker container configuration
│   ├── greeny
│   ├── manage.py
│   ├── uploads/imatges     # Profile pictures for registered users
│   └── requirements.txt    # Backend dependencies
├── LICENSE.md              # Apache license
└── README.md               # This file
```
