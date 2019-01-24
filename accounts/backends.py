from .models import Financer


class FinancerAuth(object):

    def authenticate(self, request, email=None, password=None):
        try:
            user = Financer.objects.get(email=email)
            if user.check_password(password):
                return user
        except Financer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = Financer.objects.get(email=user_id)
            if user.is_active:
                return user
            return None
        except Financer.DoesNotExist:
            return None
