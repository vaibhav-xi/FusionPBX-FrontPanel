from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class ImpersonateUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if request.user.is_superuser and 'impersonate_user_id' in request.session:
            impersonate_user_id = request.session.pop('impersonate_user_id')
            try:
                user = User.objects.get(id=impersonate_user_id)
                return user
            except User.DoesNotExist:
                pass
        return None