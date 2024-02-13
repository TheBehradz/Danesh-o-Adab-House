from consts import *
from xlsxwriter import Workbook
from orm import User, get_grade_name, get_major_name
# ==========================================

def get_start_msg_for_user(user):
    # if not user.completed_user_data :
    #     return UserConsts.MSG_ON_START_WITH_NO_USER_DATA
    # else :
    #     return UserConsts.MSG_ON_START
    return UserConsts.MSG_ON_START

def validate_entered_fullname(fullname):
    if len(fullname) > 50 :
        return False
    return True

def make_english_phone_number(phone):
    eng_phone = ""
    for char in phone :
        if char == '۰':
            eng_phone += "0"
        elif char == '۱':
            eng_phone += "1"
        elif char == '۲':
            eng_phone += "2"
        elif char == '۳':
            eng_phone += "3"
        elif char == '۴':
            eng_phone += "4"
        elif char == '۵':
            eng_phone += "5"
        elif char == '۶':
            eng_phone += "6"
        elif char == '۷':
            eng_phone += "7"
        elif char == '۸':
            eng_phone += "8"
        elif char == '۹':
            eng_phone += "9"
        elif char in "0123456789" :
            eng_phone += char
    return eng_phone

def validate_entered_phone(entered_phone):
    if len(entered_phone) != 11 :
        return None
    phone = make_english_phone_number(entered_phone)
    if not phone.startswith("09"):
        return None
    return phone

def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if (gm > 2):
        gy2 = gy + 1
    else:
        gy2 = gy
    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    jy = -1595 + (33 * (days // 12053))
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if (days < 186):
        jm = 1 + (days // 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + ((days - 186) // 30)
        jd = 1 + ((days - 186) % 30)
    return [jy, jm, jd]


def jalali_to_gregorian(jy, jm, jd):
    jy += 1595
    days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
    if (jm < 7):
        days += (jm - 1) * 31
    else:
        days += ((jm - 7) * 30) + 186
    gy = 400 * (days // 146097)
    days %= 146097
    if (days > 36524):
        days -= 1
        gy += 100 * (days // 36524)
        days %= 36524
    if (days >= 365):
        days += 1
    gy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        gy += ((days - 1) // 365)
        days = (days - 1) % 365
    gd = days + 1
    if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        kab = 29
    else:
        kab = 28
    sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    while (gm < 13 and gd > sal_a[gm]):
        gd -= sal_a[gm]
        gm += 1
    return [gy, gm, gd]

def all_registerations_excel_file(bot):
    try :
        users = User.objects.all().order_by('-register_date')
        workbook = Workbook(f'/0MandProject/Mand/mandBot_registers_report.XLSX')
        worksheet = workbook.add_worksheet()
        worksheet.right_to_left()
        worksheet.write('A1', 'نام')
        worksheet.write('B1', 'شماره تلفن')
        worksheet.write('C1', 'پایه')
        worksheet.write('D1', 'رشته')
        worksheet.write('E1', 'تاریخ ثبت نام')
        worksheet.write('F1', 'روز ثبت نام')
        worksheet.write('G1', 'ماه ثبت نام')
        worksheet.write('H1', 'سال ثبت نام')
        worksheet.write('I1', 'یوزرنیم تلگرام')
        worksheet.write('J1', 'یوزر آیدی تلگرام')
        worksheet.write('K1', 'اسم کوچک در تلگرام')
        worksheet.write('L1', 'فامیلی در تلگرام')
        c = 2
        dateFormat = workbook.add_format({'num_format': 'd mmm yyyy'})
        for user in users :
            reg_date = user.register_date
            y, m, d = gregorian_to_jalali(reg_date.year, reg_date.month, reg_date.day)
            worksheet.write(f"A{c}", user.fullname)
            worksheet.write(f"B{c}", user.phone_number)
            worksheet.write(f"C{c}", get_grade_name(user.grade))
            worksheet.write(f"D{c}", get_major_name(user.major))
            worksheet.write(f"E{c}", user.register_date, dateFormat)
            worksheet.write(f"F{c}", d)
            worksheet.write(f"G{c}", m)
            worksheet.write(f"H{c}", y)
            worksheet.write(f"I{c}", user.tel_username)
            worksheet.write(f"J{c}", user.id)
            worksheet.write(f"K{c}", user.tel_firstname)
            worksheet.write(f"L{c}", user.tel_lastname)
            c += 1
        workbook.close()
        file = open('/0MandProject/Mand/mandBot_registers_report.XLSX', 'rb')
        return file
    except Exception as e :
        bot.send_message(341393410, f"error in all_registerations_excel_file:{str(e)}")
        return None

def month_name(month):
    l = ['فروردین',
    'اردیبهشت',
    'خرداد',
    'تیر',
    'مرداد',
    'شهریور',
    'مهر',
    'آبان',
    'آذر',
    'دی',
    'بهمن',
    'اسفند',
    ]
    return l[int(month)-1]




def copy_message_and_add_btn(bot, reciver, markup, source_msg):
  try :
    message = source_msg
    if message.content_type == 'photo':
      msg = bot.send_photo(reciver.id, message.photo[-1].file_id, caption=message.caption, reply_markup=markup)
    elif message.content_type == 'video':
      msg = bot.send_video(reciver.id, message.video.file_id, caption=message.caption, reply_markup=markup)
    elif message.content_type == 'text':
      msg = bot.send_message(reciver.id, message.text, reply_markup=markup)
    elif message.content_type == 'audio':
      msg = bot.send_audio(reciver.id, message.audio.file_id, caption=message.caption, reply_markup=markup)
    elif message.content_type == 'voice':
      msg = bot.send_voice(reciver.id, message.voice.file_id, caption=message.caption, reply_markup=markup)
    elif message.content_type == 'document':
      msg = bot.send_document(reciver.id, message.document.file_id, caption=message.caption, reply_markup=markup)
    elif message.content_type == 'animation':
      msg = bot.send_document(reciver.id, message.animation.file_id, caption=message.caption, reply_markup=markup) 
    return msg
  except Exception as e :
    bot.send_message(341393410, "error in copy_message_and_add_btn"+str(e))


def send_btn_message_to_all(bot, source_msg, markup):
  users = User.objects.filter()
  for user in users :
    copy_message_and_add_btn(bot, user, markup, source_msg)


def copy_message(bot, reciver, message):
  try :
    if message.content_type == 'photo':
      bot.send_photo(reciver.id, message.photo[-1].file_id, caption=message.caption)
    elif message.content_type == 'video':
      bot.send_video(reciver.id, message.video.file_id, caption=message.caption)
    elif message.content_type == 'text':
      bot.send_message(reciver.id, message.text)
    elif message.content_type == 'audio':
      bot.send_audio(reciver.id, message.audio.file_id, caption=message.caption)
    elif message.content_type == 'voice':
      bot.send_voice(reciver.id, message.voice.file_id, caption=message.caption)
    elif message.content_type == 'document':
      bot.send_document(reciver.id, message.document.file_id, caption=message.caption)
    elif message.content_type == 'animation':
      bot.send_document(reciver.id, message.animation.file_id, caption=message.caption) 
    else:
      print(f'{message.content_type} can not be send')
      return False
    return True
  except :
    return False

def send_message_to_all(bot, message):
  try :
    users = User.objects.filter()
    for user in users:
      copy_message(bot, user, message)
  except Exception as e :
    bot.send_message("341393410", f"error in send_message_to_all :\n{e}")

