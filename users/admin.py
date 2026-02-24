from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import CustomerLoginActivity, AdminActivity


@admin.register(CustomerLoginActivity)
class CustomerLoginActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "ip_address", "logged_in_at")
    search_fields = ("user__username", "ip_address")
    list_filter = ("logged_in_at",)
    readonly_fields = ("user", "ip_address", "user_agent", "logged_in_at")


@admin.register(AdminActivity)
class AdminActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "object_repr", "action_time")
    search_fields = ("user__username", "object_repr", "change_message")
    list_filter = ("action", "action_time")
    readonly_fields = ("user", "action", "object_repr", "change_message", "app_label", "model", "action_time")


@staff_member_required
@require_POST
def clear_recent_actions(request):
    deleted_count, _ = LogEntry.objects.filter(user_id=request.user.id).delete()
    messages.success(request, f"Cleared {deleted_count} recent action(s).")
    return redirect("admin:index")
