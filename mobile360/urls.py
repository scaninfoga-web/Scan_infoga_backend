from django.urls import path
from . import views

app_name = 'mobile360'

urlpatterns = [
    path('getMobile360Dtls', views.mobile_360_search, name='mobile_360_search'),
    path('getuanhistory', views.uan_history_search, name='uan_history_search'),
    path('uanemploymentHistory', views.uan_employment_history_search, name='uan_employment_history_search'),
    path('gstadvancev2', views.gst_advance_v2, name='gst_advance_v2'),
    path('esicdtls', views.esic_details_search, name='esic_details_search'),
    path('gstturnover', views.gst_turnover, name='gst_turnover'),
    path('verifyudyam', views.udyam_details_search, name='udyam_details_search'),
    path('mobiletoaccount', views.mobile_to_account_search, name='mobile_to_account_search'),
    path('profileadvance', views.profile_advance_search, name='profile_advance_search'),
    path('equifaxv3', views.equifax_report_search, name='equifax_report_search'),
]