#!bin/bash

# w/ sudo?
cd /opt/tm-trivia
git reset --hard &&
pull origin main &&
npm i &&
npm run build &&
pipenv install &&
cd /server &&
pipenv run python manage.py collectstatic --no-input &&
pipenv run python manage.py migrate

# definitely w/ sudo
sudo systemctl restart tm-trivia.service
sudo systemctl restart tm-trivia-api.service
