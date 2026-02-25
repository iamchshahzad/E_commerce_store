from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import DatabaseError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from .models import CustomerLoginActivity, AdminActivity

# Create your views here.

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class CustomerTokenObtainPairSerializer(TokenObtainPairSerializer):
    @staticmethod
    def _get_client_ip(request):
        if not request:
            return None
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user.is_staff or getattr(user, "is_admin", False):
            raise AuthenticationFailed("Use admin login for this account.")
        request = self.context.get("request")
        try:
            CustomerLoginActivity.objects.create(
                user=user,
                ip_address=self._get_client_ip(request),
                user_agent=(request.META.get("HTTP_USER_AGENT", "")[:1000] if request else ""),
            )
        except DatabaseError:
            # Keep auth flow working even if login-audit migration is pending.
            pass
        return data


class CustomerLoginView(TokenObtainPairView):
    serializer_class = CustomerTokenObtainPairSerializer


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_staff": user.is_staff,
                "is_admin": getattr(user, "is_admin", False),
            }
        )


class AdminRecentActionsView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _is_admin(user):
        return bool(user and (user.is_staff or getattr(user, "is_admin", False)))

    def get(self, request):
        if not self._is_admin(request.user):
            return Response({"detail": "Admin access required."}, status=403)

        try:
            actions = AdminActivity.objects.filter(user_id=request.user.id).order_by("-action_time")[:20]
        except DatabaseError:
            return Response(
                {"detail": "Admin activity table unavailable. Run migrations first."},
                status=503,
            )
        payload = []
        for action in actions:
            payload.append(
                {
                    "id": action.id,
                    "action_time": action.action_time,
                    "object_repr": action.object_repr,
                    "change_message": action.change_message or "No details",
                    "action_flag": action.action,
                    "app_label": action.app_label,
                    "model": action.model,
                }
            )
        return Response(payload)


class AdminClearRecentActionsView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _is_admin(user):
        return bool(user and (user.is_staff or getattr(user, "is_admin", False)))

    def post(self, request):
        if not self._is_admin(request.user):
            return Response({"detail": "Admin access required."}, status=403)

        try:
            deleted_count, _ = AdminActivity.objects.filter(user_id=request.user.id).delete()
        except DatabaseError:
            return Response(
                {"detail": "Admin activity table unavailable. Run migrations first."},
                status=503,
            )
        return Response({"cleared": deleted_count})
