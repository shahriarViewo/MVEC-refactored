from rest_framework import serializers
from .models import VendorWallet, VendorTransaction, VendorPayout

# -----------------------------
# Transaction Serializer
# -----------------------------
class VendorTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorTransaction
        fields = ['id', 'amount', 'transaction_type', 'description', 'created_at']


# -----------------------------
# Payout Serializer
# -----------------------------
class VendorPayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPayout
        fields = ['id', 'amount', 'status', 'payout_date', 'admin_note', 'created_at']
        read_only_fields = ['status', 'payout_date', 'admin_note', 'created_at']

    def validate_amount(self, value):
        # Business logic: Ensure vendor has enough balance
        # (Assuming context has the wallet or user)
        # detailed validation usually happens in the View or Service layer
        if value <= 0:
            raise serializers.ValidationError("Payout amount must be positive.")
        return value


# -----------------------------
# Wallet Serializer
# -----------------------------
class VendorWalletSerializer(serializers.ModelSerializer):
    # Nested history is often too large, so we usually don't include transactions here
    # by default, but we can include the last few or a summary.
    
    class Meta:
        model = VendorWallet
        fields = ['id', 'balance', 'updated_at']
        read_only_fields = ['balance', 'updated_at'] # Balance is updated only via backend logic