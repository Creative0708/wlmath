# wlmath

wlmath (alternatively stylized wlmath) is an online platform for the Mackenzie Math Club to host individual problems, weekly contests, mock contests, video explanations, and more. It will feature leaderboards for various criteria (problems solved, etc) and an admin panel for execs and teachers to add problems to the website.
It will soon exist on the first of October, 2025.
### 1st of October, 2025 update:
As funding has not been recieved yet, proper deployment will be delayed to mid-october when clubs recieve SAC funding.

### 19th of November, 2025 update:
A domain and hosting provider will be secured by the end of the week.
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
