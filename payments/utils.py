from .models import WalletBalance

def create_wallet(user):
    return WalletBalance.objects.create(user=user)
    