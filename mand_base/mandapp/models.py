from django.db import models
from django.utils.translation import gettext_lazy as _
import random
from datetime import datetime
import pytz
time_zone = pytz.timezone("Asia/Tehran")
import requests
import telebot
testbot = telebot.TeleBot('6709376264:AAERpPTQJQNQbpgIp7-40ky7mfDhKDvjKnY', threaded=False)
# ======================================================================================
def get_default_verifCode():
    return random.randint(1000, 9999)
token_url = "http://RestfulSms.com/api/Token"
token_body = {
	"UserApiKey"  :"4be326ac803595315aa3f2b",
	"SecretKey" : "first_sec_code_sms_ir_f5@H7^%3jO"
             }
mainurl = "https://RestfulSms.com/api/VerificationCode"
fasturl = "https://RestfulSms.com/api/UltraFastSend"

def sms_ir_get_TokenKey():
    token_resp = requests.post(token_url, data=token_body)
    token_data = token_resp.json()
    if token_data['IsSuccessful'] == True :
        return token_data['TokenKey']
    return

def sms_ir_send_verif_sms(verif_code, phone_number):
    TokenKey = sms_ir_get_TokenKey()
    mainheaders = {}
    mainheaders["x-sms-ir-secure-token"] = TokenKey
    mainbody = {
        "Code" : str(verif_code),
        "MobileNumber" : str(phone_number)}
    resp = requests.post(mainurl, data=mainbody, headers=mainheaders)
    data = resp.json()
    if not data['IsSuccessful'] :
        return False
    return True

def get_current_date():
    return datetime.now(time_zone).date()

def get_current_datetime():
    return datetime.now(time_zone)
# ======================================================================================
class Grade(models.IntegerChoices):
    FIRST = 1, _('اول')
    SECOND = 2, _('دوم')
    THIRD = 3, _('سوم')
    FORTH = 4, _('چهارم')
    FIFTH = 5, _('پنجم')
    SIXTH = 6, _('ششم')
    SEVENTH = 7, _('هفتم')
    EIGHTH = 8, _('هشتم')
    NINETH = 9, _('نهم')
    TENTH = 10, _('دهم')
    ELEVENTH = 11, _('یازدهم')
    TWELWETH = 12, _('دوازدهم')
    FINISHED_SCHOOL = 18, _('فارغ التحصیل')

class Major(models.IntegerChoices):
    MATH = 0, _('ریاضی')
    SIENCE = 1, _('تجربی')
    HUMN = 2, _('انسانی')
    ART = 3, _('هنر')
    OTHER = 4, _('سایر')

class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    tel_firstname = models.TextField(null=True, default=None, blank=True)
    tel_lastname = models.TextField(null=True, default=None, blank=True)
    tel_username = models.TextField(null=True, default=None, blank=True)
    fullname = models.CharField(max_length=50, null=True, default=None, blank=True)
    phone_number = models.CharField(max_length=11, null=True, default=None, blank=True)
    grade = models.IntegerField(choices=Grade.choices, null=True, default=None, blank=True)
    major = models.IntegerField(choices=Major.choices, null=True, default=None, blank=True)
    completed_user_data = models.BooleanField(default=False)
    register_date = models.DateField(default=get_current_date)
    def __str__(self):
        return self.fullname
    def check_data_complition(self):
        if (
            self.fullname != None,
            self.grade != None,
            self.major != None,
            self.phone_number != None,
        ):
            self.completed_user_data = True
            self.save()

class VrifCode(models.Model):
    code = models.IntegerField(default=get_default_verifCode)
    phone_number = models.CharField(max_length=11, null=True, default=None)
    is_sent = models.BooleanField(default=False)
    def save(self, force_insert=False, force_update=True, *args, **kwargs):
        super(VrifCode, self).save()
        if not self.is_sent :
            sending_status = sms_ir_send_verif_sms(self.code, self.phone_number)
            if not sending_status :
                testbot.send_message(341393410, f"couldn't send sms ! num:{self.phone_number}")
            else :
                self.is_sent = True
                super(VrifCode, self).save()

class File(models.Model):
    btn_text = models.TextField(null=True, default=None, blank=True)
    msg_type = models.TextField(null=True, default=None, blank=True)
    msg_id = models.IntegerField(null=True, default=None, blank=True) # message_id in reference channel
    creation_datetime = models.DateTimeField(default=get_current_datetime)
    added_by = models.ForeignKey(User, null=True, default=None, blank=True, on_delete=models.SET_NULL, related_name="added_files")
    finalized = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
