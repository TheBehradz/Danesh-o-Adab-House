from mand_base.mandapp.models import *

# =======================================================

def get_user(tel_user):
    try :
        return User.objects.get(id=tel_user.id)
    except User.DoesNotExist :
        return User.objects.create(id=tel_user.id, tel_firstname=tel_user.first_name , tel_lastname=tel_user.last_name, tel_username=tel_user.username)

def get_major_by_farsi_name(farsi_name):
    if farsi_name == "ریاضی" :
        return Major.MATH
    if farsi_name == "تجربی" :
        return Major.SIENCE
    if farsi_name == "انسانی" :
        return Major.HUMN
    if farsi_name == "هنر" :
        return Major.ART
    if farsi_name == "سایر" :
        return Major.OTHER

def verify_phone(phone_number):
    vc = VrifCode.objects.create(phone_number=phone_number)
    if vc.is_sent :
        return True
    return False

def check_verifCode(phone_number, code):
    try :
        if VrifCode.objects.filter(phone_number=phone_number).exists():
            last_vc = VrifCode.objects.filter(phone_number=phone_number).last()
            return int(code) == last_vc.code
        return False
    except :
        return False

def get_grade_name(grade):
    if grade == Grade.FIRST :
        return "اول"
    elif grade == Grade.SECOND :
        return "دوم"
    elif grade == Grade.THIRD :
        return "سوم"
    elif grade == Grade.FORTH :
        return "چهارم"
    elif grade == Grade.FIFTH :
        return "پنجم"
    elif grade == Grade.SIXTH :
        return "ششم"
    elif grade == Grade.SEVENTH :
        return "هفتم"
    elif grade == Grade.EIGHTH :
        return "هشتم"
    elif grade == Grade.NINETH :
        return "نهم"
    elif grade == Grade.TENTH :
        return "دهم"
    elif grade == Grade.ELEVENTH :
        return "یازدهم"
    elif grade == Grade.TWELWETH :
        return "دوازدهم"
    elif grade == Grade.FINISHED_SCHOOL :
        return "فارغ التحصیل"
    return "ثبت نشده !"

def get_major_name(major):
    if major == Major.MATH :
        return "ریاضی"
    elif major==Major.HUMN :
        return "انسانی"
    elif major==Major.SIENCE :
        return "تجربی"
    elif major==Major.ART :
        return "هنر"
    elif major==Major.OTHER :
        return "سایر"
    return "ثبت نشده !"



def put_msg_in_channel(bot, reference_channel, message):
  reciver = reference_channel
  try :
    if message.content_type == 'photo':
      msg = bot.send_photo(reciver, message.photo[-1].file_id, caption=message.caption)
    elif message.content_type == 'video':
      msg = bot.send_video(reciver, message.video.file_id, caption=message.caption)
    elif message.content_type == 'text':
      msg = bot.send_message(reciver, message.text)
    elif message.content_type == 'audio':
      msg = bot.send_audio(reciver, message.audio.file_id, caption=message.caption)
    elif message.content_type == 'voice':
      msg = bot.send_voice(reciver, message.voice.file_id, caption=message.caption)
    elif message.content_type == 'document':
      msg = bot.send_document(reciver, message.document.file_id, caption=message.caption)
    elif message.content_type == 'animation':
      msg = bot.send_document(reciver, message.animation.file_id, caption=message.caption) 
    else:
      return None
    return msg.message_id
  except :
    return None

def create_new_file_object(bot, message, user, reference_channel):
    try :
        in_channel_msg_id = put_msg_in_channel(bot, reference_channel, message)
        msg_content_type = message.content_type
        if not in_channel_msg_id :
            return None
        file = File.objects.create(
            msg_type=msg_content_type,
            msg_id=in_channel_msg_id,
            added_by=user,
        )
        file.save()
        return file
    except Exception as e :
        bot.send_message(341393410, f"error in create_new_file_object: {str(e)}")
        return None

def find_file(id):
    try :
        return File.objects.get(id=int(id))
    except :
        return None
    
def get_all_files():
    return File.objects.filter(finalized=True).order_by('-creation_datetime')