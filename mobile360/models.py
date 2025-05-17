from django.db import models

class Mobile360(models.Model):
    mobile_number = models.CharField(max_length=15, primary_key=True)
    txn_id = models.UUIDField(unique=True)
    api_category = models.CharField(max_length=50)
    api_name = models.CharField(max_length=50)
    billable = models.BooleanField(default=True)
    message = models.CharField(max_length=255)
    status = models.IntegerField()
    datetime = models.DateTimeField()

    class Meta:
        db_table = 'mobile360'

class DigitalPaymentInfo(models.Model):
    mobile_response = models.OneToOneField(Mobile360, on_delete=models.CASCADE, related_name='digital_payment_info')
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255, null=True)
    bank = models.CharField(max_length=255, null=True)
    branch = models.CharField(max_length=255, null=True)
    center = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'digital_payment_info'

class LPGInfo(models.Model):
    mobile_response = models.ForeignKey(Mobile360, on_delete=models.CASCADE, related_name='lpg_info')
    code = models.CharField(max_length=10)
    gas_provider = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    consumer_mobile = models.CharField(max_length=15)
    consumer_id = models.CharField(max_length=50)
    consumer_status = models.CharField(max_length=50)
    consumer_type = models.CharField(max_length=100)
    address = models.TextField()
    distributor_code = models.CharField(max_length=50)
    distributor_name = models.CharField(max_length=255)
    distributor_contact = models.CharField(max_length=50)
    distributor_address = models.TextField()

    class Meta:
        db_table = 'lpg_info'

class TelcoInfo(models.Model):
    mobile_response = models.OneToOneField(Mobile360, on_delete=models.CASCADE, related_name='telco_info')
    code = models.CharField(max_length=10)
    is_valid = models.BooleanField(default=False)
    subscriber_status = models.CharField(max_length=50)
    connection_type = models.CharField(max_length=50)
    msisdn = models.CharField(max_length=20)
    msisdn_country_code = models.CharField(max_length=5)
    network_name = models.CharField(max_length=100)
    network_region = models.CharField(max_length=100)
    is_roaming = models.BooleanField(default=False)

    class Meta:
        db_table = 'telco_info'

class MobileAgeInfo(models.Model):
    mobile_response = models.OneToOneField(Mobile360, on_delete=models.CASCADE, related_name='mobile_age_info')
    code = models.CharField(max_length=10)
    is_ported = models.CharField(max_length=5)
    mobile_age = models.CharField(max_length=50)
    number_active = models.CharField(max_length=5)
    number_valid = models.CharField(max_length=5)
    ported_region = models.CharField(max_length=100, blank=True)
    ported_telecom = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100)
    roaming = models.CharField(max_length=5)
    telecom = models.CharField(max_length=100)

    class Meta:
        db_table = 'mobile_age_info'

class WhatsappInfo(models.Model):
    mobile_response = models.OneToOneField(Mobile360, on_delete=models.CASCADE, related_name='whatsapp_info')
    code = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    is_business = models.CharField(max_length=5)

    class Meta:
        db_table = 'whatsapp_info'

class RevokeInfo(models.Model):
    mobile_response = models.OneToOneField(Mobile360, on_delete=models.CASCADE, related_name='revoke_info')
    code = models.CharField(max_length=10)
    revoke_date = models.CharField(max_length=50, blank=True)
    revoke_status = models.CharField(max_length=5)

    class Meta:
        db_table = 'revoke_info'

class KeyHighlights(models.Model):
    mobile_response = models.OneToOneField(Mobile360, on_delete=models.CASCADE, related_name='key_highlights')
    digital_payment_id_name = models.CharField(max_length=255)
    gas_connection_found = models.CharField(max_length=5)
    connection_type = models.CharField(max_length=50)
    whatsapp_business_account_status = models.CharField(max_length=50)
    age_of_mobile = models.CharField(max_length=50)
    active_status = models.CharField(max_length=5)
    revoke_date = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'key_highlights'

############################# UAN HISTORY LATEST V2 ###########################

class UanHistoryLatestV2(models.Model):
    uan = models.CharField(max_length=12, primary_key=True)
    txn_id = models.UUIDField(unique=True)
    api_category = models.CharField(max_length=50)
    api_name = models.CharField(max_length=50)
    billable = models.BooleanField(default=True)
    message = models.CharField(max_length=255)
    status = models.IntegerField()
    datetime = models.DateTimeField()
    
    # Result fields
    name = models.CharField(max_length=255)
    dob = models.DateField()
    guardian_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    member_id = models.CharField(max_length=50)
    date_of_joining = models.DateField()
    last_pf_submitted = models.DateField()

    class Meta:
        db_table = 'uan_history_latest_v2'

############## UAN History ##############
class UanEmploymentHistory(models.Model):
    # Basic info from result
    name = models.CharField(max_length=255)
    dob = models.CharField(max_length=10)  # Store as string to maintain dd/mm/yyyy format
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'uan_employment_history'

class CompanyHistory(models.Model):
    uan_history = models.ForeignKey(UanEmploymentHistory, on_delete=models.CASCADE, related_name='employment_history')
    company_name = models.CharField(max_length=255)
    company_address = models.TextField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company_history'

################### MOBILE TO ESIC DETAILS
class EsicDtls(models.Model):
    esic_number = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    employer_code = models.CharField(max_length=50)
    employer_name = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=15)
    uan_number = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    branch_name = models.CharField(max_length=100, blank=True)
    bank_account_status = models.CharField(max_length=20)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'esic_dtls'

################### GST VERIFICATION ###################
class GstVerification(models.Model):
    gstin = models.CharField(max_length=15, primary_key=True)
    
    # Result fields
    aggregate_turn_over = models.CharField(max_length=50, blank=True)
    business_constitution = models.CharField(max_length=100)
    can_flag = models.CharField(max_length=50, blank=True)
    central_jurisdiction = models.TextField()
    compliance_rating = models.CharField(max_length=50, blank=True)
    current_registration_status = models.CharField(max_length=50)
    is_field_visit_conducted = models.CharField(max_length=5)
    legal_name = models.CharField(max_length=255)
    mandate_e_invoice = models.CharField(max_length=50, blank=True)
    register_cancellation_date = models.CharField(max_length=20, blank=True)
    register_date = models.CharField(max_length=20)
    state_jurisdiction = models.TextField()
    tax_payer_type = models.CharField(max_length=50)
    trade_name = models.CharField(max_length=255)
    gross_total_income = models.CharField(max_length=50, blank=True)
    gross_total_income_financial_year = models.CharField(max_length=20, blank=True)
    business_email = models.CharField(max_length=100, blank=True)
    business_mobile = models.CharField(max_length=20, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gst_verification'

class GstAuthorizedSignatory(models.Model):
    gst_verification = models.ForeignKey(GstVerification, on_delete=models.CASCADE, related_name='authorized_signatories')
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'gst_authorized_signatory'

class GstBusinessNature(models.Model):
    gst_verification = models.ForeignKey(GstVerification, on_delete=models.CASCADE, related_name='business_natures')
    nature = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'gst_business_nature'

class GstBusinessDetail(models.Model):
    gst_verification = models.ForeignKey(GstVerification, on_delete=models.CASCADE, related_name='business_details')
    saccd = models.CharField(max_length=20)
    sdes = models.TextField()
    
    class Meta:
        db_table = 'gst_business_detail'

class GstFilingStatus(models.Model):
    gst_verification = models.ForeignKey(GstVerification, on_delete=models.CASCADE, related_name='filing_statuses')
    fy = models.CharField(max_length=10)
    taxp = models.CharField(max_length=20)
    mof = models.CharField(max_length=20)
    dof = models.CharField(max_length=20)
    rtntype = models.CharField(max_length=10)
    arn = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'gst_filing_status'

class GstBusinessAddress(models.Model):
    gst_verification = models.OneToOneField(GstVerification, on_delete=models.CASCADE, related_name='primary_address')
    business_nature = models.TextField()
    detailed_address = models.TextField(blank=True)
    last_updated_date = models.CharField(max_length=20, blank=True)
    registered_address = models.TextField()
    
    class Meta:
        db_table = 'gst_business_address'
        
################### GST Turnover ###################
class GstTurnover(models.Model):
    txn_id = models.CharField(max_length=50, primary_key=True)
    gstin = models.CharField(max_length=15)  # <-- Add this line
    gst_estimated_total = models.FloatField(null=True)
    gst_filed_total = models.FloatField()
    year = models.CharField(max_length=10)
    filing_date = models.CharField(max_length=20)
    pan_estimated_total = models.FloatField()
    pan_filed_total = models.FloatField()
    gst_status = models.CharField(max_length=50)
    legal_name = models.CharField(max_length=255)
    trade_name = models.CharField(max_length=255)
    register_date = models.CharField(max_length=20)
    tax_payer_type = models.CharField(max_length=50)
    datetime = models.DateTimeField()

    # Optional fields for compatibility or display
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    turnover = models.FloatField(null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'gst_turnover'

class GstTurnoverAuthorizedSignatory(models.Model):
    gst_turnover = models.ForeignKey(GstTurnover, on_delete=models.CASCADE, related_name='authorized_signatories')
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'gst_turnover_authorized_signatory'

class GstTurnoverBusinessNature(models.Model):
    gst_turnover = models.ForeignKey(GstTurnover, on_delete=models.CASCADE, related_name='business_natures')
    nature = models.CharField(max_length=100)

    class Meta:
        db_table = 'gst_turnover_business_nature'
        
################### Verify Udyam ###################
class UdyamDetails(models.Model):
    udyamnumber = models.CharField(max_length=50, db_column='registration_no')
    txn_id = models.CharField(max_length=100)
    api_category = models.CharField(max_length=100)
    api_name = models.CharField(max_length=100)
    billable = models.BooleanField()
    message = models.CharField(max_length=255)
    status = models.IntegerField()
    datetime = models.DateTimeField()

    enterprise_name = models.CharField(max_length=255)
    organisation_type = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    social_category = models.CharField(max_length=50)
    date_of_incorporation = models.DateField()
    date_of_commencement = models.DateField()
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    dic = models.CharField(max_length=100)
    msme_dfo = models.CharField(max_length=100)
    date_of_udyam_registeration = models.DateField()

    class Meta:
        db_table = 'udyam_details'

class UdyamAddress(models.Model):
    udyam = models.OneToOneField(UdyamDetails, on_delete=models.CASCADE, related_name='address')
    flat_no = models.CharField(max_length=100)
    building = models.CharField(max_length=255)
    village = models.CharField(max_length=100)
    block = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)

class UdyamPlantDetail(models.Model):
    udyam = models.ForeignKey(UdyamDetails, on_delete=models.CASCADE, related_name='plant_details')
    unit_name = models.CharField(max_length=255)
    flat = models.CharField(max_length=100)
    building = models.CharField(max_length=255)
    village = models.CharField(max_length=100)
    block = models.CharField(max_length=100)
    road = models.CharField(max_length=255)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)

class UdyamEnterpriseType(models.Model):
    udyam = models.ForeignKey(UdyamDetails, on_delete=models.CASCADE, related_name='enterprise_type')
    classification_year = models.CharField(max_length=20)
    enterprise_type = models.CharField(max_length=50)
    classification_date = models.DateField()

class UdyamNICCode(models.Model):
    udyam = models.ForeignKey(UdyamDetails, on_delete=models.CASCADE, related_name='nic_code')
    nic_2_digit = models.CharField(max_length=100)
    nic_4_digit = models.CharField(max_length=100)
    nic_5_digit = models.CharField(max_length=100)
    activity = models.CharField(max_length=50)
    date = models.DateField()

################### Mobile to Account ###################
class MobileToAccountDetails(models.Model):
    txn_id = models.CharField(max_length=100, unique=True)
    api_category = models.CharField(max_length=100)
    api_name = models.CharField(max_length=100)
    billable = models.BooleanField()
    message = models.CharField(max_length=255)
    status = models.IntegerField()
    datetime = models.DateTimeField()
    mobile = models.CharField(max_length=15)  # Input mobile number

    class Meta:
        db_table = 'mobile_to_account_details'

class AccountDetails(models.Model):
    record = models.OneToOneField(MobileToAccountDetails, on_delete=models.CASCADE, related_name='account_details')
    account_ifsc = models.CharField(max_length=20)
    account_number = models.CharField(max_length=30)
    amount_deposited = models.DecimalField(max_digits=10, decimal_places=2)

class VpaDetails(models.Model):
    record = models.OneToOneField(MobileToAccountDetails, on_delete=models.CASCADE, related_name='vpa_details')
    account_holder_name = models.CharField(max_length=100)
    vpa = models.CharField(max_length=100)
    
