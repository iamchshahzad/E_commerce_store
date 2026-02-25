from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect


def react_app(request):
    index_path = settings.FRONTEND_DIST_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path.open("rb"))
    if settings.DEBUG:
        return redirect(f"{settings.REACT_DEV_SERVER_URL}{request.get_full_path()}")
    return HttpResponse(
        "React build not found. Run: cd frontend && npm install && npm run build",
        status=503,
    )
