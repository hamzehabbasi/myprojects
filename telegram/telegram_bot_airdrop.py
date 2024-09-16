import telebot
from telebot import types

# توکن ربات تلگرام شما
bot = telebot.TeleBot("7316797697:AAEkspaYR33gMF6J9PCRD3rI6aY_qKS0agI")

CHANNEL_USERNAME = "@my_chan12"  # نام کاربری کانال شما

user_data = {}  # دیکشنری برای ذخیره داده‌های ورودی کاربران


@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()

    # دکمه عضویت در کانال
    join_channel_button = types.InlineKeyboardButton("عضویت در کانال", url="https://t.me/my_chan12")
    markup.add(join_channel_button)

    # دکمه تأیید عضویت
    confirm_membership_button = types.InlineKeyboardButton("تأیید عضویت در کانال", callback_data="confirm_membership")
    markup.add(confirm_membership_button)

    bot.reply_to(message, "به ربات ما خوش آمدید", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "confirm_membership")
def confirm_membership(call):
    user_id = call.from_user.id

    # پاسخ سریع به callback query برای جلوگیری از انقضا
    bot.answer_callback_query(call.id, "در حال بررسی عضویت شما...")

    try:
        # بررسی عضویت کاربر در کانال
        print(f"Checking membership for user: {user_id} in channel: {CHANNEL_USERNAME}")
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        member_status = member.status

        if member_status in ['member', 'administrator', 'creator']:
            bot.send_message(call.message.chat.id, "عضویت شما در کانال تایید شد. ممنون!")

            # ایجاد دکمه "برای ادامه کلیک کنید"
            markup = types.InlineKeyboardMarkup()
            continue_button = types.InlineKeyboardButton("برای ادامه کلیک کنید", callback_data="continue")
            markup.add(continue_button)

            bot.send_message(call.message.chat.id, "برای ادامه کلیک کنید:", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "شما عضو کانال ما نشده‌اید. لطفاً ابتدا در کانال عضو شوید.")

    except telebot.apihelper.ApiTelegramException as e:
        print(f"API Error: {e.description}")
        bot.send_message(call.message.chat.id, "شما عضو کانال ما نشده‌اید. لطفاً ابتدا در کانال عضو شوید.")

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        bot.send_message(call.message.chat.id, "یک خطای نامشخص رخ داده است. لطفاً بعداً دوباره تلاش کنید.")


@bot.callback_query_handler(func=lambda call: call.data == "continue")
def continue_process(call):
    bot.answer_callback_query(call.id, "شما ادامه را انتخاب کردید.")

    # ایجاد لیست دکمه‌ها
    buttons = [
        ("🐹hamster", "hamster"),
        ("🪙 تپ سواپ", "tapswap"),
        ("🍀 بلوم", "blum"),
        ("🪙 Cex", "cexio"),
        ("🪙 یس کوین", "yescoin"),
        ("🪙 تایم فارم", "time_farm"),
        ("⭐️ ماژور", "major"),
        ("🤨 داگز", "dogs"),
        ("🪙 ممفی", "mmfi"),
        ("🪙 بوم", "boom"),
        ("🤩 بامپ", "bump"),
        ("🤩 بولران", "bullrun"),
        ("🤑 ایسبرگ", "icpberg"),
        ("🤩 دایمور", "diamore")
    ]

    markup = types.InlineKeyboardMarkup()
    for text, callback_data in buttons:
        markup.add(types.InlineKeyboardButton(text, callback_data=callback_data))

    bot.send_message(call.message.chat.id, "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: call.data in ["hamster", "tapswap", "blum", "cexio", "yescoin", "time_farm", "major", "dogs",
                                    "mmfi", "boom", "bump", "bullrun", "icpberg", "diamore"])
def handle_option(call):
    user_data[call.from_user.id] = {"option": call.data}  # ذخیره انتخاب کاربر
    user_option = call.data

    if user_option == "hamster":
        user_data[call.from_user.id]["state"] = "awaiting_profit"
        bot.send_message(call.message.chat.id, "لطفاً پروفیت خود را وارد کنید:")
    elif user_option == "mmfi":
        user_data[call.from_user.id]["state"] = "awaiting_balance_mmfi"
        bot.send_message(call.message.chat.id, "لطفاً موجودی خود را وارد کنید:")
    else:
        user_data[call.from_user.id]["state"] = "awaiting_balance"
        bot.send_message(call.message.chat.id, "لطفاً موجودی خود را وارد کنید:")


@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("state") == "awaiting_profit")
def get_profit(message):
    try:
        profit = float(message.text)
        user_data[message.from_user.id]["profit"] = profit
        user_data[message.from_user.id]["state"] = "awaiting_token_balance"
        bot.send_message(message.chat.id, "لطفاً موجودی توکن خود را وارد کنید:")
    except ValueError:
        bot.send_message(message.chat.id, "لطفاً یک عدد معتبر وارد کنید.")


@bot.message_handler(
    func=lambda message: user_data.get(message.from_user.id, {}).get("state") == "awaiting_token_balance")
def get_token_balance(message):
    try:
        token_balance = float(message.text)
        user_data[message.from_user.id]["token_balance"] = token_balance
        user_data[message.from_user.id]["state"] = "awaiting_referrals"
        bot.send_message(message.chat.id, "لطفاً تعداد زیرمجموعه‌های خود را وارد کنید:")
    except ValueError:
        bot.send_message(message.chat.id, "لطفاً یک عدد معتبر وارد کنید.")


@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("state") == "awaiting_referrals")
def get_referrals(message):
    try:
        referrals = int(message.text)
        user_data[message.from_user.id]["referrals"] = referrals

        user_option = user_data[message.from_user.id]["option"]
        balance = user_data[message.from_user.id].get("balance", 0)
        profit = user_data[message.from_user.id].get("profit", 0)
        token_balance = user_data[message.from_user.id].get("token_balance", 0)
        referrals = user_data[message.from_user.id]["referrals"]
        total = 0

        if user_option == "hamster":
            calculated_profit = ((profit * 0.000001) ** 5) / 5
            calculated_token_balance = token_balance * 0.00000004
            total = calculated_profit + calculated_token_balance + referrals * 1
        elif user_option == "tapswap":
            total = (balance * 0.0000007) + (referrals * 0.1)
        elif user_option == "blum":
            total = (balance * 0.0008) + (referrals * 0.2)
        elif user_option == "cexio":
            total = (balance * 0.0007) + (referrals * 0.2)
        elif user_option == "yescoin":
            total = (balance * 0.000001) + (referrals * 1)
        elif user_option == "time_farm":
            total = (balance * 0.000001) + (referrals * 0.3)
        elif user_option == "major":
            total = (balance * 0.001) + (referrals * 0.2)
        elif user_option == "dogs":
            total = (balance * 0.001) + (referrals * 0.3)
        elif user_option == "boom":
            total = (balance * 0.0000002) + (referrals * 0.3)
        elif user_option == "bump":
            total = (balance * 0.00000003) + (referrals * 1)
        elif user_option == "bullrun":
            total = (balance / 3) + (referrals * 0.5)
        elif user_option == "icpberg":
            total = (balance * 0.0005) + (referrals * 0.2)
        elif user_option == "diamore":
            total = (balance * 0.001) + (referrals * 0.3)
        rial = total * 60000
        bot.send_message(message.chat.id, f"دارایی به دلار: : {int(total)}\n دارایی به ریال: {int(rial)}")

        # پاک کردن داده‌های کاربر
        del user_data[message.from_user.id]
    except ValueError:
        bot.send_message(message.chat.id, "لطفاً یک عددمعتبر وارد کنید.")


@bot.message_handler(
    func=lambda message: user_data.get(message.from_user.id, {}).get("state") == "awaiting_balance_mmfi")
def get_balance_mmfi(message):
    try:
        balance = float(message.text)
        user_data[message.from_user.id]["balance"] = balance
        bot.send_message(message.chat.id, "لطفاً تعداد زیرمجموعه‌های خود را وارد کنید:")
        user_data[message.from_user.id]["state"] = "awaiting_referrals"
    except ValueError:
        bot.send_message(message.chat.id, "لطفاً یک عدد معتبر وارد کنید.")


@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("state") == "awaiting_balance")
def get_balance(message):
    try:
        balance = float(message.text)
        user_data[message.from_user.id]["balance"] = balance
        user_data[message.from_user.id]["state"] = "awaiting_referrals"
        bot.send_message(message.chat.id, "لطفاً تعداد زیرمجموعه‌های خود را وارد کنید:")
    except ValueError:
        bot.send_message(message.chat.id, "لطفاً یک عدد معتبر وارد کنید.")


if __name__ == '__main__':
    print("Bot is polling...")
    bot.polling()
