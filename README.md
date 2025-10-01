# wlmath

CLUB CRAWL BRANCH! Anonymous users can solve problems, and an email is prompted after the user solves the problem.

Emails are written to `./winning_emails.txt`.

## setup

```
python3 -m venv .venv

# Linux/MacOS
source .venv/bin/activate
# Windows (command prompt)
.venv/Scripts/activate.bat
# Windows (PowerShell)
.venv/Scripts/activate.ps1

pip install -r requirements.txt

# Django setup
python manage.py migrate --run-syncdb
python manage.py populate_categories
python manage.py createsuperuser
python manage.py runserver

# Tailwind setup
npm i
npm run watch

# Run `python manage.py runserver` and `npm run watch` in separate terminal tabs. Enjoy the website!
```
