# run migrate
docker compose exec web python manage.py migrate

# create superuser (interactive)
docker compose exec web python manage.py createsuperuser

# open Django shell
docker compose exec web python manage.py shell

# collect static files
docker compose exec web python manage.py collectstatic --noinput