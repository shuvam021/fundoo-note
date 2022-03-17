py=python manage.py

run:
	$(py) runserver

migrate:
	$(py) makemigrations
	$(py) migrate

test:
	$(py) test

mail_debug:
	python -m smtpd -n -c DebuggingServer localhost:1025

celery_worker:
	celery -A config worker -l info