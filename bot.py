from collections import deque
from datetime import datetime, timedelta
import time
import pytz
time_zone = pytz.timezone("Asia/Tehran")
import os
import django
from django.conf import settings
from mand_base.mand_base.settings import *
from simple_utils import *
from django_config import get_django_config
from bots_config import get_bot
import threading
from django.db.__init__ import close_old_connections
# import pymysql
# ========================================
CURRENT_ENV = None
CURRENT_ENV = get_environment()
dj_conf = get_django_config()
settings.configure(
  DATABASES=dj_conf['DATABASES'],
  INSTALLED_APPS=dj_conf['INSTALLED_APPS'],
  TIME_ZONE=dj_conf['TIME_ZONE'],
  USE_I18N=dj_conf['USE_I18N'],
  USE_L10N=dj_conf['USE_L10N'],
  USE_TZ=dj_conf['USE_TZ'],
  SECRET_KEY=dj_conf['SECRET_KEY'],
 )
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mand_base.mand_base.settings')
django.setup(dj_conf)
bot = get_bot(CURRENT_ENV)
# ========================================
from menus_and_btns import *
from orm import *
from consts import *
from utilities import *

from telebot import types
# ======================================================================================================
@bot.message_handler(commands = ['deleteacc',])
def delete(message):
  user = get_user(message.from_user)
  user.delete()
  bot.send_message(message.from_user.id, "your user is deleted !")
  # File.objects.all().delete()
  # bot.send_message(message.from_user.id, "all files deleted !")
  return


@bot.message_handler(commands = ['shit',])
def shit(message):
  markup = types.InlineKeyboardMarkup()
  for i in range(1, 30):
    markup.add(types.InlineKeyboardButton(text = i, callback_data="dsoifjsldfij"))
  bot.send_message(message.from_user.id, "grrrrrr", reply_markup=markup)
  markup = types.InlineKeyboardMarkup()
  for i in range(1, 45):
    markup.add(types.InlineKeyboardButton(text = i, callback_data="dsoifjsldfij"))
  bot.send_message(message.from_user.id, "grrrrrr", reply_markup=markup)
  markup = types.InlineKeyboardMarkup()
  for i in range(1, 60):
    markup.add(types.InlineKeyboardButton(text = i, callback_data="dsoifjsldfij"))
  bot.send_message(message.from_user.id, "grrrrrr", reply_markup=markup)
  return






@bot.message_handler(commands = ['admin',])
def admin_starting(message):
  msg = bot.send_message(message.from_user.id, AdminConsts.START_ADMIN)
  bot.clear_step_handler_by_chat_id(chat_id=message.from_user.id)
  bot.register_next_step_handler(msg, check_admin_password)
  return

def start_admin(message):
  msg = bot.send_message(message.from_user.id, AdminConsts.ENTER_ADMIN_PANNEL, reply_markup=AdminMenus.gen_admin_main_menu())
  bot.clear_step_handler_by_chat_id(message.from_user.id)
  bot.register_next_step_handler(msg, admin_main_menu_handler)
  return

def check_admin_password(message):
  if message.text == AdminConsts.PASSWORD :
    start_admin(message)
  else :
    bot.send_message(message.from_user.id, AdminConsts.INVALID_PASSWORD)
    start(message)
  return

def admin_main_menu_invalid_message(message):
  msg = bot.send_message(message.from_user.id, "پیغام نامفهوم ، لطفا دوباره تلاش کنید .", reply_markup=AdminMenus.gen_admin_main_menu())
  bot.clear_step_handler_by_chat_id(message.from_user.id)
  bot.register_next_step_handler(msg, admin_main_menu_handler)
  return

def admin_files_menu_invalid_message(message):
  msg = bot.send_message(message.from_user.id, "پیغام نامفهوم ، لطفا دوباره تلاش کنید .", reply_markup=AdminMenus.gen_files_menu())
  bot.clear_step_handler_by_chat_id(message.from_user.id)
  bot.register_next_step_handler(msg, admin_handel_files_section)
  return

def admin_main_menu_handler(message):
  user = get_user(message.from_user)
  if message.text == AdminConsts.ALL_REGISTERED_USERS_EXCEL :
    send_total_registers_excel(message, user)
  elif message.text == AdminConsts.SEND_AD :
    bot.send_message(user.id, AdminConsts.START_SEND_AD)
    handel_start_ad(message, get_user(message.from_user))
  elif message.text == AdminConsts.FILES :
    msg = bot.send_message(user.id, AdminConsts.START_FILES_SECTION, reply_markup=AdminMenus.gen_files_menu())
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    bot.register_next_step_handler(msg, admin_handel_files_section)
  elif message.text == AdminConsts.EXIT :
    bot.send_message(message.from_user.id, "از پنل ادمین خارج شدید .", reply_markup=ReplyKeyboardRemove())
    start(message)
  else :
    admin_main_menu_invalid_message(message)
  return

def admin_handel_files_section(message):
  if message.text == AdminConsts.NEW_FILE :
    msg = bot.send_message(message.from_user.id, AdminConsts.SEND_YOUR_FILE, reply_markup=AdminMenus.gen_cancel_reply_btn_markup())
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    bot.register_next_step_handler(msg, admin_handel_sending_file)
  elif message.text == AdminConsts.SEE_ALL_FILES :
    files = File.objects.filter(finalized=True).order_by('-creation_datetime')
    msg = bot.send_message(message.from_user.id, AdminConsts.SELECT_FILE_YOU_WANT, reply_markup=AdminMenus.gen_all_files_for_admin(files))
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    bot.register_next_step_handler(msg, admin_handel_selecting_file)
  elif message.text == AdminConsts.BACK :
    start_admin(message)
  else :
    admin_files_menu_invalid_message(message)
  return

def admin_handel_selecting_file(message):
  if message.text == AdminConsts.BACK :
    msg = bot.send_message(message.from_user.id, AdminConsts.START_FILES_SECTION, reply_markup=AdminMenus.gen_files_menu())
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    bot.register_next_step_handler(msg, admin_handel_files_section)
    return
  file_ = File.objects.filter(btn_text=message.text, finalized=True)
  if not file_.exists() :
    bot.send_message(message.from_user.id, "با این متن انتخابی فایلی پیدا نشد !")
    msg = bot.send_message(message.from_user.id, AdminConsts.SELECT_FILE_YOU_WANT, reply_markup=AdminMenus.gen_all_files_for_admin(get_all_files()))
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    bot.register_next_step_handler(msg, admin_handel_selecting_file)
  else :
    file = file_.last()
    bot.copy_message(message.from_user.id, AdminConsts.REFERENCE_CHANNEL, file.msg_id,
                     reply_markup=AdminMenus.gen_show_a_file_to_admin_markup(action="show", file_id=file.id))
    msg = bot.send_message(message.from_user.id, 
                           "اکنون میتوانید این ☝🏻 فایل را حذف کنید ، یا از منو فایل دیگری را انتخاب کنید ...")
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    bot.register_next_step_handler(msg, admin_handel_selecting_file)
  return

def admin_handel_sending_file(message):
  user = get_user(message.from_user)
  try :
    if message.text == "انصراف" :
      bot.send_message(message.from_user.id, "لغو شد !")
      msg = bot.send_message(user.id, AdminConsts.START_FILES_SECTION, reply_markup=AdminMenus.gen_files_menu())
      bot.clear_step_handler_by_chat_id(user.id)
      bot.register_next_step_handler(msg, admin_handel_files_section)
    else :
      file = create_new_file_object(bot, message, user, AdminConsts.REFERENCE_CHANNEL)
      if file :
        msg = bot.send_message(user.id, AdminConsts.FILE_PRIMARILY_SAVED_ENTER_BTN_TEXT)
        bot.clear_step_handler_by_chat_id(user.id)
        bot.register_next_step_handler(msg, handel_set_btn_text_for_file_to_finalize, user, file)
      else :
        msg = bot.send_message(user.id, "عملیات ناموفق بود ...", reply_markup=AdminMenus.gen_files_menu())
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.register_next_step_handler(msg, admin_handel_files_section)
  except Exception as e :
    bot.send_message(341393410, f"error in admin_handel_sending_file: {str(e)}")
    msg = bot.send_message(user.id, "عملیات error بود ...", reply_markup=AdminMenus.gen_files_menu())
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    bot.register_next_step_handler(msg, admin_handel_files_section)

def handel_set_btn_text_for_file_to_finalize(message, user, file):
  if not message.content_type == "text" :
    msg = bot.send_message(user.id, "باید پیام متنی بفرستید ! دوباره تلاش کنید ...")
    bot.clear_step_handler_by_chat_id(user.id)
    bot.register_next_step_handler(msg, handel_set_btn_text_for_file_to_finalize, user, file)
  elif File.objects.filter(btn_text=message.text).exists() :
    msg = bot.send_message(user.id, "اسم دکمه قبلا برای فایل دیگری ثبت شده ! دوباره امتحان کنید ...")
    bot.clear_step_handler_by_chat_id(user.id)
    bot.register_next_step_handler(msg, handel_set_btn_text_for_file_to_finalize, user, file)
  elif len(message.text) > 40 :
    msg = bot.send_message(user.id, "طول اسم دکمه باید حداکثر 40 کاراکتر باشد تا به درستی نمایش داده شود ! دوباره امتحان کنید ...")
    bot.clear_step_handler_by_chat_id(user.id)
    bot.register_next_step_handler(msg, handel_set_btn_text_for_file_to_finalize, user, file)
  else :
    btn_text = message.text
    file.btn_text = btn_text
    file.finalized = True
    file.save()
    bot.send_message(user.id, AdminConsts.FINALLY_SAVED_FILE)
    msg = bot.send_message(user.id, AdminConsts.START_FILES_SECTION, reply_markup=AdminMenus.gen_files_menu())
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    bot.register_next_step_handler(msg, admin_handel_files_section)

def send_total_registers_excel(message, user):
    file = all_registerations_excel_file(bot)
    if not file :
      bot.send_message(user.id, "مشکلی پیش اومد !")
      msg = bot.send_message(message.from_user.id, AdminConsts.BACK_TO_ADMIN_MENU, reply_markup=AdminMenus.gen_admin_main_menu())
      bot.clear_step_handler_by_chat_id(message.from_user.id)
      bot.register_next_step_handler(msg, admin_main_menu_handler)
      return
    else :
      today = datetime.now(time_zone).date()
      jalali_date = gregorian_to_jalali(today.year, today.month, today.day)
      jy = jalali_date[0]
      jm = month_name(jalali_date[1])
      jd = jalali_date[2]
      caption = f"گزارش تمام کاربران ربات - تاریخ گزارش {jd} {jm} {jy}"
      bot.send_document(user.id, file, caption=caption)
      msg = bot.send_message(message.from_user.id, AdminConsts.BACK_TO_ADMIN_MENU, reply_markup=AdminMenus.gen_admin_main_menu())
      bot.clear_step_handler_by_chat_id(message.from_user.id)
      bot.register_next_step_handler(msg, admin_main_menu_handler)
      return

def handel_start_ad(message, user, source_user_msg=None):
  try:
    if message.text == AdminConsts.SEND:
      if not message.reply_to_message:
        bot.send_message(user.id, AdminConsts.REMIND_SEND)
        msg = bot.send_message(message.from_user.id, AdminConsts.BACK_TO_ADMIN_MENU, reply_markup=AdminMenus.gen_admin_main_menu())
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.register_next_step_handler(msg, admin_main_menu_handler)
        return
      bot.send_message(user.id, 'در حال ارسال')
      thread = threading.Thread(target=send_message_to_all, args=(bot, message.reply_to_message))
      thread.start()
      msg = bot.send_message(message.from_user.id, AdminConsts.BACK_TO_ADMIN_MENU, reply_markup=AdminMenus.gen_admin_main_menu())
      bot.clear_step_handler_by_chat_id(message.from_user.id)
      bot.register_next_step_handler(msg, admin_main_menu_handler)
      return
    # elif message.text == AdminConsts.ADD_BTN :
    #   if not message.reply_to_message:
    #     bot.send_message(user.id, AdminConsts.REMIND_SEND)
    #     msg = bot.send_message(message.from_user.id, AdminConsts.BACK_TO_ADMIN_MENU, reply_markup=AdminMenus.gen_admin_main_menu())
    #     bot.clear_step_handler_by_chat_id(message.from_user.id)
    #     bot.register_next_step_handler(msg, admin_main_menu_handler)
    #     return
      # source_user_msg = message.reply_to_message
      # msg = bot.send_message(user.id, AdminConsts.CHOOSE_BTN_FORMAT, reply_markup=AdminMenus.gen_choose_btn_format_to_create_markup())
      # bot.clear_step_handler_by_chat_id(chat_id=user.id)
      # bot.register_next_step_handler(msg, handel_start_ad, user, source_user_msg)
      # return
    # elif message.text == AdminConsts.LINK_BTN:
    #   msg = bot.send_message(user.id, AdminConsts.SEND_YOUR_LINK, reply_markup=AdminMenus.gen_cancel_reply_btn_markup())
    #   bot.clear_step_handler_by_chat_id(chat_id=user.id)
    #   bot.register_next_step_handler(msg, handel_adding_btn_to_ad_msg, user, source_user_msg, AdminConsts.LINK_BTN, "", "")
    #   return
    # elif message.text == AdminConsts.WEB_APP_BTN:
    #   msg = bot.send_message(user.id, AdminConsts.SEND_YOUR_LINK, reply_markup=AdminMenus.gen_cancel_reply_btn_markup())
    #   bot.clear_step_handler_by_chat_id(chat_id=user.id)
    #   bot.register_next_step_handler(msg, handel_adding_btn_to_ad_msg, user, source_user_msg, AdminConsts.LINK_BTN, "", "")
    #   return
    elif message.text == AdminConsts.BACK:
      msg = bot.send_message(message.from_user.id, AdminConsts.BACK_TO_ADMIN_MENU, reply_markup=AdminMenus.gen_admin_main_menu())
      bot.clear_step_handler_by_chat_id(message.from_user.id)
      bot.register_next_step_handler(msg, admin_main_menu_handler)
      return
    else:
      msg = bot.send_message(user.id, AdminConsts.REMIND_SEND)
      bot.clear_step_handler_by_chat_id(chat_id=user.id)
      bot.register_next_step_handler(msg, handel_start_ad, user)
      return
  except Exception as e:
    bot.send_message(user.id, 'مشکلی پیش آمده')
    bot.send_message(user.id, str(e))

def handel_send_or_cancel_btn_ad_msg(message, user, final_msg, btn_type, btn_link, btn_text):
  if message.text == "بازگشت":
    msg = bot.send_message(message.from_user.id, AdminConsts.BACK_TO_ADMIN_MENU, reply_markup=AdminMenus.gen_admin_main_menu())
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    bot.register_next_step_handler(msg, admin_main_menu_handler)
    return
  elif message.text == AdminConsts.SEND_TO_ALL :
    bot.send_message(user.id, 'در حال ارسال')
    markup = AdminMenus.gen_markup_for_btn_ad(btn_type, btn_text, btn_link)
    thread = threading.Thread(target=send_btn_message_to_all, args=(bot, final_msg, markup, ))
    thread.start()
    msg = bot.send_message(message.from_user.id, AdminConsts.BACK_TO_ADMIN_MENU, reply_markup=AdminMenus.gen_admin_main_menu())
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    bot.register_next_step_handler(msg, admin_main_menu_handler)
    return

def add_btn_under_msg_and_send_final_msg_to_user(bot, user, source_user_msg, btn_type, btn_link, btn_text):
    markup = AdminMenus.gen_markup_for_btn_ad(btn_type, btn_text, btn_link)
    msg = copy_message_and_add_btn(bot, reciver=user, markup=markup, source_msg=source_user_msg)
    return msg

def handel_adding_btn_to_ad_msg(message, user, source_user_msg, btn_type, btn_link, btn_text):
  if message.text == 'انصراف':
    msg = bot.send_message(message.from_user.id, AdminConsts.BACK_TO_ADMIN_MENU, reply_markup=AdminMenus.gen_admin_main_menu())
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    bot.register_next_step_handler(msg, admin_main_menu_handler)
    return
  elif message.text.startswith('https'):
    entered_btn_link = message.text
    msg = bot.send_message(user.id, AdminConsts.SEND_BTN_TITLE, reply_markup=AdminMenus.gen_cancel_reply_btn_markup())
    bot.clear_step_handler_by_chat_id(chat_id=user.id)
    bot.register_next_step_handler(msg, handel_adding_btn_to_ad_msg, user, source_user_msg, btn_type, entered_btn_link, "")
    return
  else :
    entered_btn_text = message.text
    final_msg = add_btn_under_msg_and_send_final_msg_to_user(bot, user, source_user_msg, btn_type, btn_link, entered_btn_text)
    msg = bot.send_message(user.id, AdminConsts.CHECK_FINAL_MSG_AND_SEND_IT, reply_markup=AdminMenus.gen_send_btn_ad_to_all_users_or_cancel())
    bot.clear_step_handler_by_chat_id(chat_id=user.id)
    bot.register_next_step_handler(msg, handel_send_or_cancel_btn_ad_msg, user, final_msg, btn_type, btn_link, btn_text)
    return


@bot.callback_query_handler(func=lambda query: "deleteFile:" in query.data)
def delete_a_file_by_admin(query):
  data = query.data
  action = data.split(":")[-2]
  file_id = int(data.split(":")[-1])
  if action == "tryDelete" :
    bot.edit_message_reply_markup(query.from_user.id, query.message.message_id,
                                  reply_markup=AdminMenus.gen_show_a_file_to_admin_markup(action="delete_confirmation", file_id=file_id))
  elif action == "finalDelete" :
    file = find_file(file_id)
    file.delete()
    bot.edit_message_reply_markup(query.from_user.id, query.message.message_id,
                                  reply_markup=AdminMenus.gen_show_a_file_to_admin_markup(action="deleted", file_id=file_id))
  elif action == "keep" :
    bot.edit_message_reply_markup(query.from_user.id, query.message.message_id,
                                  reply_markup=AdminMenus.gen_show_a_file_to_admin_markup(action="show", file_id=file_id))
  return






































@bot.chat_join_request_handler()
def join_request_handler(join_request):
  try :
    user = get_user(join_request.from_user)
    starting_str = "دوست"
    if user.tel_firstname :
      starting_str = user.tel_firstname
    bot.send_message(user.id, UserConsts.JOIN_REQUEST_WELCOME_MSG.format(starting_str))
  except :
    ...


@bot.message_handler(commands = ['start',])
def start(message):
  user = get_user(message.from_user)
  if user.completed_user_data :
    msg = bot.send_message(user.id, get_start_msg_for_user(user), reply_markup=UserMenus.gen_main_menu(user))
    bot.clear_step_handler_by_chat_id(chat_id=user.id)
    bot.register_next_step_handler(msg, user_main_menu_handler)
    return
  else :
    # register process
    ask_fullname(user)

def ask_fullname(user):
  msg = bot.send_message(user.id, UserConsts.ASK_NAME)
  bot.clear_step_handler_by_chat_id(chat_id=user.id)
  bot.register_next_step_handler(msg, save_name, user)
  return

def save_name(message, user):
  # validation of entered fullname
  if not validate_entered_fullname(message.text) :
    msg = bot.send_message(user.id, UserConsts.FULLNAME_TOO_LONG)
    bot.clear_step_handler_by_chat_id(chat_id=user.id)
    bot.register_next_step_handler(msg, save_name, user)
    return
  # save fullname
  user.fullname = message.text
  user.save()
  # let's ask user's grade
  bot.send_message(user.id, UserConsts.ASK_GRADE, reply_markup=UserMenus.gen_grades_glass_btns())
  return
  
@bot.callback_query_handler(func= lambda query: "set_grade:" in query.data)
def set_grade(query):
  user = get_user(query.from_user)
  # save grade
  user.grade = int(query.data.split(":")[-1])
  user.save()
  # check if user needs to be asked major
  if user.grade >= 9 :
    # let's ask major
    bot.edit_message_text(UserConsts.ASK_MAJOR, user.id, query.message.message_id, reply_markup=UserMenus.gen_majors_glass_btns())
    return
  # let's ask phone number
  bot.delete_message(user.id, query.message.message_id)
  msg = bot.send_message(user.id, UserConsts.ASK_PHONE_NUMBER)
  bot.clear_step_handler_by_chat_id(chat_id=user.id)
  bot.register_next_step_handler(msg, get_phone_number, user)
  return

@bot.callback_query_handler(func= lambda query: "set_major:" in query.data)
def set_grade(query):
  user = get_user(query.from_user)
  # save major
  user.major = int(query.data.split(":")[-1])
  user.save()
  # let's ask phone number
  msg = bot.edit_message_text(UserConsts.ASK_PHONE_NUMBER, user.id, query.message.message_id)
  # msg = bot.send_message(user.id, UserConsts.ASK_PHONE_NUMBER)
  bot.clear_step_handler_by_chat_id(chat_id=user.id)
  bot.register_next_step_handler(msg, get_phone_number, user)
  return

def get_phone_number(message, user):
  # phone validation
  phone_number = validate_entered_phone(message.text)
  if not phone_number :
    msg = bot.send_message(user.id, UserConsts.INVALID_ENTERED_PHONE_NUMBER)
    bot.clear_step_handler_by_chat_id(chat_id=user.id)
    bot.register_next_step_handler(msg, get_phone_number, user)
    return
  # let's send sms
  verify_phone(phone_number)
  msg = bot.send_message(user.id, UserConsts.VERIFICATION_CODE_IS_SENT.format(phone_number))
  bot.clear_step_handler_by_chat_id(chat_id=user.id)
  bot.register_next_step_handler(msg, verify_code_and_save_phone_number, user, phone_number)
  return

def verify_code_and_save_phone_number(message, user, phone_number):
  code = message.text
  if check_verifCode(phone_number, code):
    # code is true and we can save phone number !
    user.phone_number = phone_number
    user.check_data_complition()
    user.save()
    bot.send_message(user.id, "تائید شد ✅")
    start(message)
    return
  else :
    bot.send_message(user.id, "رد شد ❌")
    msg = bot.send_message(user.id, UserConsts.ASK_PHONE_NUMBER)
    bot.clear_step_handler_by_chat_id(chat_id=user.id)
    bot.register_next_step_handler(msg, get_phone_number, user)
    return

@bot.callback_query_handler(func= lambda query: "edit_user_data:" in query.data)
def edit_user_data(query):
  action = query.data.split(":")[-1]
  user = get_user(query.from_user)
  if action == "back" :
    bot.delete_message(user.id, query.message.message_id)
    msg = bot.send_message(user.id, get_start_msg_for_user(user), reply_markup=UserMenus.gen_main_menu(user))
    bot.clear_step_handler_by_chat_id(chat_id=user.id)
    bot.register_next_step_handler(msg, user_main_menu_handler)
    return
  elif action == "name" :
    msg = bot.send_message(user.id, "اسم جدیدت رو بفرست ⛏")
    bot.clear_step_handler_by_chat_id(chat_id=user.id)
    bot.register_next_step_handler(msg, edit_user_fullname, user)
    return
  elif action == "grade" :
    bot.send_message(user.id, "پایت رو انتخاب کن ...", reply_markup=UserMenus.gen_editing_grades_glass_btns())
    return
  elif action == "major" :
    bot.send_message(user.id, "رشتت رو انتخاب کن ...", reply_markup=UserMenus.gen_editing_majors_glass_btns())
    return

def edit_user_fullname(message, user):
  if not validate_entered_fullname(message.text) :
    msg = bot.send_message(user.id, UserConsts.FULLNAME_TOO_LONG)
    bot.clear_step_handler_by_chat_id(chat_id=user.id)
    bot.register_next_step_handler(msg, edit_user_fullname, user)
    return
  # save fullname
  user.fullname = message.text
  user.save()
  bot.send_message(user.id, f"اسمت با موفقیت تغییر کرد به {user.fullname}")
  start(message)

@bot.callback_query_handler(func= lambda query: "edit_grade:" in query.data)
def edit_data_grade(query):
  user = get_user(query.from_user)
  user.grade = int(query.data.split(":")[-1])
  user.save()
  bot.delete_message(user.id, query.message.message_id)
  bot.send_message(user.id, f"✅ پایت با موفقیت تغییر کرد به {get_grade_name(user.grade)}")
  msg = bot.send_message(user.id, get_start_msg_for_user(user), reply_markup=UserMenus.gen_main_menu(user))
  bot.clear_step_handler_by_chat_id(chat_id=user.id)
  bot.register_next_step_handler(msg, user_main_menu_handler)
  return

@bot.callback_query_handler(func= lambda query: "edit_major:" in query.data)
def edit_data_major(query):
  user = get_user(query.from_user)
  user.major = int(query.data.split(":")[-1])
  user.save()
  bot.delete_message(user.id, query.message.message_id)
  bot.send_message(user.id, f"✅ رشتت با موفقیت تغییر کرد به {get_major_name(user.major)}")
  msg = bot.send_message(user.id, get_start_msg_for_user(user), reply_markup=UserMenus.gen_main_menu(user))
  bot.clear_step_handler_by_chat_id(chat_id=user.id)
  bot.register_next_step_handler(msg, user_main_menu_handler)
  return

@bot.callback_query_handler(func= lambda query: "user_show_file:" in query.data)
def user_file_selection(query):
  user = get_user(query.from_user)
  file_id = int(query.data.split(":")[-1])
  file = find_file(file_id)
  if not file :
    bot.send_message(user.id, UserConsts.THIS_FILE_IS_DELETED)
  else :
    bot.copy_message(user.id, AdminConsts.REFERENCE_CHANNEL, file.msg_id)
  





@bot.message_handler()
def user_main_menu_handler(message):
  user = get_user(message.from_user)
  # check for possible message options
  if message.text == UserConsts.MY_USER_DATA_BTN:
    user_data_msg_text = UserConsts.MY_USER_DATA.format(user.fullname, get_grade_name(user.grade), get_major_name(user.major)) if user.grade >= 9 else UserConsts.MY_USER_DATA_WITHOUT_MAJOR.format(user.fullname, get_grade_name(user.grade))
    bot.send_message(user.id,
    user_data_msg_text,
    reply_markup=UserMenus.gen_edit_user_data_glass_menu(user.grade))
  elif message.text == UserConsts.FILES_SECTION :
    bot.send_message(user.id,
                     UserConsts.ENTER_FILES_SECTION.format(user.fullname),
                     reply_markup=UserMenus.gen_all_files_markup(get_all_files())
                     )
  elif message.text == '/start' :
    start(message)
  elif message.text == '/admin' :
    admin_starting(message)
  elif message.text == "/deleteacc" :
    delete(message)
  else :
    bot.send_message(user.id, UserConsts.INVALID_MSG_ON_MAIN_MENU)
    start(message)
  return








# ======================================================================================================
if __name__ == '__main__':
  print(f'bot running on {CURRENT_ENV} environment')
  bot.send_message(341393410, "bot is running !")
  init_loggers()
  while True:
    try:
      bot.send_message(341393410, "WHILE started ! let's poll the bot !")
      bot.polling(none_stop=True, timeout=60)
    except KeyboardInterrupt:
      exit()
    except Exception as e:
      bot.send_message(341393410, str(e))
      main_log = logging.getLogger('main_log')
      main_log.error(str(e))
      django.setup()
      # bot.stop_polling()
      # time.sleep(5)

