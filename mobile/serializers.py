from rest_framework import serializers
from .models import Mobile360Report, UANHistoryReport, UANEmploymentReport, ESICReport, GSTVerificationReport, UdyamReport, ProfileAdvanceReport, EquifaxV3Report, GSTTurnoverReport, MobileToAccountNumber, UanWithoutOtp, MobileToDLLookup, PanAllInOne, DigitalPaymentAnalyser, LeakOSINT, HunterFind, HunterVerify

class Mobile360ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile360Report
        fields = '__all__'

class UANHistoryReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UANHistoryReport
        fields = '__all__'

class UANEmploymentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UANEmploymentReport
        fields = '__all__'
        
class ESICReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESICReport
        fields = '__all__'
        
class GSTVerificationReportSerializer(serializers.ModelSerializer):
    # Example: expose legal_name from nested result JSON
    legal_name = serializers.SerializerMethodField()

    class Meta:
        model = GSTVerificationReport
        fields = ['gst_no', 'result', 'legal_name', 'created_at', 'updated_at']

    def get_legal_name(self, obj):
        if obj.result:
            return obj.result.get('legal_name')
        return None

class UdyamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UdyamReport
        fields = '__all__'
    
class ProfileAdvanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ProfileAdvanceReport

class EquifaxV3ReportSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = EquifaxV3Report

class GSTTurnoverReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = GSTTurnoverReport
        fields = '__all__'

class MobileToAccountNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileToAccountNumber
        fields = '__all__'

class UanWithoutOtpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = UanWithoutOtp

class MobileToDLLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileToDLLookup
        fields = '__all__'
        
class PanAllInOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanAllInOne
        fields = '__all__'

class DigitalPaymentAnalyserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalPaymentAnalyser
        fields = '__all__'

class LeakOSINTSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeakOSINT
        fields = '__all__'
        
class HunterFindSerializer(serializers.ModelSerializer):
    class Meta:
        model = HunterFind
        fields = '__all__'

class HunterVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = HunterVerify
        fields = '__all__'