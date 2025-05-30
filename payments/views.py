from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.utils import create_response, get_token_from_header, get_user_from_token
from .models import Transaction, WalletBalance
from core.permissions import IsAdminUserType
from .serializers import TransactionSerializer
from rest_framework import status
from decimal import Decimal

from django.utils import timezone


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_txn(request):
    token = get_token_from_header(request)
    user = get_user_from_token(token)
    txn_id = request.data.get('txn_id')
    amount = request.data.get('amount')
    if not amount:
        return Response(
            create_response(
                status=False,
                message="Amount is required",
                data=None
            ),
            status=status.HTTP_400_BAD_REQUEST
        )
    # check if the amount is a valid number
    if not amount.isdigit():
        return Response(
            create_response(
                status=False,
                message="Amount is not a valid number",
                data=None
            ),
            status=status.HTTP_400_BAD_REQUEST
        )
    if not txn_id:
        return Response(
            create_response(
                status=False,
                message="Transaction ID is required",
                data=None
            ),
            status=status.HTTP_400_BAD_REQUEST
        )

    if not user:
        return Response(
            create_response(
                status=False,
                message="User not found",
                data=None
            ),
            status=status.HTTP_400_BAD_REQUEST
        )
    Transaction.objects.create(
        user=user,
        txn_id=txn_id,
        amount=amount
    )

    return Response(
        create_response(
            status=True,
            message="Transaction ID saved successfully",
            data=None
        ),
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pending_txns(request):
    txns = Transaction.objects.filter(status='PENDING')
    serialized_txns = TransactionSerializer(txns, many=True)
    return Response(
        create_response(
            status=True,
            message="Pending transactions retrieved successfully",
            data=serialized_txns.data
        ),
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_completed_txns(request):
    txns = Transaction.objects.filter(status='SUCCESS')
    serialized_txns = TransactionSerializer(txns, many=True)
    return Response(
        create_response(
            status=True,
            message="Successful transactions retrieved successfully",
            data=serialized_txns.data
        ),
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_failed_txns(request):
    txns = Transaction.objects.filter(status='FAILED')
    serialized_txns = TransactionSerializer(txns, many=True)
    return Response(
        create_response(
            status=True,
            message="Failed transactions retrieved successfully",
            data=serialized_txns.data
        ),
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_txns(request):
    token = get_token_from_header(request)
    user = get_user_from_token(token)
    if(user.user_type != 'admin'):
        txns = Transaction.objects.filter(user=user)
    else:
        txns = Transaction.objects.all()
    
    serialized_txns = TransactionSerializer(txns, many=True)
    return Response(
        create_response(
            status=True,
            message="All transactions retrieved successfully",
            data=serialized_txns.data
        ),
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_txn_status_to_success(request):
    txn_id = request.data.get('txn_id')
    amount = request.data.get('amount')
    if not amount:
        return Response(
            create_response(
                status=False,
                message="Amount is required",
                data=None
            ),
            status=status.HTTP_400_BAD_REQUEST
        )
    if not txn_id:
        return Response(
            create_response(
                status=False,
                message="Transaction ID is required",
                data=None
            ),
            status=status.HTTP_400_BAD_REQUEST
        )
    txn = Transaction.objects.get(txn_id=txn_id)
    txn.status = 'SUCCESS'
    txn.amount = amount
    txn.updated_at = timezone.now()
    txn.save()

    # update the wallet balance for the user
    wallet = WalletBalance.objects.get(user=txn.user)
    wallet.balance += Decimal(txn.amount)
    wallet.save()

    return Response(
        create_response(
            status=True,
            message="Transaction status updated successfully",
            data=None
        ),
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_txn_status_to_failed(request):
    txn_id = request.data.get('txn_id')
    amount = request.data.get('amount')
    if not amount:
        return Response(
            create_response(
                status=False,
                message="Amount is required",
                data=None
            ),
            status=status.HTTP_400_BAD_REQUEST
        )
    if not txn_id:
        return Response(
            create_response(
                status=False,
                message="Transaction ID is required",
                data=None
            ),
            status=status.HTTP_400_BAD_REQUEST
        )
    txn = Transaction.objects.get(txn_id=txn_id)
    txn.status = 'FAILED'
    txn.amount = amount
    txn.updated_at = timezone.now()
    txn.save()
    return Response(
        create_response(
            status=True,
            message="Transaction status updated successfully",
            data=None
        ),
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wallet_balance(request):
    token = get_token_from_header(request)
    print("TOKEN: ", token)
    user = get_user_from_token(token)
    print("USER: ", user)
    wallet = WalletBalance.objects.get(user=user)
    print("WALLET: ", wallet.balance)
    return Response(
        create_response(
            status=True,
            message="Wallet balance retrieved successfully",
            data={"balance": wallet.balance}
        ),
        status=status.HTTP_200_OK
    )





