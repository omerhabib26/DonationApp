from .models import User


class CustomAccountAuth(object):

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            user = User.objects.get(username=username)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
