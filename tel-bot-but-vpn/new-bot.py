import telebot
from telebot import types


# جایگزین کردن 'YOUR_TOKEN' با توکن ربات خود
bot = telebot.TeleBot('7474361966:AAH6vIJybv5EkU8MK63633Zt9e_qVsi65B8')


# تعریف لیست ادمین‌ها
admin_list = [6735104339]  # آیدی عددی ادمین‌ها
# تابعی برای مدیریت فرمان /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # ایجاد صفحه‌کلید پاسخ با طراحی بهینه و چشم‌نواز
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    # تعریف دکمه‌ها با استفاده از ایموجی‌های مناسب و مرتبط
    btn1 = types.KeyboardButton('🔄 تمدید سرویس')
    btn2 = types.KeyboardButton('🛒 خرید سرویس')
    btn3 = types.KeyboardButton('👤 حساب کاربری')
    btn4 = types.KeyboardButton('🆓 اکانت تست')
    btn5 = types.KeyboardButton('🏷 تعرفه‌ها')
    btn6 = types.KeyboardButton('🔥 سرویس‌ها')
    btn7 = types.KeyboardButton('👩‍🏭 پشتیبانی')
    btn8 = types.KeyboardButton('🔗 راهنمای اتصال')
    btn9 = types.KeyboardButton('🎁 دریافت هدیه')
    btn10 = types.KeyboardButton('🍎 اپل آیدی (مخزن)')

    # اضافه کردن دکمه‌ها به صفحه‌کلید به صورت مرتب و زیبا
    markup.add(btn2)  # اولین ردیف (تمدید سرویس، خرید سرویس)
    markup.add(btn1, btn4)  # دومین ردیف (حساب کاربری، اکانت تست)
    markup.add(btn3)  # دومین ردیف (حساب کاربری، اکانت تست)
    markup.add(btn5, btn6)  # سومین ردیف (تعرفه‌ها، سرویس‌ها)
    markup.add(btn7, btn8)  # چهارمین ردیف (پشتیبانی، راهنمای اتصال)
    markup.add(btn9, btn10) # پنجمین ردیف (هدیه ویژه، اپل آیدی)


    # چک کردن اینکه کاربر ادمین است یا خیر
    if message.from_user.id in admin_list:
        # دکمه مدیریت ربات که فقط برای ادمین نمایش داده می‌شود
        btn_admin = types.KeyboardButton('🛠 مدیریت ربات')
        markup.add(btn_admin)

    # ارسال پیام خوش‌آمدگویی به همراه منو
    bot.send_message(message.chat.id, "به ربات خوش آمدید! یکی از گزینه‌ها را انتخاب کنید:", reply_markup=markup)


# تابعی برای مدیریت کلیک روی دکمه '🛠 مدیریت ربات'
@bot.message_handler(func=lambda message: message.text == '🛠 مدیریت ربات' and message.from_user.id in admin_list)
def show_admin_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=4)

    # تعریف دکمه‌های مدیریتی با callback_data
    btn1 = types.InlineKeyboardButton('📢 اطلاع رسانی', callback_data='notify')
    btn2 = types.InlineKeyboardButton('🔌 پنل‌های پروتکل', callback_data='panel')
    btn3 = types.InlineKeyboardButton('💾 بکاپ گیری', callback_data='backup')
    btn4 = types.InlineKeyboardButton('💳 افزایش موجودی کاربر', callback_data='increase_balance')
    btn5 = types.InlineKeyboardButton('🔍 بررسی سرورها و محدودیت‌ها', callback_data='check_servers')
    btn6 = types.InlineKeyboardButton('🗑 حذف اکانت منقضی', callback_data='delete_expired')
    btn7 = types.InlineKeyboardButton('🎉 پیام خوش آمدگویی', callback_data='welcome_message')
    btn8 = types.InlineKeyboardButton('🎁 بخش هدیه', callback_data='gift_section')
    btn9 = types.InlineKeyboardButton('🛒 تنظیمات خرید', callback_data='purchase_settings')
    btn10 = types.InlineKeyboardButton('📝 تنظیمات ساخت اکانت', callback_data='account_settings')
    btn11 = types.InlineKeyboardButton('⛔ بن یا آزاد کردن کاربر', callback_data='ban_user')
    btn12 = types.InlineKeyboardButton('🔎 پیگیری کاربر', callback_data='track_user')
    btn13 = types.InlineKeyboardButton('👥 ادمین‌ها', callback_data='admins')
    btn14 = types.InlineKeyboardButton('⚙️ تغییر تنظیمات', callback_data='change_settings')
    btn15 = types.InlineKeyboardButton('🧪 تست کردن', callback_data='test')
    btn16 = types.InlineKeyboardButton('💰 تنظیمات موجودی', callback_data='balance_settings')
    btn17 = types.InlineKeyboardButton('📊 آمار بات', callback_data='bot_stats')
    btn18 = types.InlineKeyboardButton('📤 ارسال پیام گروهی', callback_data='send_group_message')
    btn19 = types.InlineKeyboardButton('📝 تنظیم متن‌ها', callback_data='edit_texts')
    btn20 = types.InlineKeyboardButton('⚡️ تغییر ظرفیت سرورها', callback_data='change_capacity')
    btn21 = types.InlineKeyboardButton('🚫 حذف از ربات/اضافه کردن', callback_data='add_remove')
    btn22 = types.InlineKeyboardButton('📬 ارسال پیام به کاربران خاص', callback_data='send_specific_message')
    btn23 = types.InlineKeyboardButton('🔒 محدودیت خرید', callback_data='purchase_limit')
    btn24 = types.InlineKeyboardButton('🌐 تغییر دامنه سرورها', callback_data='change_domain')
    btn25 = types.InlineKeyboardButton('🔧 تنظیمات ساخت اکانت سرور', callback_data='server_account_settings')

    # دکمه برگشت به منوی اصلی
    btn_back = types.InlineKeyboardButton('⬅️ برگشت', callback_data='back')

    # اضافه کردن دکمه‌های مدیریتی به منو
    markup.add(btn1, btn2, btn3)
    markup.add(btn4, btn5, btn6)

    markup.add(btn7, btn8, btn9)
    markup.add(btn10, btn11, btn12)
    markup.add(btn13, btn14, btn15)

    markup.add(btn16, btn17, btn18)
    markup.add(btn19, btn20, btn21)
    markup.add(btn22, btn23, btn24, btn25)
    markup.add(btn_back)

    # ارسال پیام منوی مدیریت به ادمین
    bot.send_message(message.chat.id, "🔧 منوی مدیریت:", reply_markup=markup)

# تابعی برای دکمه برگشت به منوی اصلی
@bot.message_handler(func=lambda message: message.text == '⬅️ برگشت' and message.from_user.id in admin_list)
def back_to_main_menu(message):
    send_welcome(message)  # برگشت به منوی اصلی


# تابعی برای مدیریت کلیک روی "خرید سرویس"
@bot.message_handler(func=lambda message: message.text == '🛒 خرید سرویس')
def service_purchase(message):
    # ایجاد دکمه‌های درون ربات (inline buttons)
    inline_markup = types.InlineKeyboardMarkup()

    # تعریف دکمه‌های پروتکل‌ها به صورت InlineKeyboardButton
    btn_v2ray = types.InlineKeyboardButton('v2ray', callback_data='v2ray')
    btn_ssh = types.InlineKeyboardButton('ssh', callback_data='ssh')
    btn_winguard = types.InlineKeyboardButton('winguard', callback_data='winguard')
    btn_openvpn = types.InlineKeyboardButton('openvpn', callback_data='openvpn')

    # اضافه کردن دکمه‌ها به صفحه‌کلید inline
    inline_markup.add(btn_v2ray)
    inline_markup.add(btn_ssh)
    inline_markup.add(btn_winguard)
    inline_markup.add(btn_openvpn)

    # ارسال پیام و نمایش دکمه‌های پروتکل‌ها به صورت inline
    bot.send_message(message.chat.id, "لطفاً پروتکل مورد نظر خود را انتخاب کنید:", reply_markup=inline_markup)


# تابعی برای مدیریت انتخاب پروتکل و نمایش گزینه‌های اشتراک
# تابعی برای مدیریت انتخاب پروتکل و نمایش گزینه‌های اشتراک برای v2ray
@bot.callback_query_handler(func=lambda call: call.data == 'v2ray')
def show_subscription_options_v2ray(call):
    # ایجاد دکمه‌های اشتراک به صورت InlineKeyboardButton
    subscription_markup = types.InlineKeyboardMarkup()

    # تعریف دکمه‌های اشتراک‌ها برای v2ray
    btn_1month = types.InlineKeyboardButton('اشتراک ۱ ماهه', callback_data='v2ray_1month')
    btn_2month = types.InlineKeyboardButton('اشتراک ۲ ماهه', callback_data='v2ray_2month')
    btn_3month = types.InlineKeyboardButton('اشتراک ۳ ماهه', callback_data='v2ray_3month')
    btn_4month = types.InlineKeyboardButton('اشتراک ۴ ماهه', callback_data='v2ray_4month')
    btn_5month = types.InlineKeyboardButton('اشتراک ۵ ماهه', callback_data='v2ray_5month')
    btn_6month = types.InlineKeyboardButton('اشتراک ۶ ماهه', callback_data='v2ray_6month')

    # تعریف دکمه برگشت
    btn_back = types.InlineKeyboardButton('⬅️ برگشت', callback_data='back_to_protocols')

    # اضافه کردن دکمه‌ها به صفحه‌کلید inline به صورت تک تک (زیر هم)
    subscription_markup.add(btn_1month)
    subscription_markup.add(btn_2month)
    subscription_markup.add(btn_3month)
    subscription_markup.add(btn_4month)
    subscription_markup.add(btn_5month)
    subscription_markup.add(btn_6month)
    subscription_markup.add(btn_back)  # دکمه برگشت

    # ارسال پیام و نمایش دکمه‌های اشتراک
    bot.edit_message_text("لطفاً اشتراک مورد نظر خود را انتخاب کنید:", chat_id=call.message.chat.id,
                          message_id=call.message.message_id, reply_markup=subscription_markup)


# تابعی برای مدیریت انتخاب اشتراک و نمایش گزینه‌های حجم و قیمت فقط برای v2ray
@bot.callback_query_handler(func=lambda call: call.data.startswith('v2ray_'))
def show_volume_options_v2ray(call):
    # استخراج مدت اشتراک از callback_data
    subscription_period = call.data.split('_')[1]

    # تنظیم ضریب قیمت‌ها بر اساس مدت اشتراک
    multipliers = {
        '1month': 1,
        '2month': 1.5,
        '3month': 2,
        '4month': 2.5,
        '5month': 3,
        '6month': 3.5
    }
    multiplier = multipliers[subscription_period]

    # ایجاد دکمه‌های حجم و قیمت‌ها به صورت InlineKeyboardButton
    volume_markup = types.InlineKeyboardMarkup()

    # تعریف دکمه‌های حجم و قیمت‌ها (قیمت‌ها بر اساس ضرب در ضریب)
    btn_10gb = types.InlineKeyboardButton(f'۱۰ گیگ - {int(10000 * multiplier)} تومان',
                                          callback_data=f'10gb_{subscription_period}')
    btn_20gb = types.InlineKeyboardButton(f'۲۰ گیگ - {int(15000 * multiplier)} تومان',
                                          callback_data=f'20gb_{subscription_period}')
    btn_30gb = types.InlineKeyboardButton(f'۳۰ گیگ - {int(25000 * multiplier)} تومان',
                                          callback_data=f'30gb_{subscription_period}')
    btn_50gb = types.InlineKeyboardButton(f'۵۰ گیگ - {int(40000 * multiplier)} تومان',
                                          callback_data=f'50gb_{subscription_period}')
    btn_unlimited = types.InlineKeyboardButton(f'نامحدود - {int(60000 * multiplier)} تومان',
                                               callback_data=f'unlimited_{subscription_period}')

    btn_back = types.InlineKeyboardButton('⬅️ برگشت', callback_data='back_to_protocols')

    # اضافه کردن دکمه‌ها به صفحه‌کلید inline به صورت تک تک (زیر هم)
    volume_markup.add(btn_10gb)
    volume_markup.add(btn_20gb)
    volume_markup.add(btn_30gb)
    volume_markup.add(btn_50gb)
    volume_markup.add(btn_unlimited)
    volume_markup.add(btn_back)
    # ارسال پیام و نمایش دکمه‌های حجم و قیمت
    bot.edit_message_text(text=f"لطفاً حجم {call.data}مورد نظر خود را انتخاب کنید:",
                      chat_id=call.message.chat.id,
                      message_id=call.message.message_id, reply_markup=volume_markup)

# تابعی برای مدیریت کلیک روی گزینه "برگشت" و بازگشت به صفحه پروتکل‌ها
@bot.callback_query_handler(func=lambda call: call.data == 'back_to_protocols')
def go_back_to_protocols(call):
    # ایجاد دکمه‌های درون ربات (inline buttons)
    inline_markup = types.InlineKeyboardMarkup()

    # تعریف دکمه‌های پروتکل‌ها به صورت InlineKeyboardButton
    btn_v2ray = types.InlineKeyboardButton('v2ray', callback_data='v2ray')
    btn_ssh = types.InlineKeyboardButton('ssh', callback_data='ssh')
    btn_winguard = types.InlineKeyboardButton('winguard', callback_data='winguard')
    btn_openvpn = types.InlineKeyboardButton('openvpn', callback_data='openvpn')

    # اضافه کردن دکمه‌ها به صفحه‌کلید inline
    inline_markup.add(btn_v2ray)
    inline_markup.add(btn_ssh)
    inline_markup.add(btn_winguard)
    inline_markup.add(btn_openvpn)

    # بازگشت به صفحه انتخاب پروتکل‌ها
    bot.edit_message_text("لطفاً پروتکل مورد نظر خود را انتخاب کنید:", chat_id=call.message.chat.id,
                          message_id=call.message.message_id, reply_markup=inline_markup)


# تابعی برای مدیریت انتخاب پروتکل‌های دیگر (ssh، winguard، openvpn) و نمایش گزینه‌های اشتراک
@bot.callback_query_handler(func=lambda call: call.data in ['ssh', 'winguard', 'openvpn'])
def show_subscription_options_other(call):
    subscription_markup = types.InlineKeyboardMarkup()

    try:
        # ایجاد دکمه‌های اشتراک به صورت InlineKeyboardButton
        # تعریف دکمه‌های اشتراک‌ها برای ssh، winguard و openvpn
        btn_1month = types.InlineKeyboardButton('اشتراک ۱ ماهه ۴۰ هزارتومان', callback_data=f'{call.data}_1month')
        btn_2month = types.InlineKeyboardButton('اشتراک ۲ ماهه ۸۰هزار تومان', callback_data=f'{call.data}_2month')
        btn_3month = types.InlineKeyboardButton('اشتراک ۳ ماهه۱۲۰هزارتومان', callback_data=f'{call.data}_3month')
        btn_4month = types.InlineKeyboardButton('اشتراک ۴ ماهه۱۶۰هزارتومان', callback_data=f'{call.data}_4month')
        btn_5month = types.InlineKeyboardButton('اشتراک ۵ ماهه۲۰۰هزارتومان', callback_data=f'{call.data}_5month')
        btn_6month = types.InlineKeyboardButton('۲۴۰هزارتومان اشتراک ۶ ماهه', callback_data=f'{call.data}_6month')

        # تعریف دکمه برگشت
        btn_back = types.InlineKeyboardButton('⬅️ برگشت', callback_data='back_to_protocols')

        # اضافه کردن دکمه‌ها به صفحه‌کلید inline به صورت تک تک (زیر هم)
        subscription_markup.add(btn_1month)
        subscription_markup.add(btn_2month)
        subscription_markup.add(btn_3month)
        subscription_markup.add(btn_4month)
        subscription_markup.add(btn_5month)
        subscription_markup.add(btn_6month)
        subscription_markup.add(btn_back)  # دکمه برگشت

        # ارسال پیام و نمایش دکمه‌های اشتراک
        bot.edit_message_text(f"لطفاً اشتراک {call.data} مورد نظر خود را انتخاب کنید:", chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=subscription_markup)
    except:
        bot.edit_message_text('در حال حاضر جواب گو نیست چندلحظه دیگر تلاش کنید.', chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=subscription_markup)

# # تابعی برای مدیریت انتخاب اشتراک (ssh، winguard، openvpn)
@bot.callback_query_handler(
    func=lambda call: call.data.endswith(('1month', '2month', '3month', '4month', '5month', '6month')))
def handle_subscription_choice(call):
    payment_markup = types.InlineKeyboardMarkup()

    # تعریف دکمه‌های پرداخت
    btn_card_payment = types.InlineKeyboardButton(' پرداخت با کارت💳', callback_data='card_payment')
    btn_wallet_payment = types.InlineKeyboardButton('پرداخت با کیف پول💰', callback_data='wallet_payment')
    btn_online_payment = types.InlineKeyboardButton('پرداخت آنلاین', callback_data='online_payment')
    btn_back = types.InlineKeyboardButton('⬅️ برگشت', callback_data='back_to_protocols')

    # اضافه کردن دکمه‌ها به صفحه‌کلید inline
    payment_markup.add(btn_card_payment)
    payment_markup.add(btn_wallet_payment)
    payment_markup.add(btn_online_payment)
    payment_markup.add(btn_back)

    # ویرایش پیام و نمایش دکمه‌های پرداخت
    bot.edit_message_text(text=f"لطفاً روش پرداخت اشتراک {call.data} را انتخاب کنید:",
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=payment_markup)

@bot.callback_query_handler(func=lambda call: call.data =='card_payment')
def pay_by_card(call):
    payment_markup = types.InlineKeyboardMarkup()

    btn_back = types.InlineKeyboardButton('⬅️ برگشت', callback_data='back_to_protocols')
    payment_markup.add(btn_back)

    bot.edit_message_text(text=f"لطفا حق اشتراک  را به کارت ۶۰۳۷۹۹۱۸ واریز کنید و رسید واریز را ارسال نمایید",
                             chat_id=call.message.chat.id,
                             message_id=call.message.message_id,
                             reply_markup=payment_markup)


# # مدیریت کلیک بر روی گزینه‌های پروتکل‌ها و قیمت‌های v2ray
# @bot.callback_query_handler(func=lambda call: call.data in ['10gb_1month', '20gb_1month', '30gb_1month', '50gb_1month', 'unlimited_1month',
#                                                            '10gb_2month', '20gb_2month', '30gb_2month', '50gb_2month', 'unlimited_2month',
#                                                            '10gb_3month', '20gb_3month', '30gb_3month', '50gb_3month', 'unlimited_3month',
#                                                            '10gb_4month', '20gb_4month', '30gb_4month', '50gb_4month', 'unlimited_4month',
#                                                            '10gb_5month', '20gb_5month', '30gb_5month', '50gb_5month', 'unlimited_5month',
#                                                            '10gb_6month', '20gb_6month', '30gb_6month', '50gb_6month', 'unlimited_6month',
#                                                            'ssh_1month', 'winguard_1month', 'openvpn_1month',
#                                                            'ssh_2month', 'winguard_2month', 'openvpn_2month',
#                                                            'ssh_3month', 'winguard_3month', 'openvpn_3month',
#                                                            'ssh_4month', 'winguard_4month', 'openvpn_4month',
#                                                            'ssh_5month', 'winguard_5month', 'openvpn_5month',
#                                                            'ssh_6month', 'winguard_6month', 'openvpn_6month'])
# def handle_subscription_selection(call):
#     # نمایش گزینه‌های پرداخت پس از انتخاب اشتراک یا قیمت
#     handle_subscription_choice(call)


# تابعی برای مدیریت کلیک روی "حساب کاربری "
@bot.message_handler(func=lambda message: message.text == '👤 حساب کاربری')
def service_purchase(message):
    # ایجاد دکمه‌های درون ربات (inline buttons)
    inline_markup = types.InlineKeyboardMarkup()

    # تعریف دکمه‌های پروتکل‌ها به صورت InlineKeyboardButton
    btn_balance = types.InlineKeyboardButton(' نمایش موجودی شما', callback_data='balance')
    btn_active_services = types.InlineKeyboardButton('سرویسهای فعال', callback_data='active_services')
    btn_invoice = types.InlineKeyboardButton('فاکتورها', callback_data='invoice')
    btn_user_ID = types.InlineKeyboardButton('آیدی عددی شما', callback_data='user_ID')
    btn_wallet = types.InlineKeyboardButton('کیف پول', callback_data='wallet')

    # اضافه کردن دکمه‌ها به صفحه‌کلید inline
    inline_markup.add(btn_balance)
    inline_markup.add(btn_active_services)
    inline_markup.add(btn_invoice)
    inline_markup.add(btn_user_ID)
    inline_markup.add(btn_wallet)

    # ارسال پیام و نمایش دکمه‌های پروتکل‌ها به صورت inline
    bot.send_message(message.chat.id, "لطفا گزینه مورد نظر خود را انتخاب کنید:", reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data == 'user_ID')
def show_user_id(call):
    user_id = call.from_user.id
    bot.send_message(call.message.chat.id, f"آیدی عددی شما: {user_id}")


# تابعی برای مدیریت کلیک روی "تمدید سرویس"
@bot.message_handler(func=lambda message: message.text == '🔄 تمدید سرویس')
def show_customer_services_button(message):
    # ایجاد صفحه کلید inline با دو دکمه: "سرویس‌های مشتری" و "برگشت"
    inline_markup = types.InlineKeyboardMarkup()
    btn_services = types.InlineKeyboardButton('📄 سرویس‌های مشتری', callback_data='customer_services')
    btn_back = types.InlineKeyboardButton('⬅️ برگشت', callback_data='back_to_main')

    inline_markup.add(btn_services)
    inline_markup.add(btn_back)

    bot.send_message(message.chat.id, "لطفاً گزینه مورد نظر خود را انتخاب کنید:", reply_markup=inline_markup)


# تابعی برای نمایش سرویس‌های مشتری
@bot.callback_query_handler(func=lambda call: call.data == 'customer_services')
def show_services_list(call):
    # شبیه‌سازی سرویس‌های مشتری (در اینجا فرضی)
    services = ['🔹 سرویس 1', '🔹 سرویس 2', '🔹 سرویس 3']  # می‌توانید سرویس‌های واقعی از دیتابیس بگیرید

    # ساخت دکمه‌ها برای لیست سرویس‌ها
    inline_markup = types.InlineKeyboardMarkup(row_width=2)

    for service in services:
        btn_service = types.InlineKeyboardButton(service, callback_data=f'service_{service}')
        inline_markup.add(btn_service)

    # دکمه برگشت
    btn_back = types.InlineKeyboardButton('⬅️ برگشت', callback_data='back_to_services')
    inline_markup.add(btn_back)

    # نمایش لیست سرویس‌ها به همراه دکمه‌های سرویس
    bot.edit_message_text("🔻 لیست سرویس‌های شما:", chat_id=call.message.chat.id, message_id=call.message.message_id,
                          reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
def show_service_options(call):
    service_name = call.data.split('_')[1]  # نام سرویس از callback_data استخراج می‌شود

    # ایجاد دکمه‌های مدیریتی برای هر سرویس به صورت دو ستونه
    inline_markup = types.InlineKeyboardMarkup(row_width=2)

    # تعریف دکمه‌های مدیریتی با ایموجی و چینش دو ستونه
    btn_extend = types.InlineKeyboardButton('🔄 تمدید ماهیانه', callback_data=f'extend_{service_name}')
    btn_delete = types.InlineKeyboardButton('❌ حذف سرویس', callback_data=f'delete_{service_name}')
    btn_change_password = types.InlineKeyboardButton('🔑 تغییر پسورد', callback_data=f'change_password_{service_name}')
    btn_change_link = types.InlineKeyboardButton('🔗 تغییر لینک دسترسی', callback_data=f'change_link_{service_name}')
    btn_service_info = types.InlineKeyboardButton('📄 مشخصات سرویس', callback_data=f'service_info_{service_name}')
    btn_account_balance = types.InlineKeyboardButton('💰 مانده حساب', callback_data=f'balance_{service_name}')
    btn_remaining_data = types.InlineKeyboardButton('📊 حجم باقیمانده', callback_data=f'remaining_data_{service_name}')

    # اضافه کردن دکمه‌ها به صورت دو ستونه (دو دکمه در هر ردیف)
    inline_markup.add(btn_extend, btn_delete)
    inline_markup.add(btn_change_password, btn_change_link)
    inline_markup.add(btn_service_info, btn_account_balance)
    inline_markup.add(btn_remaining_data)

    # دکمه برگشت به لیست سرویس‌ها
    btn_back = types.InlineKeyboardButton('⬅️ برگشت به سرویس‌ها', callback_data='customer_services')
    inline_markup.add(btn_back)

    # نمایش لیست اقدامات مدیریتی برای سرویس انتخاب شده با چینش دو ستونه
    bot.edit_message_text(f"🔻 مدیریت {service_name}:", chat_id=call.message.chat.id, message_id=call.message.message_id,
                          reply_markup=inline_markup)


# تابع برگشت به منوی اصلی
@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main')
def back_to_main_menu(call):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('🔄تمدید سرویس')
    btn2 = types.KeyboardButton('🛒خرید سرویس')
    btn3 = types.KeyboardButton('حساب کاربری')
    # سایر دکمه‌های منوی اصلی ...

    markup.add(btn1, btn2, btn3)
    bot.send_message(call.message.chat.id, "بازگشت به منوی اصلی:", reply_markup=markup)

# تابعی برای مدیریت کلیک روی "خرید سرویس"
@bot.message_handler(func=lambda message: message.text == '🆓 اکانت تست')
def service_purchase(message):
    # ایجاد دکمه‌های درون ربات (inline buttons)
    inline_markup = types.InlineKeyboardMarkup()

    # تعریف دکمه‌های پروتکل‌ها به صورت InlineKeyboardButton
    btn_v2ray = types.InlineKeyboardButton(' اکانت تست v2ray', callback_data='v2ray')
    btn_ssh = types.InlineKeyboardButton('اکانت تست ssh', callback_data='ssh')
    btn_winguard = types.InlineKeyboardButton('اکانت تست winguard', callback_data='winguard')
    btn_openvpn = types.InlineKeyboardButton('اکانت تست openvpn', callback_data='openvpn')

    # اضافه کردن دکمه‌ها به صفحه‌کلید inline
    inline_markup.add(btn_v2ray)
    inline_markup.add(btn_ssh)
    inline_markup.add(btn_winguard)
    inline_markup.add(btn_openvpn)

    # ارسال پیام و نمایش دکمه‌های پروتکل‌ها به صورت inline
    bot.send_message(message.chat.id, "لطفاً جهت فعال سازی اکانت تست ۲۴ ساعته‌‌ پروتکل مورد نظر خود را انتخاب کنید:", reply_markup=inline_markup)

# تابعی برای مدیریت کلیک روی "حساب کاربری "
@bot.message_handler(func=lambda message: message.text == '👤 حساب کاربری')
def service_purchase(message):
    # ایجاد دکمه‌های درون ربات (inline buttons)
    inline_markup = types.InlineKeyboardMarkup()

    # تعریف دکمه‌های پروتکل‌ها به صورت InlineKeyboardButton
    btn_balance = types.InlineKeyboardButton(' نمایش موجودی شما', callback_data='balance')
    btn_active_services = types.InlineKeyboardButton('سرویسهای فعال', callback_data='active_services')
    btn_invoice = types.InlineKeyboardButton('فاکتورها', callback_data='invoice')
    btn_user_ID = types.InlineKeyboardButton('آیدی عددی شما', callback_data='user_ID')
    btn_wallet = types.InlineKeyboardButton('کیف پول', callback_data='wallet')

    # اضافه کردن دکمه‌ها به صفحه‌کلید inline
    inline_markup.add(btn_balance)
    inline_markup.add(btn_active_services)
    inline_markup.add(btn_invoice)
    inline_markup.add(btn_user_ID)
    inline_markup.add(btn_wallet)

    # ارسال پیام و نمایش دکمه‌های پروتکل‌ها به صورت inline
    bot.send_message(message.chat.id, "لطفا گزینه مورد نظر خود را انتخاب کنید:", reply_markup=inline_markup)

@bot.callback_query_handler(func=lambda call: call.data == 'user_ID')
def show_user_id(call):
    user_id = call.from_user.id
    bot.send_message(call.message.chat.id, f"آیدی عددی شما: {user_id}")

# تابعی برای مدیریت کلیک روی "نمایش موجودی شما"
@bot.callback_query_handler(func=lambda call: call.data == 'balance')
def balance(call):
    # مقدار موجودی (به صورت فرضی صفر)
    balan = 0
    # ویرایش پیام اصلی برای نمایش موجودی
    bot.edit_message_text(text=f"موجودی کیف پول شما: {balan} هزار تومان می‌باشد",
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id)

    # شروع bot


# تابعی برای مدیریت کلیک روی '👩‍🏭 پشتیبانی'
@bot.message_handler(func=lambda message: message.text == '👩‍🏭 پشتیبانی')
def support_handler(message):
    # ایجاد دکمه‌های inline برای ارتباط با پشتیبانی
    inline_markup = types.InlineKeyboardMarkup(row_width=2)

    # تعریف دکمه‌ها
    btn_direct_contact = types.InlineKeyboardButton('📞 ارتباط مستقیم با ادمین', callback_data='direct_contact')
    btn_id_contact = types.InlineKeyboardButton('🆔 ارتباط از طریق آی‌دی', url='https://t.me/vtajook')
    btn_back = types.InlineKeyboardButton('⬅️ بازگشت', callback_data='back_to_menu')

    # اضافه کردن دکمه‌ها به صفحه‌کلید
    inline_markup.add(btn_id_contact,btn_direct_contact)
    # inline_markup.add(btn_id_contact)
    inline_markup.add(btn_back)

    # ارسال پیام و نمایش دکمه‌ها
    bot.send_message(
        message.chat.id,
        "برای ارتباط با پشتیبانی، یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=inline_markup
    )

# تابع برای مدیریت کلیک روی دکمه '📞 ارتباط مستقیم با ادمین'
@bot.callback_query_handler(func=lambda call: call.data == 'direct_contact')
def direct_contact_handler(call):
    # ارسال پیام به ادمین
    bot.send_message(call.message.chat.id, "برای ارتباط مستقیم با ادمین، پیام خود را ارسال کنید:")

    # تنظیم حالت انتظار برای دریافت پیام کاربر و ارسال آن به ادمین
    @bot.message_handler(func=lambda message: True)
    def forward_to_admin(message):
        admin_chat_id = "7270577718"  # آی‌دی چت ادمین را اینجا وارد کنید
        bot.forward_message(admin_chat_id, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "پیام شما به ادمین ارسال شد.")

# تابع برای مدیریت دکمه '⬅️ بازگشت'
@bot.callback_query_handler(func=lambda call: call.data == 'back_to_menu')
def back_to_menu(call):
    send_welcome(call.message)  # بازگشت به منوی اصلی

# توابع برای دریافت تعرفه‌های پروتکل‌ها

def get_v2ray_prices():
    return "1 ماهه: 40,000 تومان\n2 ماهه: 80,000 تومان\n3 ماهه: 120,000 تومان\n4 ماهه: 160,000 تومان\n5 ماهه: 200,000 تومان\n6 ماهه: 240,000 تومان"

def get_ssh_prices():
    return "1 ماهه: 50,000 تومان\n2 ماهه: 100,000 تومان\n3 ماهه: 150,000 تومان\n4 ماهه: 200,000 تومان\n5 ماهه: 250,000 تومان\n6 ماهه: 300,000 تومان"

def get_winguard_prices():
    return "1 ماهه: 60,000 تومان\n2 ماهه: 120,000 تومان\n3 ماهه: 180,000 تومان\n4 ماهه: 240,000 تومان\n5 ماهه: 300,000 تومان\n6 ماهه: 360,000 تومان"

def get_openvpn_prices():
    return "1 ماهه: 70,000 تومان\n2 ماهه: 140,000 تومان\n3 ماهه: 210,000 تومان\n4 ماهه: 280,000 تومان\n5 ماهه: 350,000 تومان\n6 ماهه: 420,000 تومان"

# مدیریت کلیک روی دکمه '🏷 تعرفه‌ها'
@bot.message_handler(func=lambda message: message.text == '🏷 تعرفه‌ها')
def show_tariffs(message):
    # دریافت قیمت‌ها از توابع مختلف
    v2ray_prices = get_v2ray_prices()
    ssh_prices = get_ssh_prices()
    winguard_prices = get_winguard_prices()
    openvpn_prices = get_openvpn_prices()

    # ساختن پیام نهایی برای ارسال به کاربر
    tariffs_message = (
        "💳 تعرفه‌های سرویس‌های ما:\n\n"
        "🔸 V2Ray:\n" + v2ray_prices + "\n\n"
        "🔸 SSH:\n" + ssh_prices + "\n\n"
        "🔸 Winguard:\n" + winguard_prices + "\n\n"
        "🔸 OpenVPN:\n" + openvpn_prices + "\n"
    )

    # ارسال پیام تعرفه‌ها به کاربر
    bot.send_message(message.chat.id, tariffs_message)


@bot.message_handler(func=lambda message: message.text == '🔗 راهنمای اتصال')
def show_connection_guide(message):
    # ایجاد دکمه‌های درون ربات (inline buttons)
    inline_markup = types.InlineKeyboardMarkup(row_width=2)

    # تعریف دکمه‌ها
    btn_software = types.InlineKeyboardButton('📱 نمایش نرم‌افزارها', callback_data='show_software')
    btn_tutorial_channel = types.InlineKeyboardButton('📺 کانال آموزش', url='https://t.me/my_chan12')  # لینک به کانال
    btn_back = types.InlineKeyboardButton('⬅️ برگشت', callback_data='back_to_main_menu')

    # اضافه کردن دکمه‌ها به صفحه‌کلید
    inline_markup.add(btn_software,btn_tutorial_channel)
    inline_markup.add(btn_back)

    # ارسال پیام به همراه دکمه‌ها
    bot.send_message(message.chat.id, "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=inline_markup)

# تابع برای مدیریت دکمه برگشت به منوی اصلی
@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main_menu')
def back_to_main_menu(call):
    send_welcome(call.message)  # بازگشت به تابع خوش‌آمدگویی و منوی اصلی

# تابعی برای مدیریت کلیک روی دکمه '🎁 دریافت هدیه'
@bot.message_handler(func=lambda message: message.text == '🎁 دریافت هدیه')
def show_gift_info(message):
    user_id = message.from_user.id

    # فرض کنید تابع get_invite_count() تعداد دعوت‌ها را برمی‌گرداند
    invite_count = get_invite_count(user_id)

    # ایجاد لینک دعوت (لینک تلگرام با استفاده از آیدی عددی کاربر)
    invite_link = f"https://t.me/EGN_VPN_bot?start={user_id}"

    # ساخت پیام هدیه
    gift_message = (
        "🎁 به ازای دعوت هر یک از دوستان خود به ربات 5000 تومان هدیه بگیرید.\n\n"
        f"📊 تعداد دعوت‌های شما: {invite_count}\n\n"
        f"🔗 لینک دعوت شما: {invite_link}"
    )

    # ایجاد دکمه بازگشت
    markup = types.InlineKeyboardMarkup()
    # ارسال پیام هدیه به کاربر
    bot.send_message(message.chat.id, gift_message, reply_markup=markup)

# تابع فرضی برای دریافت تعداد دعوت‌ها
def get_invite_count(user_id):
    # اینجا تعداد دعوت‌های کاربر را از دیتابیس بگیرید
    # برای مثال، فرض کنیم کاربر 3 دعوت داشته باشد:
    return 3

if __name__ == '__main__':
    print("Bot is polling...")
    bot.polling()

