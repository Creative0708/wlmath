import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wlmath.settings')
from random import randint, choice
from datetime import datetime, timedelta
now = datetime.now()

NUM_USERS = 50
NUM_PROBLEMS = 100

print(f"warning: this script is for testing. it will create {NUM_USERS} users and {NUM_PROBLEMS} problems.")
if input("confirm? ").lower() not in ("y", "yes", "actually no please don't"):
	print("aborting.")
	exit(1)

import django
django.setup()
from web.models import WlmathUser, Problem

for user in range(1, NUM_USERS + 1):
	WlmathUser.objects.create(
		username=f"user{user}",
		email=f"testuser{user}@example.localhost"
	)

for problem in range(1, NUM_PROBLEMS + 1):
	n1 = randint(1, 100)
	n2 = randint(1, 100)
	op = choice("+-*")
	answer = eval(f"{n1}{op}{n2}")
	if op == "*": op = r"\cdot"
	problem_text = f"What is ${n1} {op} {n2}$?"
	Problem.objects.create(
		title=f"Problem {problem}",
		body=problem_text,
		answer=answer,
		points=choice((2, 3, 5, 7, 10, 15)),
		slug=f"test{problem}",
		date_added=now - timedelta(days=randint(2, 50)),
		date_modified=now - timedelta(minutes=randint(0, 2 * 60 * 24)),
	)
