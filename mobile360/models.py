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
    
################### Profile Advance ###################
class ProfileAdvanceLookup(models.Model):
    """Main model to store the API response for Profile Advance lookup"""
    txn_id = models.CharField(max_length=100, unique=True)
    api_category = models.CharField(max_length=100)
    api_name = models.CharField(max_length=100)
    billable = models.BooleanField()
    message = models.CharField(max_length=255)
    status = models.IntegerField()
    datetime = models.DateTimeField()
    mobile = models.CharField(max_length=15)  # Input mobile number - add this field to store the queried mobile

    class Meta:
        db_table = 'profile_advance_lookup'

class PersonalInformation(models.Model):
    """Model to store personal information from the API response"""
    profile = models.OneToOneField(ProfileAdvanceLookup, on_delete=models.CASCADE, related_name='personal_information')
    full_name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    age = models.CharField(max_length=5, blank=True)  # Using CharField since age comes as string in the API
    date_of_birth = models.DateField(null=True, blank=True)
    income = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'profile_personal_information'

class AlternatePhone(models.Model):
    """Model to store alternate phone numbers"""
    profile = models.ForeignKey(ProfileAdvanceLookup, on_delete=models.CASCADE, related_name='alternate_phones')
    serial_number = models.CharField(max_length=10)
    value = models.CharField(max_length=15)

    class Meta:
        db_table = 'profile_alternate_phones'

class Email(models.Model):
    """Model to store email addresses"""
    profile = models.ForeignKey(ProfileAdvanceLookup, on_delete=models.CASCADE, related_name='emails')
    serial_number = models.CharField(max_length=10)
    value = models.EmailField()

    class Meta:
        db_table = 'profile_emails'

class Address(models.Model):
    """Model to store addresses"""
    profile = models.ForeignKey(ProfileAdvanceLookup, on_delete=models.CASCADE, related_name='addresses')
    detailed_address = models.TextField(blank=True)
    state = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    type = models.CharField(max_length=100, blank=True)
    date_of_reporting = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'profile_addresses'

class DocumentData(models.Model):
    """Parent model for document data"""
    profile = models.OneToOneField(ProfileAdvanceLookup, on_delete=models.CASCADE, related_name='document_data')

    class Meta:
        db_table = 'profile_document_data'

class PanDocument(models.Model):
    """Model to store PAN card details"""
    document_data = models.ForeignKey(DocumentData, on_delete=models.CASCADE, related_name='pan_documents')
    serial_number = models.CharField(max_length=10)
    value = models.CharField(max_length=10)  # PAN is typically 10 characters

    class Meta:
        db_table = 'profile_pan_documents'

################### Equifax V3 ###################
class EquifaxReport(models.Model):
    """Main model to store the API response for Equifax V3 lookup"""
    txn_id = models.CharField(max_length=100, unique=True)
    api_category = models.CharField(max_length=100)
    api_name = models.CharField(max_length=100)
    billable = models.BooleanField()
    message = models.CharField(max_length=255)
    status = models.IntegerField()
    datetime = models.DateTimeField()
    # Input identifiers
    id_number = models.CharField(max_length=20)
    id_type = models.CharField(max_length=20)
    mobile = models.CharField(max_length=15)
    
    class Meta:
        db_table = 'equifax_report'

class BasicCreditInfo(models.Model):
    """Model to store basic credit information from the API response"""
    report = models.OneToOneField(EquifaxReport, on_delete=models.CASCADE, related_name='basic_credit_info')
    name = models.CharField(max_length=255, blank=True)
    credit_score = models.CharField(max_length=10, blank=True)
    
    class Meta:
        db_table = 'equifax_basic_credit_info'

class InquiryResponseHeader(models.Model):
    """Model to store response header data"""
    report = models.OneToOneField(EquifaxReport, on_delete=models.CASCADE, related_name='inquiry_response_header')
    client_id = models.CharField(max_length=50, blank=True)
    cust_ref_field = models.CharField(max_length=50, blank=True)
    report_order_no = models.CharField(max_length=50, blank=True)
    success_code = models.CharField(max_length=10, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.CharField(max_length=10, blank=True)
    
    class Meta:
        db_table = 'equifax_inquiry_response_header'

class ProductCode(models.Model):
    """Model to store product codes"""
    response_header = models.ForeignKey(InquiryResponseHeader, on_delete=models.CASCADE, related_name='product_codes')
    value = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'equifax_product_code'

class InquiryRequestInfo(models.Model):
    """Model to store inquiry request information"""
    report = models.OneToOneField(EquifaxReport, on_delete=models.CASCADE, related_name='inquiry_request_info')
    inquiry_purpose = models.CharField(max_length=50, blank=True)
    transaction_amount = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'equifax_inquiry_request_info'

class InquiryPhone(models.Model):
    """Model to store inquiry phones"""
    request_info = models.ForeignKey(InquiryRequestInfo, on_delete=models.CASCADE, related_name='inquiry_phones')
    seq = models.CharField(max_length=10)
    number = models.CharField(max_length=15)
    
    class Meta:
        db_table = 'equifax_inquiry_phone'

class PhoneType(models.Model):
    """Model to store phone types"""
    inquiry_phone = models.ForeignKey(InquiryPhone, on_delete=models.CASCADE, related_name='phone_types')
    value = models.CharField(max_length=5)
    
    class Meta:
        db_table = 'equifax_phone_type'

class IDDetail(models.Model):
    """Model to store ID details"""
    request_info = models.ForeignKey(InquiryRequestInfo, on_delete=models.CASCADE, related_name='id_details')
    seq = models.CharField(max_length=10)
    id_type = models.CharField(max_length=10)
    source = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'equifax_id_detail'

class Score(models.Model):
    """Model to store score information"""
    report = models.ForeignKey(EquifaxReport, on_delete=models.CASCADE, related_name='scores')
    type = models.CharField(max_length=20)
    version = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'equifax_score'

class CreditReport(models.Model):
    """Model to store the entire credit report section"""
    report = models.OneToOneField(EquifaxReport, on_delete=models.CASCADE, related_name='credit_report')
    
    class Meta:
        db_table = 'equifax_credit_report'

class CIRReportData(models.Model):
    """Model to store CIR report data"""
    credit_report = models.ForeignKey(CreditReport, on_delete=models.CASCADE, related_name='cir_report_data_list')
    
    class Meta:
        db_table = 'equifax_cir_report_data'

class EnquirySummary(models.Model):
    """Model to store enquiry summary"""
    cir_report_data = models.OneToOneField(CIRReportData, on_delete=models.CASCADE, related_name='enquiry_summary')
    past_12_months = models.CharField(max_length=10, blank=True)
    past_24_months = models.CharField(max_length=10, blank=True)
    past_30_days = models.CharField(max_length=10, blank=True)
    purpose = models.CharField(max_length=20, blank=True)
    recent = models.CharField(max_length=20, blank=True)
    total = models.CharField(max_length=10, blank=True)
    
    class Meta:
        db_table = 'equifax_enquiry_summary'

class Enquiry(models.Model):
    """Model to store individual enquiries"""
    cir_report_data = models.ForeignKey(CIRReportData, on_delete=models.CASCADE, related_name='enquiries')
    amount = models.CharField(max_length=20, blank=True)
    date = models.DateField(null=True, blank=True)
    institution = models.CharField(max_length=255, blank=True)
    request_purpose = models.CharField(max_length=20, blank=True)
    time = models.CharField(max_length=10, blank=True)
    seq = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'equifax_enquiry'

class IDAndContactInfo(models.Model):
    """Model to store ID and contact information"""
    cir_report_data = models.OneToOneField(CIRReportData, on_delete=models.CASCADE, related_name='id_and_contact_info')
    
    class Meta:
        db_table = 'equifax_id_and_contact_info'

class AddressInfo(models.Model):
    """Model to store address information"""
    id_and_contact_info = models.ForeignKey(IDAndContactInfo, on_delete=models.CASCADE, related_name='address_info')
    address = models.TextField(blank=True)
    postal = models.CharField(max_length=10, blank=True)
    reported_date = models.DateField(null=True, blank=True)
    seq = models.CharField(max_length=10)
    state = models.CharField(max_length=10, blank=True)
    type = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'equifax_address_info'

class EmailAddressInfo(models.Model):
    """Model to store email address information"""
    id_and_contact_info = models.ForeignKey(IDAndContactInfo, on_delete=models.CASCADE, related_name='email_address_info')
    email_address = models.EmailField(blank=True)
    reported_date = models.DateField(null=True, blank=True)
    seq = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'equifax_email_address_info'

class IdentityInfo(models.Model):
    """Model to store identity information"""
    id_and_contact_info = models.OneToOneField(IDAndContactInfo, on_delete=models.CASCADE, related_name='identity_info')
    
    class Meta:
        db_table = 'equifax_identity_info'

class OtherId(models.Model):
    """Model to store other ID information"""
    identity_info = models.ForeignKey(IdentityInfo, on_delete=models.CASCADE, related_name='other_ids')
    id_number = models.CharField(max_length=20)
    reported_date = models.DateField(null=True, blank=True)
    seq = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'equifax_other_id'

class PANId(models.Model):
    """Model to store PAN ID information"""
    identity_info = models.ForeignKey(IdentityInfo, on_delete=models.CASCADE, related_name='pan_ids')
    id_number = models.CharField(max_length=10)
    reported_date = models.DateField(null=True, blank=True)
    seq = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'equifax_pan_id'

class PersonalInfo(models.Model):
    """Model to store personal information"""
    id_and_contact_info = models.OneToOneField(IDAndContactInfo, on_delete=models.CASCADE, related_name='personal_info')
    age = models.CharField(max_length=5, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=50, blank=True)
    total_income = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'equifax_personal_info'

class PhoneInfo(models.Model):
    """Model to store phone information"""
    id_and_contact_info = models.ForeignKey(IDAndContactInfo, on_delete=models.CASCADE, related_name='phone_info')
    number = models.CharField(max_length=15)
    reported_date = models.DateField(null=True, blank=True)
    seq = models.CharField(max_length=10)
    type_code = models.CharField(max_length=5, blank=True)
    
    class Meta:
        db_table = 'equifax_phone_info'

class OtherKeyInd(models.Model):
    """Model to store other key indicators"""
    cir_report_data = models.OneToOneField(CIRReportData, on_delete=models.CASCADE, related_name='other_key_ind')
    age_of_oldest_trade = models.CharField(max_length=10, blank=True)
    all_lines_ever_written = models.CharField(max_length=20, blank=True)
    all_lines_ever_written_in_6_months = models.CharField(max_length=10, blank=True)
    all_lines_ever_written_in_9_months = models.CharField(max_length=10, blank=True)
    number_of_open_trades = models.CharField(max_length=10, blank=True)
    
    class Meta:
        db_table = 'equifax_other_key_ind'

class RecentActivities(models.Model):
    """Model to store recent activities"""
    cir_report_data = models.OneToOneField(CIRReportData, on_delete=models.CASCADE, related_name='recent_activities')
    accounts_deliquent = models.CharField(max_length=10, blank=True)
    accounts_opened = models.CharField(max_length=10, blank=True)
    accounts_updated = models.CharField(max_length=10, blank=True)
    total_inquiries = models.CharField(max_length=10, blank=True)
    
    class Meta:
        db_table = 'equifax_recent_activities'

class RetailAccountsSummary(models.Model):
    """Model to store retail accounts summary"""
    cir_report_data = models.OneToOneField(CIRReportData, on_delete=models.CASCADE, related_name='retail_accounts_summary')
    average_open_balance = models.CharField(max_length=20, blank=True)
    most_severe_status_within_24_months = models.CharField(max_length=50, blank=True)
    no_of_accounts = models.CharField(max_length=10, blank=True)
    no_of_active_accounts = models.CharField(max_length=10, blank=True)
    no_of_past_due_accounts = models.CharField(max_length=10, blank=True)
    no_of_write_offs = models.CharField(max_length=10, blank=True)
    no_of_zero_balance_accounts = models.CharField(max_length=10, blank=True)
    oldest_account = models.CharField(max_length=100, blank=True)
    recent_account = models.CharField(max_length=100, blank=True)
    single_highest_balance = models.CharField(max_length=20, blank=True)
    single_highest_credit = models.CharField(max_length=20, blank=True)
    single_highest_sanction_amount = models.CharField(max_length=20, blank=True)
    total_balance_amount = models.CharField(max_length=20, blank=True)
    total_credit_limit = models.CharField(max_length=20, blank=True)
    total_high_credit = models.CharField(max_length=20, blank=True)
    total_monthly_payment_amount = models.CharField(max_length=20, blank=True)
    total_past_due = models.CharField(max_length=20, blank=True)
    total_sanction_amount = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'equifax_retail_accounts_summary'

class RetailAccountDetail(models.Model):
    """Model to store retail account details"""
    cir_report_data = models.ForeignKey(CIRReportData, on_delete=models.CASCADE, related_name='retail_account_details')
    account_number = models.CharField(max_length=20)
    account_status = models.CharField(max_length=50, blank=True)
    account_type = models.CharField(max_length=50, blank=True)
    balance = models.CharField(max_length=20, blank=True)
    date_opened = models.DateField(null=True, blank=True)
    date_reported = models.DateField(null=True, blank=True)
    institution = models.CharField(max_length=255, blank=True)
    last_payment_date = models.DateField(null=True, blank=True)
    open = models.CharField(max_length=5, blank=True)
    ownership_type = models.CharField(max_length=20, blank=True)
    past_due_amount = models.CharField(max_length=20, blank=True)
    sanction_amount = models.CharField(max_length=20, blank=True)
    term_frequency = models.CharField(max_length=20, blank=True)
    seq = models.CharField(max_length=10)
    source = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'equifax_retail_account_detail'

class History48Month(models.Model):
    """Model to store 48-month history of retail accounts"""
    retail_account = models.ForeignKey(RetailAccountDetail, on_delete=models.CASCADE, related_name='history_48_months')
    asset_classification_status = models.CharField(max_length=5, blank=True)
    payment_status = models.CharField(max_length=5, blank=True)
    suit_filed_status = models.CharField(max_length=5, blank=True)
    key = models.CharField(max_length=10, blank=True)  # Month-Year format
    
    class Meta:
        db_table = 'equifax_history_48_month'

class ScoreDetail(models.Model):
    """Model to store score details"""
    cir_report_data = models.ForeignKey(CIRReportData, on_delete=models.CASCADE, related_name='score_details')
    name = models.CharField(max_length=20, blank=True)
    type = models.CharField(max_length=20, blank=True)
    value = models.CharField(max_length=10, blank=True)
    version = models.CharField(max_length=10, blank=True)
    
    class Meta:
        db_table = 'equifax_score_detail'

class ScoringElement(models.Model):
    """Model to store scoring elements"""
    score_detail = models.ForeignKey(ScoreDetail, on_delete=models.CASCADE, related_name='scoring_elements')
    description = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=10, blank=True)
    seq = models.CharField(max_length=10)
    type = models.CharField(max_length=10, blank=True)
    
    class Meta:
        db_table = 'equifax_scoring_element'
        
