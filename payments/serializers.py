from rest_framework import serializers
from .models import Transaction, WalletBalance

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        # fields = '__all__'
        fields = ['txn_id', 'amount', 'status', 'created_at', 'comment', 'created_at']
        
class WalletBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletBalance
        fields = '__all__'