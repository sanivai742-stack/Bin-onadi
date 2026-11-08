import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests

# আপনার বন্ধুর নতুন বটের টোকেন
API_TOKEN = '9027972676:AAFsDj4wBDZfU-gUEfr29umXPyU67wG7Mqk'
bot = telebot.TeleBot(API_TOKEN)

# NP Network API কনফিগারেশন
NP_API_BASE_URL = 'https://www.npnetworkbd.com/api/user'
NP_API_KEY = 'NP-6HXU732PNEATGVFM'

# ইউজার ব্যালেন্স ট্র্যাক করার ডিকশনারি
user_balances = {}

def get_user_balance(user_id):
    return user_balances.get(user_id, 0.0)

def add_user_balance(user_id, amount):
    current = user_balances.get(user_id, 0.0)
    user_balances[user_id] = round(current + amount, 2)

# মূল মেনু (নিচের স্থায়ী বাটন)
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("📞 Get Number"),
        KeyboardButton("🔍 Search Number"),
        KeyboardButton("🔥 Proxy/VPN"),
        KeyboardButton("👥 Refer"),
        KeyboardButton("🛡️ 2FA"),
        KeyboardButton("💰 Balance"),
        KeyboardButton("💬 Support"),
        KeyboardButton("💳 Withdrawal")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "✨ *Welcome to Number & OTP Service.*\n\n"
        "👇 Choose an option below to continue:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_menu())

# Get Number ক্লিক করলে সার্ভিস লিস্ট
@bot.message_handler(func=lambda message: message.text == "📞 Get Number")
def handle_get_number(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🇫 FB Forgot"),
        KeyboardButton("🇫 Facebook"),
        KeyboardButton("📸 Instagram"),
        KeyboardButton("📱 WhatsApp"),
        KeyboardButton("🏠 Home")
    )
    bot.send_message(message.chat.id, "📍 *Select a service:*", parse_mode="Markdown", reply_markup=markup)

# সার্ভিস সিলেক্ট করার পর কান্ট্রি লিস্ট (Italy, Franceসহ অন্যান্য দেশ)
@bot.message_handler(func=lambda message: message.text in ["🇫 FB Forgot", "🇫 Facebook", "📸 Instagram", "📱 WhatsApp"])
def handle_service_selection(message):
    service_name = message.text.split(' ')[1]
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton(f"🇮🇹 Italy - {service_name}"),
        KeyboardButton(f"🇫🇷 France - {service_name}"),
        KeyboardButton(f"🇨🇲 Cameroon - {service_name}"),
        KeyboardButton(f"🇪🇹 Ethiopia - {service_name}"),
        KeyboardButton(f"🇹🇯 Tajikistan - {service_name}"),
        KeyboardButton("🔙 Back"),
        KeyboardButton("🏠 Home")
    )
    bot.send_message(message.chat.id, f"🌐 *Select a country for {service_name}:*", parse_mode="Markdown", reply_markup=markup)

# সঠিক কান্ট্রি অনুযায়ী API থেকে নাম্বার ফেচ করা
@bot.message_handler(func=lambda message: any(c in message.text for c in ["Italy", "France", "Cameroon", "Ethiopia", "Tajikistan", "Change Number"]))
def handle_number_generation(message):
    text_input = message.text
    
    country_name = "Unknown"
    country_code = "IT"
    if "Italy" in text_input:
        country_name = "Italy"
        country_code = "IT"
    elif "France" in text_input:
        country_name = "France"
        country_code = "FR"
    elif "Cameroon" in text_input:
        country_name = "Cameroon"
        country_code = "CM"
    elif "Ethiopia" in text_input:
        country_name = "Ethiopia"
        country_code = "ET"
    elif "Tajikistan" in text_input:
        country_name = "Tajikistan"
        country_code = "TJ"

    phone_number = "+393201234567" # ফলব্যাক বা ডেমো নম্বর
    
    try:
        api_url = f"{NP_API_BASE_URL}?key={NP_API_KEY}&action=getNumber&country={country_code}"
        response = requests.get(api_url, timeout=5)
        data = response.json()
        if 'number' in data:
            phone_number = data['number']
    except Exception as e:
        print(f"API Error: {e}")

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        KeyboardButton(f"📋 {phone_number}"),
        KeyboardButton("🔄 Check / Simulate OTP Received"),
        KeyboardButton("🔄 Change Number"),
        KeyboardButton("🏠 Home")
    )
    
    text = (
        f"🔴 *Country : {country_name}*\n\n"
        f"🔄 *Status: Waiting for OTP...*\n\n"
        f"📱 *Number:* `{phone_number}`\n\n"
        f"*(ওটিপি আসার জন্য অপেক্ষা করুন অথবা নিচের চেক বাটনে ক্লিক করুন)*"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

# OTP Received হওয়ার পরে কেবল ব্যালেন্সে ০.১ টাকা যোগ হওয়া
@bot.message_handler(func=lambda message: message.text == "🔄 Check / Simulate OTP Received")
def handle_otp_received(message):
    user_id = message.from_user.id
    
    add_user_balance(user_id, 0.1)
    current_balance = get_user_balance(user_id)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        KeyboardButton("🔄 Change Number"),
        KeyboardButton("🏠 Home")
    )
    
    text = (
        f"🔔 *New OTP Received!*\n\n"
        f"📩 *Code:* `482910`\n\n"
        f"💰 *You have earned 0.1 tk* (Total Balance: `{current_balance} tk`)"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

# ব্যালেন্স চেক
@bot.message_handler(func=lambda message: message.text == "💰 Balance")
def handle_balance(message):
    user_id = message.from_user.id
    balance = get_user_balance(user_id)
    text = f"💰 *Account Balance:*\nআপনার বর্তমান ব্যালেন্স: `{balance} TK`"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_menu())

# অন্যান্য কমন মেনু
@bot.message_handler(func=lambda message: message.text in ["🏠 Home", "🔙 Back", "🔍 Search Number", "🔥 Proxy/VPN", "👥 Refer", "🛡️ 2FA", "💬 Support", "💳 Withdrawal"])
def handle_other_menus(message):
    txt = message.text
    if txt in ["🏠 Home", "🔙 Back"]:
        bot.send_message(message.chat.id, "🏡 মূল মেনুতে ফিরে এসেছেন:", reply_markup=get_main_menu())
    elif txt == "💬 Support":
        bot.send_message(message.chat.id, "💬 যেকোনো সহায়তার জন্য আমাদের সাপোর্টে যোগাযোগ করুন।", reply_markup=get_main_menu())
    elif txt == "👥 Refer":
        bot.send_message(message.chat.id, "👥 আপনার রেফারেল লিংক শেয়ার করে আয় করুন!", reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, f"📌 *{txt}* অপশনটি সিলেক্ট করা হয়েছে।", parse_mode="Markdown", reply_markup=get_main_menu())

if __name__ == '__main__':
    print("Friend's Bot is running successfully...")
    bot.infinity_polling()