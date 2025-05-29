from django.urls import path
from . import views

urlpatterns = [
    path("postTxn", views.post_txn, name="post_txn"),
    path("getPendingTxns", views.get_pending_txns, name="get_pending_txn"),
    path("getCompletedTxns", views.get_completed_txns, name="get_completed_txn"),
    path("getFailedTxns", views.get_failed_txns, name="get_failed_txn"),
    path("getAllTxns", views.get_all_txns, name="get_all_txn"),
    path("updateTxnToSuccess", views.update_txn_status_to_success, name="update_txn_to_success"),
    path("updateTxnToFailed", views.update_txn_status_to_failed, name="update_txn_to_failed"),
    path("getWalletBalance", views.get_wallet_balance, name="get_wallet_balance"),
]