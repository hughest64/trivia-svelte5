# TrivaMafia SvelteKit Concept
A re-platformed re-conceived version of the trivia app intended to provide more flexibility, better scalability, easier implementation of new features, and better testing patterns.

## Installation
### SvelteKit
- SvelteKit requires `node >= 16`, so make sure that is installed and active.
- For convenience there is a `.nvmrc` file at the root which will automatically load the correct version in this directory. This is only useful if you are using Node Version Manager.
- with node 16 active, run `npm i` to install the dependencies

### Python
- from the `server` directory run `pipenv install` to add the python dependencies

### Environment Variables
- create a `.env` file at the root and add the following variables which are requried for running the dev server

```python
VITE_API_HOST = 'http://localhost:8000'

VITE_WEBSOCKET_HOST = 'ws://localhost:8000'
```

## Project Setup
- TODO: (db migrations, add users, add teams, etc)

## Run the Dev Servers
- python - with `pipenv` active from the `server` run `python manage.py runserver`
- SvelteKit - from the root run `npm run dev`

## Building for Production
- TODO