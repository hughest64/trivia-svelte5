# Trivia Mafia - SvelteKit Edition

A demonstration of the Trivia Mafia app using the awesome SvelteKit framework and Django as an api backend.

## Installation

### SvelteKit
Make sure you have `node >=16` then `npm i` to install the dependencies

### Python
`cd server` then `pipenv install` to add the python dependencies

### Environment Variables
All required `.env` settings for development and testing are included in the repo

## Project Setup
### Database
`TODO:` update with postgres information for standard and test databases\
`NOTE:` it might just be easier to make a copy of the standard db to create the test db for the initial setup
For simplicity the default `sqlite` is used
### Migrations
Migrations are tracked in the repo so there is no need to run `makemigrations` for the inital setup. After the initial setup commands will need to be invoked two times as shown below. Django explicitly does not migrate multiple databases simeltaneously.
- `python manage.py makemigrations <app>` for the standard db
- `python manage.py makemigrations <app> --settings=server.settings_tst` for the test database
- `python manage.py migrate` for the standard db
- `python manage.py migrate --settings=server.settings_tst` for the test database

### Load Initial Data
Again, two commands are required
- `python manage.py loaddata game/fixtures/initial.json`
- `python manage.py loaddata game/fixtures/initial.json --settings=server.settings_tst`
### Create a Super User
- `python manage.py createsuperuser` - follow the prompts (same rule to set yourself up in the test database)

## Testing
### Playwright

`npm run test` will start a Django dev server on port 7000 using the test database and run all tests.

Tests can also be run directly in vscode if the playwright extension is installed. Just open a test file and click the play button 
next to the test. (if it works, the extension can be a bit flaky)

### Django
`python manage.py test` will use the data from `game/fixtures/initial.json` to run tests against the api.

## Development
### Run the Dev Servers
- With `pipenv` active from `/server` run `python manage.py runserver` to start Django at `localhost:8000`
- From the root: `npm run dev` to start the SvetleKit dev server at `localhost:5173`
