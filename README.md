# wlmath

wlmath (alternatively stylized wlmath) is an online platform for the Mackenzie Math Club to host individual problems, weekly contests, mock contests, video explanations, and more. It will feature leaderboards for various criteria (problems solved, etc) and an admin panel for execs and teachers to add problems to the website.

The only problem is that it doesn't exist yet.

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
python manage.py createsuperuser
python manage.py runserver

# Tailwind setup
npm i
npm run watch

# Run `python manage.py runserver` and `npm run watch` in separate terminal tabs. Enjoy the website!
```
