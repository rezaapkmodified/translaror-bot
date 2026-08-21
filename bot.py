"""
Glass Translator Bot - نسخه کامل با مدیریت استیکر برای Railway
"""

import os
import requests
import json
import time
import sys
from datetime import datetime

# ============================================
# CONFIGURATION - دریافت توکن از محیط
# ============================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ خطا: BOT_TOKEN تنظیم نشده است!")
    sys.exit(1)

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ============================================
# لیست ادمین‌ها
# ============================================
ADMINS = [7699447054]  # آیدی خود را وارد کنید

# ============================================
# STICKER CONFIGURATION
# ============================================
WELCOME_STICKER = "CAACAgIAAxkBAAEBBBBkZGVhZCBzdGlja2Vy"
SAVED_STICKERS = {
    "default": "CAACAgIAAxkBAAEBBBBkZGVhZCBzdGlja2Vy",
    "welcome": "CAACAgIAAxkBAAEBBBBkZGVhZCBzdGlja2Vy",
}

# ============================================
# GOOGLE TRANSLATE
# ============================================
def translate_text(text, to_lang='en', from_lang='fa'):
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": from_lang,
            "tl": to_lang,
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if response.status_code == 200 and data:
            translated = ""
            for item in data[0]:
                if item[0]:
                    translated += item[0]
            return translated
        return None
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def detect_language(text):
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "en",
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if response.status_code == 200 and data:
            return data[2]
        return None
    except Exception as e:
        print(f"Language detection error: {e}")
        return None

# ============================================
# TELEGRAM API FUNCTIONS
# ============================================
def send_sticker(chat_id, sticker_id):
    """ارسال استیکر به کاربر"""
    url = f"{API_URL}/sendSticker"
    payload = {"chat_id": chat_id, "sticker": sticker_id}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error sending sticker: {e}")
        return None

def send_message(chat_id, text, keyboard=None, parse_mode="HTML"):
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if keyboard:
        payload["reply_markup"] = json.dumps(keyboard)
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def send_chat_action(chat_id, action="typing"):
    url = f"{API_URL}/sendChatAction"
    payload = {"chat_id": chat_id, "action": action}
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def answer_callback(callback_id, text=None):
    url = f"{API_URL}/answerCallbackQuery"
    payload = {"callback_query_id": callback_id}
    if text:
        payload["text"] = text
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def get_user_info(user_id):
    url = f"{API_URL}/getChat"
    params = {"chat_id": user_id}
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        if data.get("ok"):
            return data["result"]
        return None
    except:
        return None

def get_lang_name(code):
    for name, c in LANGUAGES.items():
        if c == code:
            return name
    return code

# ============================================
# LANGUAGES & THEMES
# ============================================
LANGUAGES = {
    "🇺🇸 English": "en",
    "🇮🇷 فارسی": "fa",
    "🇩🇪 Deutsch": "de",
    "🇫🇷 Français": "fr",
    "🇪🇸 Español": "es",
    "🇮🇹 Italiano": "it",
    "🇯🇵 日本語": "ja",
    "🇨🇳 中文": "zh-cn",
    "🇷🇺 Русский": "ru",
    "🇹🇷 Türkçe": "tr",
    "🇦🇪 العربية": "ar",
}

THEMES = {
    "default": {
        "name": "پیش‌فرض",
        "emoji": "🌈",
        "primary_style": "primary",
        "success_style": "success",
        "danger_style": "danger",
        "emoji_set": {
            "translate": "🌍",
            "swap": "🔄",
            "auto": "🤖",
            "theme": "🎨",
            "audio": "🎤",
            "help": "📖",
            "creator": "👤",
            "sticker": "📱"
        }
    },
    "dark": {
        "name": "تاریک",
        "emoji": "🌙",
        "primary_style": "primary",
        "success_style": "success",
        "danger_style": "danger",
        "emoji_set": {
            "translate": "🌑",
            "swap": "🔀",
            "auto": "⚡",
            "theme": "🌌",
            "audio": "🎵",
            "help": "❓",
            "creator": "⭐",
            "sticker": "📱"
        }
    },
    "ocean": {
        "name": "اقیانوسی",
        "emoji": "🌊",
        "primary_style": "primary",
        "success_style": "success",
        "danger_style": "danger",
        "emoji_set": {
            "translate": "🐠",
            "swap": "🐙",
            "auto": "🐬",
            "theme": "🏖️",
            "audio": "🎶",
            "help": "🧜",
            "creator": "⚓",
            "sticker": "📱"
        }
    },
    "sunset": {
        "name": "غروب",
        "emoji": "🌅",
        "primary_style": "primary",
        "success_style": "success",
        "danger_style": "danger",
        "emoji_set": {
            "translate": "☀️",
            "swap": "🌤️",
            "auto": "⭐",
            "theme": "🎆",
            "audio": "🎸",
            "help": "🌇",
            "creator": "🌠",
            "sticker": "📱"
        }
    },
    "forest": {
        "name": "جنگل",
        "emoji": "🌳",
        "primary_style": "primary",
        "success_style": "success",
        "danger_style": "danger",
        "emoji_set": {
            "translate": "🌿",
            "swap": "🦋",
            "auto": "🐝",
            "theme": "🍃",
            "audio": "🐦",
            "help": "🦉",
            "creator": "🌺",
            "sticker": "📱"
        }
    }
}

# ============================================
# DATA STORAGE
# ============================================
user_preferences = {}
user_stats = {}
user_themes = {}
blocked_users = {}
last_update_id = 0
admin_states = {}

# ============================================
# KEYBOARDS
# ============================================
def create_main_menu(chat_id=None):
    theme_name = user_themes.get(chat_id, 'default') if chat_id else 'default'
    theme = THEMES.get(theme_name, THEMES['default'])
    emojis = theme["emoji_set"]
    
    keyboard = {
        "inline_keyboard": [
            [
                {"text": f"{emojis['translate']} مبدأ", "callback_data": "show_src", "style": theme["primary_style"]},
                {"text": f"{emojis['translate']} مقصد", "callback_data": "show_dest", "style": theme["success_style"]}
            ],
            [
                {"text": f"{emojis['swap']} تعویض", "callback_data": "swap", "style": theme["primary_style"]},
                {"text": f"{emojis['auto']} خودکار", "callback_data": "auto", "style": theme["success_style"]}
            ],
            [
                {"text": f"{emojis['theme']} تم", "callback_data": "show_themes", "style": theme["primary_style"]},
                {"text": f"{emojis['audio']} صوتی", "callback_data": "audio_help", "style": theme["success_style"]}
            ],
            [
                {"text": f"{emojis['help']} راهنما", "callback_data": "help", "style": theme["primary_style"]},
                {"text": f"{emojis['creator']} سازنده", "callback_data": "creator", "style": theme["danger_style"]}
            ]
        ]
    }
    return keyboard

def create_admin_panel():
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "📊 آمار", "callback_data": "admin_stats", "style": "primary"},
                {"text": "👥 کاربران", "callback_data": "admin_users", "style": "success"}
            ],
            [
                {"text": "📱 استیکر", "callback_data": "admin_sticker", "style": "primary"},
                {"text": "🚫 مسدود", "callback_data": "admin_blocked", "style": "danger"}
            ],
            [
                {"text": "🔙 بازگشت", "callback_data": "back_to_menu", "style": "primary"}
            ]
        ]
    }
    return keyboard

def create_sticker_admin_panel():
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "📱 استیکر فعلی", "callback_data": "admin_sticker_current", "style": "primary"},
                {"text": "📤 تغییر", "callback_data": "admin_sticker_change", "style": "success"}
            ],
            [
                {"text": "📋 لیست", "callback_data": "admin_sticker_list", "style": "primary"},
                {"text": "🔄 پیش‌فرض", "callback_data": "admin_sticker_reset", "style": "danger"}
            ],
            [
                {"text": "🔙 بازگشت", "callback_data": "admin_panel", "style": "primary"}
            ]
        ]
    }
    return keyboard

def create_theme_keyboard():
    keyboard = []
    row = []
    for theme_key, theme_data in THEMES.items():
        row.append({
            "text": f"{theme_data['emoji']} {theme_data['name']}",
            "callback_data": f"theme_{theme_key}",
            "style": "primary"
        })
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([
        {"text": "🔙 بازگشت", "callback_data": "back_to_menu", "style": "primary"}
    ])
    return {"inline_keyboard": keyboard}

def create_language_keyboard(lang_type="src"):
    keyboard = []
    row = []
    styles = ["primary", "success", "danger", "primary", "success", "danger", 
              "primary", "success", "danger", "primary", "success"]
    for i, (lang_name, lang_code) in enumerate(LANGUAGES.items()):
        style = styles[i % len(styles)]
        row.append({
            "text": lang_name,
            "callback_data": f"lang_{lang_code}_{lang_type}",
            "style": style
        })
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([
        {"text": "🔙 بازگشت", "callback_data": "back_to_menu", "style": "primary"}
    ])
    return {"inline_keyboard": keyboard}

# ============================================
# HANDLERS
# ============================================
def is_admin(user_id):
    return user_id in ADMINS

def handle_start(chat_id, first_name):
    # مقداردهی اولیه
    if chat_id not in user_preferences:
        user_preferences[chat_id] = {"src": "fa", "dest": "en"}
    if chat_id not in user_stats:
        user_stats[chat_id] = 0
    if chat_id not in user_themes:
        user_themes[chat_id] = 'default'
    
    if chat_id in blocked_users:
        send_message(chat_id, "🚫 شما مسدود شده‌اید.")
        return
    
    # ارسال استیکر خوش‌آمدگویی
    send_chat_action(chat_id, "typing")
    send_sticker(chat_id, WELCOME_STICKER)
    
    theme_name = user_themes.get(chat_id, 'default')
    theme = THEMES.get(theme_name, THEMES['default'])
    
    if is_admin(chat_id):
        welcome = (
            f"🌟 <b>سلام ادمین {first_name}!</b>\n\n"
            f"👑 شما دسترسی مدیریت دارید.\n"
            f"🎨 تم: {theme['emoji']} {theme['name']}\n"
            f"📱 استیکر: {WELCOME_STICKER[:20]}...\n"
            f"🌍 {len(LANGUAGES)} زبان\n\n"
            f"💡 برای مدیریت استیکر از پنل ادمین استفاده کنید."
        )
        admin_keyboard = {
            "inline_keyboard": [
                [{"text": "👑 پنل مدیریت", "callback_data": "admin_panel", "style": "danger"}],
                [{"text": "🔙 منوی کاربری", "callback_data": "user_menu", "style": "primary"}]
            ]
        }
        send_message(chat_id, welcome, admin_keyboard)
    else:
        welcome = (
            f"🌟 <b>سلام {first_name}!</b>\n\n"
            f"✨ <b>به Glass Translator خوش آمدید</b>\n"
            f"🌍 {len(LANGUAGES)} زبان\n\n"
            f"📝 متن خود را ارسال کنید."
        )
        send_message(chat_id, welcome, create_main_menu(chat_id))

# ============================================
# مدیریت استیکر
# ============================================
def handle_sticker_admin(chat_id, action):
    global WELCOME_STICKER
    
    if action == "current":
        send_message(chat_id, f"📱 <b>استیکر فعلی:</b>\n\n<code>{WELCOME_STICKER}</code>")
        send_sticker(chat_id, WELCOME_STICKER)
        send_message(chat_id, "⬆️ استیکر بالا استیکر فعلی است.", create_sticker_admin_panel())
    
    elif action == "change":
        admin_states[chat_id] = "waiting_for_sticker"
        send_message(
            chat_id,
            "📤 <b>ارسال استیکر جدید</b>\n\n"
            "لطفاً یک استیکر جدید ارسال کنید.",
            create_sticker_admin_panel()
        )
    
    elif action == "list":
        list_text = "📋 <b>لیست استیکرها</b>\n\n"
        for name, sticker_id in SAVED_STICKERS.items():
            list_text += f"• {name}: <code>{sticker_id}</code>\n"
        send_message(chat_id, list_text, create_sticker_admin_panel())
    
    elif action == "reset":
        WELCOME_STICKER = SAVED_STICKERS["default"]
        send_message(
            chat_id,
            f"✅ استیکر به پیش‌فرض بازنشانی شد!",
            create_sticker_admin_panel()
        )

def handle_new_sticker(chat_id, sticker_file_id):
    global WELCOME_STICKER
    WELCOME_STICKER = sticker_file_id
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    SAVED_STICKERS[f"custom_{timestamp}"] = sticker_file_id
    admin_states.pop(chat_id, None)
    send_message(chat_id, "✅ استیکر تغییر کرد!", create_sticker_admin_panel())
    send_sticker(chat_id, sticker_file_id)

def handle_sticker_message(chat_id, sticker_file_id):
    if is_admin(chat_id) and admin_states.get(chat_id) == "waiting_for_sticker":
        handle_new_sticker(chat_id, sticker_file_id)
    else:
        send_message(chat_id, "🙂 استیکر زیبایی!", create_main_menu(chat_id))

def handle_translation(chat_id, text):
    if chat_id in blocked_users:
        send_message(chat_id, "🚫 شما مسدود شده‌اید.")
        return
    
    if admin_states.get(chat_id) == "waiting_for_sticker":
        send_message(chat_id, "⚠️ لطفاً یک استیکر ارسال کنید، نه متن.")
        return
    
    user_stats[chat_id] = user_stats.get(chat_id, 0) + 1
    
    prefs = user_preferences.get(chat_id, {"src": "fa", "dest": "en"})
    src = prefs.get("src", "fa")
    dest = prefs.get("dest", "en")
    
    send_chat_action(chat_id, "typing")
    
    if src == "auto":
        detected = detect_language(text)
        if detected and detected != "auto":
            src_name = get_lang_name(detected)
        else:
            src_name = "ناشناخته"
        
        translated = translate_text(text, dest, "auto")
        if translated:
            response = f"🌍 <b>ترجمه خودکار</b>\n\n🔍 زبان: {src_name}\n\n<code>{translated}</code>"
        else:
            response = "❌ خطا در ترجمه"
    else:
        translated = translate_text(text, dest, src)
        if translated:
            response = (
                f"🔄 <b>از {get_lang_name(src)} به {get_lang_name(dest)}</b>\n\n"
                f"📝 <b>متن اصلی:</b>\n<code>{text}</code>\n\n"
                f"⬇️ <b>ترجمه:</b>\n<code>{translated}</code>"
            )
        else:
            response = "❌ خطا در ترجمه"
    
    send_message(chat_id, response, create_main_menu(chat_id))

def handle_theme_change(chat_id, theme_key):
    if theme_key in THEMES:
        user_themes[chat_id] = theme_key
        theme = THEMES[theme_key]
        send_message(
            chat_id,
            f"✅ <b>تم با موفقیت تغییر کرد!</b>\n\n🎨 {theme['emoji']} {theme['name']}",
            create_main_menu(chat_id)
        )

def handle_help(chat_id):
    help_text = (
        f"📖 <b>راهنمای ربات</b>\n\n"
        f"🌍 {len(LANGUAGES)} زبان\n"
        f"🎨 {len(THEMES)} تم\n\n"
        f"1️⃣ انتخاب زبان\n"
        f"2️⃣ ارسال متن"
    )
    send_message(chat_id, help_text, create_main_menu(chat_id))

def handle_audio_help(chat_id):
    help_text = (
        "🎤 <b>ترجمه صوتی</b>\n\n"
        "فایل صوتی خود را ارسال کنید.\n"
        "ربات متن را تشخیص داده و ترجمه می‌کند."
    )
    send_message(chat_id, help_text, create_main_menu(chat_id))

# ============================================
# ADMIN FUNCTIONS
# ============================================
def admin_stats():
    total_users = len(user_stats)
    total_translations = sum(user_stats.values())
    active_users = len([u for u in user_stats if user_stats[u] > 0])
    blocked = len(blocked_users)
    
    stats_text = (
        f"📊 <b>آمار کلی</b>\n\n"
        f"👥 کاربران: {total_users}\n"
        f"🟢 فعال: {active_users}\n"
        f"📝 ترجمه‌ها: {total_translations}\n"
        f"🚫 مسدود: {blocked}\n"
        f"🌍 زبان‌ها: {len(LANGUAGES)}\n"
        f"📱 استیکر: {WELCOME_STICKER[:20]}..."
    )
    return stats_text

# ============================================
# MAIN
# ============================================
def main():
    global last_update_id
    
    print("╔════════════════════════════════════════╗")
    print("║    🌍 GLASS TRANSLATOR BOT       🌍    ║")
    print("║   📱 با مدیریت استیکر                ║")
    print("║   ✅ ترجمه با Google Translate        ║")
    print("╚════════════════════════════════════════╝")
    print()
    
    # تست اتصال
    try:
        test_response = requests.get(f"{API_URL}/getMe", timeout=10)
        test_data = test_response.json()
        if test_data.get("ok"):
            print(f"✅ ربات متصل شد! @{test_data['result']['username']}")
            print(f"📱 استیکر فعلی: {WELCOME_STICKER[:20]}...")
            print(f"🌍 تعداد زبان‌ها: {len(LANGUAGES)}")
        else:
            print("❌ توکن نامعتبر!")
            return
    except Exception as e:
        print(f"❌ خطا: {e}")
        return
    
    print("\n🔄 ربات در حال اجراست...")
    print("=" * 50)
    
    try:
        while True:
            url = f"{API_URL}/getUpdates"
            params = {
                "offset": last_update_id + 1,
                "timeout": 30,
                "allowed_updates": ["message", "callback_query"]
            }
            
            response = requests.get(url, params=params, timeout=35)
            data = response.json()
            
            if data.get("ok") and data.get("result"):
                for update in data["result"]:
                    last_update_id = update["update_id"]
                    
                    if "message" in update:
                        message = update["message"]
                        chat_id = message["chat"]["id"]
                        first_name = message["from"].get("first_name", "User")
                        
                        if "text" in message:
                            text = message["text"]
                            print(f"📨 پیام از {first_name}: {text[:30]}...")
                            
                            if text == "/start":
                                handle_start(chat_id, first_name)
                            elif text == "/help":
                                handle_help(chat_id)
                            elif text.startswith("/"):
                                send_message(chat_id, "❌ دستور نامعتبر", create_main_menu(chat_id))
                            else:
                                handle_translation(chat_id, text)
                        
                        elif "sticker" in message:
                            sticker_file_id = message["sticker"]["file_id"]
                            sticker_emoji = message["sticker"].get("emoji", "")
                            print(f"📱 استیکر از {first_name}: {sticker_emoji}")
                            handle_sticker_message(chat_id, sticker_file_id)
                    
                    elif "callback_query" in update:
                        callback = update["callback_query"]
                        chat_id = callback["message"]["chat"]["id"]
                        data = callback["data"]
                        
                        print(f"🔘 کلیک دکمه: {data}")
                        answer_callback(callback["id"])
                        
                        # ========================
                        # CALLBACK HANDLERS
                        # ========================
                        
                        # Admin Panel
                        if data == "admin_panel" and is_admin(chat_id):
                            send_message(chat_id, "👑 پنل مدیریت", create_admin_panel())
                        
                        elif data == "user_menu":
                            send_message(chat_id, "🔙 منوی کاربری", create_main_menu(chat_id))
                        
                        # Sticker Admin
                        elif data == "admin_sticker" and is_admin(chat_id):
                            send_message(
                                chat_id,
                                "📱 <b>مدیریت استیکر خوش‌آمدگویی</b>\n\n"
                                f"استیکر فعلی: <code>{WELCOME_STICKER}</code>",
                                create_sticker_admin_panel()
                            )
                        
                        elif data == "admin_sticker_current" and is_admin(chat_id):
                            handle_sticker_admin(chat_id, "current")
                        
                        elif data == "admin_sticker_change" and is_admin(chat_id):
                            handle_sticker_admin(chat_id, "change")
                        
                        elif data == "admin_sticker_list" and is_admin(chat_id):
                            handle_sticker_admin(chat_id, "list")
                        
                        elif data == "admin_sticker_reset" and is_admin(chat_id):
                            handle_sticker_admin(chat_id, "reset")
                        
                        # Themes
                        elif data == "show_themes":
                            current_theme = user_themes.get(chat_id, 'default')
                            theme_name = THEMES.get(current_theme, THEMES['default'])['name']
                            theme_emoji = THEMES.get(current_theme, THEMES['default'])['emoji']
                            send_message(
                                chat_id,
                                f"🎨 <b>انتخاب تم</b>\n\nتم فعلی: {theme_emoji} {theme_name}",
                                create_theme_keyboard()
                            )
                        
                        elif data.startswith("theme_"):
                            theme_key = data.replace("theme_", "")
                            handle_theme_change(chat_id, theme_key)
                        
                        elif data == "audio_help":
                            handle_audio_help(chat_id)
                        
                        # Language selection
                        elif data == "show_src":
                            send_message(chat_id, "🌍 انتخاب مبدأ:", create_language_keyboard("src"))
                        
                        elif data == "show_dest":
                            send_message(chat_id, "🌍 انتخاب مقصد:", create_language_keyboard("dest"))
                        
                        elif data.startswith("lang_"):
                            parts = data.split("_")
                            lang_code = parts[1]
                            lang_type = parts[2]
                            
                            if chat_id not in user_preferences:
                                user_preferences[chat_id] = {"src": "fa", "dest": "en"}
                            
                            user_preferences[chat_id][lang_type] = lang_code
                            send_message(
                                chat_id,
                                f"✅ {lang_type} به {get_lang_name(lang_code)} تغییر یافت",
                                create_main_menu(chat_id)
                            )
                        
                        elif data == "swap":
                            prefs = user_preferences.get(chat_id, {"src": "fa", "dest": "en"})
                            src, dest = prefs["src"], prefs["dest"]
                            user_preferences[chat_id]["src"] = dest
                            user_preferences[chat_id]["dest"] = src
                            send_message(chat_id, "🔄 تعویض شد!", create_main_menu(chat_id))
                        
                        elif data == "auto":
                            if chat_id not in user_preferences:
                                user_preferences[chat_id] = {"src": "fa", "dest": "en"}
                            user_preferences[chat_id]["src"] = "auto"
                            send_message(chat_id, "🤖 خودکار فعال شد", create_main_menu(chat_id))
                        
                        elif data == "help":
                            handle_help(chat_id)
                        
                        elif data == "creator":
                            theme_name = user_themes.get(chat_id, 'default')
                            theme = THEMES.get(theme_name, THEMES['default'])
                            send_message(
                                chat_id,
                                f"👤 <b>سازنده</b>\n\n"
                                f"ساخته شده توسط @Mrnobody_ir\n\n"
                                f"🎨 تم: {theme['emoji']} {theme['name']}",
                                create_main_menu(chat_id)
                            )
                        
                        elif data == "back_to_menu":
                            send_message(chat_id, "🔙 منوی اصلی", create_main_menu(chat_id))
                        
                        # Admin callbacks
                        elif data == "admin_stats" and is_admin(chat_id):
                            send_message(chat_id, admin_stats(), create_admin_panel())
                        
                        elif data == "admin_users" and is_admin(chat_id):
                            send_message(chat_id, "👥 لیست کاربران (به زودی)", create_admin_panel())
                        
                        elif data == "admin_blocked" and is_admin(chat_id):
                            if blocked_users:
                                blocked_text = "🚫 <b>کاربران مسدود</b>\n\n"
                                for user_id in blocked_users:
                                    user_info = get_user_info(user_id)
                                    if user_info:
                                        name = user_info.get("first_name", "نامشخص")
                                        blocked_text += f"• {name} (ID: {user_id})\n"
                                send_message(chat_id, blocked_text, create_admin_panel())
                            else:
                                send_message(chat_id, "✅ هیچ کاربر مسدودی وجود ندارد.", create_admin_panel())
            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\n👋 ربات متوقف شد!")
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 خداحافظ!")
        sys.exit(0)
