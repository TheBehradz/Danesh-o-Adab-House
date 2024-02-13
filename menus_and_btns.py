from telebot.types import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, WebAppInfo,)

from consts import UserConsts, AdminConsts

# ==============================================================================================
class AdminMenus:
    def gen_admin_main_menu():
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton(AdminConsts.FILES))
        markup.add(
            KeyboardButton(AdminConsts.ALL_REGISTERED_USERS_EXCEL),
            KeyboardButton(AdminConsts.SEND_AD))
        markup.add(KeyboardButton(AdminConsts.EXIT))
        return markup
    def gen_files_menu():
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(
            KeyboardButton(AdminConsts.NEW_FILE),
            KeyboardButton(AdminConsts.SEE_ALL_FILES))
        markup.add(KeyboardButton(AdminConsts.BACK))
        return markup
    def gen_all_files_for_admin(all_files):
        # if all_files.count() > 28 : # bcs we can only show maximum 29 btns in telebot.ReplyKeyboardMarkup (and 1st btn is "BACK")
        #     # files = all_files[-29:-1]
        #     files = list(all_files[::-1][0:29])
        # else :
        #     files = all_files
        files = all_files[0:27]
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        count = files.count()
        markup.add(KeyboardButton(AdminConsts.BACK))
        for i in range(count) :
            markup.add(KeyboardButton(files[i].btn_text))
        return markup
    def gen_show_a_file_to_admin_markup(action, file_id):
        markup = InlineKeyboardMarkup(row_width=2)
        if action == "show" :
            markup.add(
                InlineKeyboardButton(text="حذف این فایل ❌", callback_data=f"deleteFile:tryDelete:{file_id}")
            )
        elif action == "delete_confirmation" :
            markup.add(
                InlineKeyboardButton(text="🚫 حدف نهایی 🚫", callback_data=f"deleteFile:finalDelete:{file_id}"),
                InlineKeyboardButton(text="نگه داشتن", callback_data=f"deleteFile:keep:{file_id}")
            )
        elif action == "deleted" :
            markup.add(InlineKeyboardButton(text="این فایل حذف شد", callback_data=f"grrrrrr!nothing!"))
        return markup
    def gen_cancel_reply_btn_markup():
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        markup.add(KeyboardButton("انصراف"))
        return markup
    def gen_markup_for_btn_ad(btn_type, btn_text, btn_link):
        markup = InlineKeyboardMarkup(row_width=1)
        if btn_type == AdminConsts.LINK_BTN :
            markup.add(InlineKeyboardButton(text=btn_text, url=btn_link))
        elif btn_type == AdminConsts.WEB_APP_BTN :
            markup.add(InlineKeyboardButton(text=btn_text, web_app=WebAppInfo(url=btn_link)))
        return markup
    def gen_send_btn_ad_to_all_users_or_cancel():
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        markup.add(KeyboardButton(AdminConsts.SEND_TO_ALL), KeyboardButton("بازگشت"))
        return markup
    def gen_choose_btn_format_to_create_markup():
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        markup.add(
        KeyboardButton(AdminConsts.LINK_BTN),
        KeyboardButton(AdminConsts.WEB_APP_BTN)
        )
        markup.add(KeyboardButton("بازگشت"))
        return markup

class UserMenus:
    def gen_majors_glass_btns():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(text='ریاضی 🧮', callback_data=f'set_major:0'),
            InlineKeyboardButton(text='تجربی 🧬', callback_data=f'set_major:1')
        )
        markup.add(
            InlineKeyboardButton(text='انسانی 👤', callback_data=f'set_major:2'),
            InlineKeyboardButton(text='هنر 🎭', callback_data=f'set_major:3')
        )
        markup.add(
            InlineKeyboardButton(text='سایر رشته ها 🎫', callback_data=f'set_major:4')
        )
        return markup
    def gen_editing_majors_glass_btns():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(text='ریاضی 🧮', callback_data=f'edit_major:0'),
            InlineKeyboardButton(text='تجربی 🧬', callback_data=f'edit_major:1')
        )
        markup.add(
            InlineKeyboardButton(text='انسانی 👤', callback_data=f'edit_major:2'),
            InlineKeyboardButton(text='هنر 🎭', callback_data=f'edit_major:3')
        )
        markup.add(
            InlineKeyboardButton(text='سایر رشته ها 🎫', callback_data=f'edit_major:4')
        )
        return markup
    def gen_grades_glass_btns():
        markup = InlineKeyboardMarkup(row_width=4)
        markup.add(
            InlineKeyboardButton(text="چهارم", callback_data=f'set_grade:4'),
            InlineKeyboardButton(text="سوم", callback_data=f'set_grade:3'),
            InlineKeyboardButton(text="دوم", callback_data=f'set_grade:2'),
            InlineKeyboardButton(text="اول", callback_data=f'set_grade:1'),
        )
        markup.add(
            InlineKeyboardButton(text="هشتم", callback_data=f'set_grade:8'),
            InlineKeyboardButton(text="هفتم", callback_data=f'set_grade:7'),
            InlineKeyboardButton(text="ششم", callback_data=f'set_grade:6'),
            InlineKeyboardButton(text="پنجم", callback_data=f'set_grade:5'),
        )
        markup.add(
            InlineKeyboardButton(text="دوازدهم", callback_data=f'set_grade:12'),
            InlineKeyboardButton(text="یازدهم", callback_data=f'set_grade:11'),
            InlineKeyboardButton(text="دهم", callback_data=f'set_grade:10'),
            InlineKeyboardButton(text="نهم", callback_data=f'set_grade:9'),
        )
        markup.add(
            InlineKeyboardButton(text="فارغ التحصیل", callback_data=f'set_grade:18'),
        )
        return markup
    def gen_editing_grades_glass_btns():
        markup = InlineKeyboardMarkup(row_width=4)
        markup.add(
            InlineKeyboardButton(text="چهارم", callback_data=f'edit_grade:4'),
            InlineKeyboardButton(text="سوم", callback_data=f'edit_grade:3'),
            InlineKeyboardButton(text="دوم", callback_data=f'edit_grade:2'),
            InlineKeyboardButton(text="اول", callback_data=f'edit_grade:1'),
        )
        markup.add(
            InlineKeyboardButton(text="هشتم", callback_data=f'edit_grade:8'),
            InlineKeyboardButton(text="هفتم", callback_data=f'edit_grade:7'),
            InlineKeyboardButton(text="ششم", callback_data=f'edit_grade:6'),
            InlineKeyboardButton(text="پنجم", callback_data=f'edit_grade:5'),
        )
        markup.add(
            InlineKeyboardButton(text="دوازدهم", callback_data=f'edit_grade:12'),
            InlineKeyboardButton(text="یازدهم", callback_data=f'edit_grade:11'),
            InlineKeyboardButton(text="دهم", callback_data=f'edit_grade:10'),
            InlineKeyboardButton(text="نهم", callback_data=f'edit_grade:9'),
        )
        markup.add(
            InlineKeyboardButton(text="فارغ التحصیل", callback_data=f'edit_grade:18'),
        )
        return markup
    def gen_main_menu(user):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(
            KeyboardButton(UserConsts.FILES_SECTION),
            KeyboardButton(UserConsts.MY_USER_DATA_BTN)
            )
        return markup
    def gen_edit_user_data_glass_menu(grade):
        markup = InlineKeyboardMarkup(row_width=2)
        if grade >= 9 :
            markup.add(InlineKeyboardButton(text="⚙️ ویرایش نام ⚙️", callback_data="edit_user_data:name"))
            markup.add(
                InlineKeyboardButton(text="⚙️ تغییر پایه ⚙️", callback_data="edit_user_data:grade"),
                InlineKeyboardButton(text="⚙️ تغییر رشته ⚙️", callback_data="edit_user_data:major")
            )
            markup.add(InlineKeyboardButton(text="بازگشت", callback_data="edit_user_data:back"))
        else :
            markup.add(
                InlineKeyboardButton(text="⚙️ تغییر پایه ⚙️", callback_data="edit_user_data:grade"),
                InlineKeyboardButton(text="⚙️ ویرایش نام ⚙️", callback_data="edit_user_data:name")
            )
            markup.add(InlineKeyboardButton(text="بازگشت", callback_data="edit_user_data:back"))
        return markup
    def gen_all_files_markup(all_files):
        count = all_files.count()
        markup = InlineKeyboardMarkup(row_width=1)
        for i in range(count) :
            markup.add(
                InlineKeyboardButton(text=all_files[i].btn_text, callback_data=f"user_show_file:{all_files[i].id}")
            )
        return markup