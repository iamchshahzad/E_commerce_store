# E_commerce_store

Django backend + React frontend.

## Run Backend (Django)

```bash
python manage.py runserver
```

## Run Frontend (React - dev mode)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://127.0.0.1:5173` and proxies `/api` + `/media` to Django at `http://127.0.0.1:8000`.

## Attach React to Django (single backend-served app)

```bash
cd frontend
npm install
npm run build
cd ..
python manage.py runserver
```

After build, Django serves the React app on `/` and frontend routes.
