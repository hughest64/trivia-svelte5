# Triva Mafia - SvelteKit Edition

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
For simplicity the default `sqlite` is used
### Migrations
- `python manage.py makemigrations user`
- `python manage.py makemigrations game`
- `python manage.py migrate`
### Load Seed Data
- `python manage.py loaddata fixtures/dbdump.json`
### SuperUser
- `python manage.py createsuperuser` - follow the prompts
- it's not currently possible to create teams in the ui, so you'll have to add yourself to one or more in the admin

## Run the Dev Servers
- With `pipenv` active from the `server` dir run `python manage.py runserver` to start Django at `localhost:8000`
- From the root run `npm run dev` to start the SvetleKit dev server at `localhost:5173`

## Run Playwright tests
There are multiple methods for running tests. Using the provided vscode task `run-tests` is the easiest way. 
This will start a Django test server at `localhost:7000`. Playwright will build the app and run tests against it. 
This keeps the actual database isolated and prevents possible false negatives. Expect 2-3 flaky tests and ~56 passing tests.

`npm run test` will run all tests against the dev database and requires Django to be running on port 8000.

Tests can also be run directly in vscode if the playwright extension is installed. Just open a test file and click the play button 
next to the test. This also uses the dev database and Django must be running on port 8000

Note that the dev database must be in "fresh" state for all tests to pass meaning that round locks, question reveals, and responses
need to be in the state of a brand new game.

You can use the command `python manage.py reset` to reset the database before the test run. 
Subsequent test runs are guaranteed to have a "fresh" state as the tests themselves reset the data frequently.
