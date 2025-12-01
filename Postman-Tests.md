# Postman Collection — Example Tests

This file contains an example Postman collection (v2.1) you can import into Postman or other compatible REST clients (Insomnia, Hoppscotch). It includes requests and small test scripts to obtain JWT tokens, refresh them, and call protected and public endpoints for the Django Photo backend running at:

Base URL: `http://localhost:8000/api/`

How to use
- Save the JSON below as `postman_collection_photo_app.json` or copy it directly into Postman (Import → Raw Text).
- Run `POST /token/` with your username/password to populate the collection variables `access_token` and `refresh_token` automatically.
- Use the other requests (they use `{{access_token}}`) to call the API.

Postman collection JSON (v2.1)

```json
{
  "info": {
    "name": "Django Photo Backend (Example)",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "_postman_id": "photo-app-example"
  },
  "item": [
    {
      "name": "Obtain Token",
      "request": {
        "method": "POST",
        "header": [
          { "key": "Content-Type", "value": "application/json" }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"username\": \"ristepan\", \"password\": \"secretpass\"}"
        },
        "url": { "raw": "http://localhost:8000/api/token/", "protocol": "http", "host": ["localhost"], "port": "8000", "path": ["api","token"] }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "const json = pm.response.json();",
              "if (json.access) pm.collectionVariables.set('access_token', json.access);",
              "if (json.refresh) pm.collectionVariables.set('refresh_token', json.refresh);",
              "pm.test('Got access token', () => pm.expect(json).to.have.property('access'))"
            ]
          }
        }
      ]
    },
    {
      "name": "Refresh Token",
      "request": {
        "method": "POST",
        "header": [ { "key": "Content-Type", "value": "application/json" } ],
        "body": { "mode": "raw", "raw": "{\"refresh\": \"{{refresh_token}}\"}" },
        "url": { "raw": "http://localhost:8000/api/token/refresh/", "protocol": "http", "host": ["localhost"], "port": "8000", "path": ["api","token","refresh"] }
      },
      "event": [
        {
          "listen": "test",
          "script": { "exec": [ "const json = pm.response.json(); if (json.access) pm.collectionVariables.set('access_token', json.access); pm.test('Refreshed access token', () => pm.expect(json).to.have.property('access'))" ] }
        }
      ]
    },
    {
      "name": "List My Media (authenticated)",
      "request": {
        "method": "GET",
        "header": [ { "key": "Authorization", "value": "Bearer {{access_token}}" } ],
        "url": { "raw": "http://localhost:8000/api/media/", "protocol": "http", "host": ["localhost"], "port": "8000", "path": ["api","media"] }
      }
    },
    {
      "name": "List Public Media (anonymous)",
      "request": {
        "method": "GET",
        "url": { "raw": "http://localhost:8000/api/media/public/", "protocol": "http", "host": ["localhost"], "port": "8000", "path": ["api","media","public"] }
      }
    },
    {
      "name": "Create Album (authenticated)",
      "request": {
        "method": "POST",
        "header": [ { "key": "Content-Type", "value": "application/json" }, { "key": "Authorization", "value": "Bearer {{access_token}}" } ],
        "body": { "mode": "raw", "raw": "{\"title\": \"My Album\", \"description\": \"Created from Postman\", \"is_public\": false }" },
        "url": { "raw": "http://localhost:8000/api/albums/", "protocol": "http", "host": ["localhost"], "port": "8000", "path": ["api","albums"] }
      }
    },
    {
      "name": "Upload Media (authenticated, multipart)",
      "request": {
        "method": "POST",
        "header": [ { "key": "Authorization", "value": "Bearer {{access_token}}" } ],
        "body": {
          "mode": "formdata",
          "formdata": [
            { "key": "file", "type": "file", "src": "<path-to-your-file>" },
            { "key": "media_type", "value": "photo", "type": "text" }
          ]
        },
        "url": { "raw": "http://localhost:8000/api/media/", "protocol": "http", "host": ["localhost"], "port": "8000", "path": ["api","media"] }
      }
    }
  ]
}
```

Notes
- Replace `<path-to-your-file>` in the Upload Media request with an actual file path on your machine when importing.
- The collection uses `collectionVariables` to store `access_token` and `refresh_token` automatically after the Obtain Token request runs.

If you want me to add the raw JSON as a separate `.json` file for direct import, I can add it to the repo (e.g. `postman_collection_photo_app.json`).
