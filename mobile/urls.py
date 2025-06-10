# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('getMobile360Dtls', views.mobile_360_search, name='mobile_360_search'),
    path('getAcDtlsFromMobNo', views.get_acc_dtls_from_mobile, name='get_acc_dtls_from_mobile'),
    path("getuanhistory", views.uan_history_search, name="uan_history_search"),#
    path("employmentsearch", views.uan_employment_search, name="uan_employment_search"),#
    path("esicsearch", views.esic_search, name="esic-search"),
    path("gstadvance", views.gst_verification_search, name="gst-verification-search"),
    path("gstturnover", views.gst_turnover_search, name="gst-turnover-search"),
    path("verifyudyam", views.udyam_verification_search, name="udyam_verification_search"),
    path("profileadvance", views.profile_advance_search, name="profile_advance_search"),
    path("equifaxv3", views.equifax_v3_search, name="equifax_v3_search"),#
    path("uanpassbookwithoutotp", views.uan_passbook_without_otp, name="uan_passbook_without_otp"),
    path("mobiletodllookup", views.mobile_to_dl_lookup, name="mobile_to_dl_lookup"),
    path("panallinone", views.pan_all_in_one, name="pan_all_in_one"),
    path("digitalpayment", views.digital_payment_analyser, name="digital_payment_analyser"),
    path("breachinfo", views.leak_osint, name="leakosint"),
    path("hunterfind", views.hunter_find, name="hunterfind"),
    path("hunterverify", views.hunter_verify, name="hunterverify"),
]
