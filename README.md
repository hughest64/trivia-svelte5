# TrivaMafia - SvelteKit Edition

A demonstartion of the Trivia Mafia app using the awesome SvelteKit framwork and Django as an api backend.

## Installation

### SvelteKit
Make sure you have `node >=16` then `npm i` to install the dependencies

### Python
`cd server` then `pipenv install` to add the python dependencies

### Environment Variables
 create a `.env` file at the root with the following values
```bash
VITE_API_HOST = 'http://127.0.0.1:8000'
VITE_WEBSOCKET_HOST = 'ws://127.0.0.1:8000'
PUBLIC_COOKIE_MAX_AGE=60
PUBLIC_SECURE_COOKIE=
PUBLIC_QUESTION_REVEAL_TIMEOUT=5000
```

## Project Setup
### Database
For simplicity the default `sqlite` is used
### Migrations
- `python manage.py makemigrations user`
- `python manage.py makemigrations game`
- `python manage.py migrate`
### Load Fixture Data
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

In order to use the vscode task you will need to create a `.env.test` file with the following parameters:
```bash
PUBLIC_QUESTION_REVEAL_TIMEOUT=1000 # 1 second for tests
PUBLIC_API_HOST='http://127.0.0.1:7000'
PUBLIC_WEBSOCKET_HOST='ws://127.0.0.1:7000'
```
This will reduce the question reveal time to 1 second to help speed up tests and build the app using the test-db port to connect to the api.

Tests can be run from the command line with `npm run test`. This runs all tests against the dev database
Tests can also be run directly in vscode if the playwright extension is installed. Just open a test file and click the play button
next to the test. This runs tests against the dev database and django must be running on port 8000

Note that the dev database must be in "fresh" state for all tests to pass meaning that round locks, question reveals, and responses
need to be in the state of a brand new game.

You can use the command `python manage.py reset` to reset the database before the test run (this should be automated at the start of each test run).
Subsequent test runs are guaranteed to have a "fesh" state as the tests themselves reset the data frequently.
