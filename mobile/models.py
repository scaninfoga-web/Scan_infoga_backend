from django.db import models

class Mobile360Report(models.Model):
    mobile_number = models.CharField(max_length=15, primary_key=True)
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mobile_number
    
class UANHistoryReport(models.Model):
    uan = models.CharField(max_length=20, unique=True)
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uan
    
class UANEmploymentReport(models.Model):
    uan = models.CharField(max_length=20, unique=True)
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uan
    
class ESICReport(models.Model):
    esic_number = models.CharField(max_length=20, unique=True)
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.esic_number

class GSTVerificationReport(models.Model):
    gst_no = models.CharField(max_length=15, unique=True)
    result = models.JSONField(blank=True, null=True)  # store full API response here

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.gst_no  

class GSTTurnoverReport(models.Model):
    gst_no = models.CharField(max_length=15)
    year = models.CharField(max_length=9)  # format like "2022-23"
    result = models.JSONField(blank=True, null=True)  # full API response's "result" field

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('gst_no', 'year')

    def __str__(self):
        return f"{self.gst_no} - {self.year}"

class UdyamReport(models.Model):
    registration_no = models.CharField(max_length=20, primary_key=True)
    result = models.JSONField(blank=True, null=True)  # Store the "result" from the API response

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.registration_no

class ProfileAdvanceReport(models.Model):
    mobile = models.CharField(max_length=15, unique=True)
    result = models.JSONField(blank=True, null=True)  # Only the "result" field from the API

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mobile

class EquifaxV3Report(models.Model):
    mobile = models.CharField(max_length=15)
    name = models.CharField(max_length=255)  # <-- add this
    id_number = models.CharField(max_length=50, primary_key=True)  # <-- add this
    id_type = models.CharField(max_length=20)  # <-- add this
    result = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.mobile} - {self.name}"

class MobileToAccountNumber(models.Model):
    mobile_number = models.CharField(max_length=15, primary_key=True)
    result = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mobile_number


class UanWithoutOtp(models.Model):
    uan = models.CharField(max_length=20, primary_key=True)
    result = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uan

class MobileToDLLookup(models.Model):
    mobile_number = models.CharField(max_length=15, primary_key=True)
    result = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Mobile to DL Lookup for {self.mobile_number}"
    
class PanAllInOne(models.Model):
    pan_number = models.CharField(max_length=10, primary_key=True)
    result = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pan_number

class DigitalPaymentAnalyser(models.Model):
    mobile_number = models.CharField(max_length=15, primary_key=True)
    result = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mobile_number

class LeakOSINT(models.Model):
    request_body = models.CharField(max_length=225, primary_key=True)
    result = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.request_body


class HunterFind(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    result = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class HunterVerify(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    result = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email