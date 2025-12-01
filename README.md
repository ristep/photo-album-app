# Django Photo Album Backend (SQLite + Filesystem)

This repository provides a simple Django + DRF backend configured to use SQLite for metadata and the container's filesystem for media. It is intended for local development and small family deployments.

## Quick start

1. Copy `.env.example` to `.env` and edit values if needed.
2. Build and run:

```bash
docker compose up --build
```

3. Create a superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

4. Visit:
- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/

Media files will be stored in `./data/media` on your host, and the SQLite file at `./data/db/db.sqlite3`.

## Notes
- For production you should use a proper webserver (host nginx) and consider PostgreSQL or MySQL if you need concurrency or advanced features.


# Django Photo Backend — Quick Test Guide

This README shows quick commands to run the backend locally (Docker Compose) and to test the Django REST Framework API using JWT tokens.

Base URL: `http://localhost:8000/api/`

Prerequisites
- Docker and Docker Compose installed
- Repository already built with project files

Start the server
```bash
docker compose up -d
```

Check the API root (browsable API)
```bash
curl -i http://localhost:8000/api/
# Or open in a browser: http://localhost:8000/api/
```

Create or set a test user password (if needed)
```bash
docker compose exec -T web python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); u=User.objects.filter(username='ristepan').first(); u.set_password('secretpass'); u.save(); print('Password set for', u.username)"
```

Obtain JWT tokens (access + refresh)
```bash
curl -s -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"ristepan","password":"secretpass"}' | python -m json.tool
```

Use the access token to call protected endpoints
```bash
# Paste the access token into ACCESS
ACCESS=<paste_access_token_here>
curl -H "Authorization: Bearer $ACCESS" http://localhost:8000/api/media/ | python -m json.tool
```

Create an album (authenticated)
```bash
curl -X POST http://localhost:8000/api/albums/ \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Album","description":"Test album","is_public":false}' | python -m json.tool
```

Upload a media file (multipart)
```bash
curl -X POST http://localhost:8000/api/media/ \
  -H "Authorization: Bearer $ACCESS" \
  -F "file=@/full/path/to/photo.jpg" \
  -F "media_type=photo"
```

Refresh the access token
```bash
REFRESH=<paste_refresh_token_here>
curl -s -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d "{\"refresh\":\"$REFRESH\"}" | python -m json.tool
```

If anonymous requests return `[]` for `GET /api/media/`:
- The API is configured to return only the authenticated user's media. Authenticate (Bearer token) to see your items.
- If you want public media visible anonymously, we can add an `is_public` flag or expose media via public albums.

Admin and browsable UI
- Admin: `http://localhost:8000/admin/` (inspect users, albums, media)
- Browsable API: open `http://localhost:8000/api/` in your browser and use the login link or supply the Authorization header in your REST client.

Rebuild (after changing requirements/settings)
```bash
docker compose down
docker compose up -d --build
```

Troubleshooting
- If changes to Python requirements aren't reflected inside the container, rebuild the image.
- To inspect the DB from shell:
```bash
docker compose exec -T web python manage.py shell -c "from apps.albums.models import MediaFile; print(MediaFile.objects.count()); print(list(MediaFile.objects.values()[:5]))"
```

Want extras?
- I can add a Postman/Insomnia collection, a README section for production settings, or an endpoint for public media. Tell me which.

