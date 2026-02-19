from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST


@staff_member_required
@require_POST
def clear_recent_actions(request):
    deleted_count, _ = LogEntry.objects.filter(user_id=request.user.id).delete()
    messages.success(request, f"Cleared {deleted_count} recent action(s).")
    return redirect("admin:index")
