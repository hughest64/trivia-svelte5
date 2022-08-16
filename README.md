# TrivaMafia SvelteKit Concept

A re-platformed re-conceived version of the trivia app intended to provide more flexibility, better scalability, easier implementation of new features, and better testing patterns.

## Installation

### SvelteKit

-   SvelteKit requires `node >= 16`, so make sure that is installed and active.
-   For convenience there is a `.nvmrc` file at the root which will automatically load the correct version in this directory. This is only useful if you are using Node Version Manager.
-   with node 16 active, run `npm i` to install the dependencies

### Python

-   from the `server` directory run `pipenv install` to add the python dependencies

### Environment Variables

-   create a `.env` file at the root and add the following variables which are requried for running the dev server

```bash
VITE_API_HOST = 'http://localhost:8000'

VITE_WEBSOCKET_HOST = 'ws://localhost:8000'
```

## Project Setup

`NOTE:` There is no need to use the `createsuperuser` command here, that is handled in the setup script described below.\
All commands need to be run from the server dirctory with `pipenv` active.

-   do the initia datbase migration with `python manage.py migrate`
-   run the database setup script with `python manage.py dbsetup` this will allow you to optionally create a superuser as well as create the example teams and guest user/team for the app

## Run the Dev Servers

-   python - with `pipenv` active from the `server` run `python manage.py runserver`
-   SvelteKit - from the root run `npm run dev`

## Testing

-   TODO
