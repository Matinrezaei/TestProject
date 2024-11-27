from .models import Account

class PhoneAuthBackend:
    def authenticate(self, request, phone_number=None, password=None):
        try:
            user = Account.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
            return None
        except Account.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
