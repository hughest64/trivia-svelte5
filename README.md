# Welcome to Trivia Mafia!

The Trivia Mafia app built with SveletKit and Django

## System Dependencies

`redis-server`, `postgresql`, `pyenv`, `pipenv` (python pip install), `node 18.18.0`

## Installation

### SvelteKit

Make sure you have `node >=18.18` then `npm i` to install the dependencies

### Python

`pipenv install` to add the python dependencies

### Environment Variables

The following files are required at the root of the project but are git ignored as the values may vary between environments:\
`.env`

```bash
PUBLIC_API_HOST='http://127.0.0.1:8000'
PUBLIC_WEBSOCKET_HOST='ws://127.0.0.1:8000'
PUBLIC_COOKIE_MAX_AGE=18000
PUBLIC_QUESTION_REVEAL_TIMEOUT=5000
# oauth settings
PUBLIC_GOOGLE_CLIENT_ID=
PRIVATE_GOOGLE_CLIENT_SECRET=
PUBLIC_GOOGLE_CALLBACK_URL=
PUBLIC_GITHUB_CLIENT_ID=
PRIVATE_GITHUB_CLIENT_SECRET=
PUBLIC_GITHUB_CALLBACK_URL=
```

`.env.test`

```bash
PUBLIC_API_HOST='http://127.0.0.1:7000'
PUBLIC_WEBSOCKET_HOST='ws://127.0.0.1:7000'
PUBLIC_QUESTION_REVEAL_TIMEOUT=1000
# oauth
PUBLIC_OAUTH_CALLBACK_URL="http://127.0.0.1:4173/user/google-auth"
```

`.env.django`

```bash
# change to False in production
DEBUG=True
SECRET_KEY="some long random string"
AIRTABLE_API_TOKEN="get this value from last pass"
# This may not be used in the end game but default to False for now, TBD
PRIVATE_EVENT=

# email
MAILGUN_API_KEY=
MAILGUN_USER=
MAILGUN_PASSWORD=
EMAIL_REDIRECT_HOST="http://localhost:5173"
```

## Project Setup

### Databases

Two Postgres databases are used in the project, `triviamafia_main` and a testing database called `triviamafia_tst`

Create the main database:

```bash
# start psql
sudo -u postres psql
# create the triviamafia user and grant privileges (if the user doesn't already exist)
CREATE USER triviamafia WITH PASSWORD 'supergoodpassword';
ALTER USER triviamafia CREATEDB;
# create the db
CREATE DATABASE triviamafia_main OWNER triviamafia;
```

The test database can be created manually as above or with this command _AFTER_ following the migration steps in the next sections.\
`CREATE DATABASE triviamafia_tst WITH TEMPLATE triviamafia_main OWNER triviamafia;`

### Migrations

Migrations are tracked in the repo so there is no need to run `makemigrations` for the inital setup. These commands _WILL_ need to be invoked two times as shown below for all migrations after that. Django explicitly does not migrate multiple databases simeltaneously.

-   `python manage.py makemigrations <appname>` for the standard db
-   `python manage.py makemigrations <appname> --settings=server.settings_tst` for the test database
-   `python manage.py migrate` for the standard db
-   `python manage.py migrate --settings=server.settings_tst` for the test database

### Load Initial Data

-   `python manage.py loaddata game/fixtures/initial.json`
-   `python manage.py loaddata game/fixtures/initial.json --settings=server.settings_tst` (only required if _NOT_ copying the main database)

### Create a Super User

-   `python manage.py createsuperuser` - follow the prompts (same rule to set yourself up in the test database)

## Testing

### Playwright

Add a `playwright/.auth` folder to the root of the project. This is used to store credentials during tests.

You may need to run `npx playwright install` to get the latest browser packages before tests will run properly.

`npm run test` will start a Django dev server on port 7000 using the test database and run all tests.

Tests can also be run directly in vscode if the playwright extension is installed. Just open a test file and click the play button next to the test. (if it works, the extension can be a bit flaky.)

Note that this will use the development database/server which should be running on `127.0.0.01:8000`

See the [testing readme](/tests/README.md) for information on creating Playwright tests and how the test configuration works.

### Django

`python manage.py test` will use the data from `game/fixtures/initial.json` to run tests against the api.

## Development

### Run the Dev Servers

-   With `pipenv` active from `/server` run `python manage.py runserver` to start Django at `localhost:8000`
-   From the root: `npm run dev` to start the SvetleKit dev server at `localhost:5173`

## Deployment

### Setup

-   Example deployment configuration files are located in `/deploy` and they are set up to run the app as a user called `triviamafia`.

### Additional files

-   `server/server/settings_prod.py` with variables for `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
-   `/tmp` folder, this is where the unix socket file is placed for production

### Deployment procedure

`Note` that this is a work in progress, and ideally will be fully automated with pipelines.

1. merge production ready code into the `main` branch
2. from the remote server, `git fetch origin main` then `git pull origin main`
3. if necessary `pipenv run python manage.py migrate` and/or `pipenv run python manage.py collectstatic`
4. run tests, `npm run test` and `pipenv run python manage.py test`
5. if all tests pass, `npm run build` and restart the service(s):
    - `sudo sytemctl restart tmtrivia`
    - `sudo sytemctl restart tmapi`
