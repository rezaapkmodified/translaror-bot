import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from googletrans import Translator

TOKEN = "8733618033:AAEhmtIeRkSez_kcru4EnFqWddtpP-92tX0"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

translator = Translator()

LANGUAGES = {
    "🇺🇸 انگلیسی": "en",
    "🇮🇷 فارسی": "fa",
    "🇩🇪 آلمانی": "de",
    "🇫🇷 فرانسوی": "fr",
    "🇪🇸 اسپانیایی": "es",
    "🇮🇹 ایتالیایی": "it",
    "🇯🇵 ژاپنی": "ja",
    "🇨🇳 چینی": "zh-cn",
    "🇷🇺 روسی": "ru",
    "🇹🇷 ترکی": "tr",
    "🇦🇪 عربی": "ar",
}

user_data = {}

def get_glassmorphism_buttons(lang_type="src"):
    keyboard = []
    row = []
    glass_colors = ["🔵", "🟢", "🔴", "🟣", "🟠", "🩷", "🩵", "💜", "💚", "💙", "💛"]
    
    for i, (lang_name, lang_code) in enumerate(LANGUAGES.items()):
        color_emoji = glass_colors[i % len(glass_colors)]
        button_text = f"{color_emoji} {lang_name}"
        row.append(
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"lang_{lang_code}_{lang_type}"
            )
        )
        if len(row) == 2:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    return InlineKeyboardMarkup(keyboard)

def get_main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🟦 انتخاب زبان مبدأ", callback_data="show_src"),
            InlineKeyboardButton("🟩 انتخاب زبان مقصد", callback_data="show_dest"),
        ],
        [
            InlineKeyboardButton("🔄 تعویض زبان‌ها", callback_data="swap"),
            InlineKeyboardButton("🤖 ترجمه خودکار", callback_data="auto"),
        ],
        [
            InlineKeyboardButton("📖 راهنما", callback_data="help"),
            InlineKeyboardButton("👤 سازنده", callback_data="creator"),
        ],
        [
            InlineKeyboardButton("✨ وضعیت فعلی", callback_data="status"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"src": "en", "dest": "fa"}
    
    await update.message.reply_text(
        "✨ **ربات ترجمه‌گر هوشمند** ✨\n\n"
        "به ربات ترجمه‌گر با دکمه‌های **شیشه‌ای رنگی** خوش آمدید!\n"
        "می‌توانید متن خود را به بیش از ۱۰ زبان ترجمه کنید.\n\n"
        "🔹 **مراحل استفاده:**\n"
        "1️⃣ از دکمه‌های رنگی زیر، زبان مبدأ و مقصد را انتخاب کنید\n"
        "2️⃣ متن خود را ارسال کنید تا ترجمه شود\n"
        "3️⃣ از دکمه‌های شیشه‌ای برای تغییر تنظیمات استفاده کنید\n\n"
        "👤 **سازنده:** @Mrnobody_ir",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    
    if user_id not in user_data:
        user_data[user_id] = {"src": "en", "dest": "fa"}
    
    if data == "show_src":
        await query.edit_message_text(
            "🟦 **انتخاب زبان مبدأ** (شیشه‌ای رنگی)\n\n"
            "از دکمه‌های رنگی زیر، زبان مبدأ را انتخاب کنید:",
            reply_markup=get_glassmorphism_buttons("src"),
            parse_mode="Markdown"
        )
    
    elif data == "show_dest":
        await query.edit_message_text(
            "🟩 **انتخاب زبان مقصد** (شیشه‌ای رنگی)\n\n"
            "از دکمه‌های رنگی زیر، زبان مقصد را انتخاب کنید:",
            reply_markup=get_glassmorphism_buttons("dest"),
            parse_mode="Markdown"
        )
    
    elif data.startswith("lang_"):
        parts = data.split("_")
        lang_code = parts[1]
        lang_type = parts[2]
        
        if lang_type == "src":
            user_data[user_id]["src"] = lang_code
            await query.edit_message_text(
                f"✅ **زبان مبدأ** به {get_lang_name(lang_code)} تغییر یافت.\n\n"
                f"🟢 حالا زبان مقصد را انتخاب کنید یا متن خود را ارسال کنید.",
                reply_markup=get_main_menu(),
                parse_mode="Markdown"
            )
        else:
            user_data[user_id]["dest"] = lang_code
            await query.edit_message_text(
                f"✅ **زبان مقصد** به {get_lang_name(lang_code)} تغییر یافت.\n\n"
                f"🟢 حالا متن خود را ارسال کنید تا ترجمه شود.",
                reply_markup=get_main_menu(),
                parse_mode="Markdown"
            )
    
    elif data == "swap":
        src = user_data[user_id]["src"]
        dest = user_data[user_id]["dest"]
        user_data[user_id]["src"] = dest
        user_data[user_id]["dest"] = src
        await query.edit_message_text(
            f"🔄 **تعویض انجام شد!**\n\n"
            f"🟦 مبدأ: {get_lang_name(user_data[user_id]['src'])}\n"
            f"🟩 مقصد: {get_lang_name(user_data[user_id]['dest'])}",
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )
    
    elif data == "auto":
        user_data[user_id]["src"] = "auto"
        await query.edit_message_text(
            "🤖 **حالت ترجمه خودکار فعال شد**\n\n"
            "زبان مبدأ به‌صورت خودکار تشخیص داده می‌شود.\n"
            "متن خود را ارسال کنید.",
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )
    
    elif data == "help":
        await query.edit_message_text(
            "📖 **راهنمای ربات شیشه‌ای**\n\n"
            "🔹 **چگونه کار می‌کند؟**\n"
            "1️⃣ از دکمه‌های شیشه‌ای رنگی، زبان مبدأ را انتخاب کنید\n"
            "2️⃣ زبان مقصد را انتخاب کنید\n"
            "3️⃣ متن خود را ارسال کنید\n"
            "4️⃣ ترجمه را دریافت کنید\n\n"
            "🔸 **ویژگی‌ها:**\n"
            "✅ دکمه‌های شیشه‌ای رنگی\n"
            "✅ ترجمه خودکار زبان\n"
            "✅ تعویض سریع زبان‌ها\n"
            "✅ پشتیبانی از ۱۱ زبان زنده دنیا\n\n"
            "👤 **سازنده:** @Mrnobody_ir",
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )
    
    elif data == "creator":
        await query.edit_message_text(
            "👤 **سازنده ربات**\n\n"
            "این ربات با **دکمه‌های شیشه‌ای رنگی** توسط\n"
            "**@Mrnobody_ir** ساخته شده است.\n\n"
            "🌟 برای ارتباط با سازنده، پیام دهید.\n"
            "✨ از استفاده شما سپاسگزاریم!",
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )
    
    elif data == "status":
        src = user_data[user_id]["src"]
        dest = user_data[user_id]["dest"]
        src_name = "خودکار" if src == "auto" else get_lang_name(src)
        await query.edit_message_text(
            f"📊 **وضعیت فعلی:**\n\n"
            f"🟦 زبان مبدأ: {src_name}\n"
            f"🟩 زبان مقصد: {get_lang_name(dest)}\n\n"
            f"💡 برای تغییر، از دکمه‌های شیشه‌ای استفاده کنید.",
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )

def get_lang_name(code):
    for name, c in LANGUAGES.items():
        if c == code:
            return name
    return code

async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if user_id not in user_data:
        user_data[user_id] = {"src": "en", "dest": "fa"}
    
    src = user_data[user_id]["src"]
    dest = user_data[user_id]["dest"]
    
    if not text:
        await update.message.reply_text("⚠️ لطفاً یک متن معتبر ارسال کنید.")
        return
    
    try:
        if src == "auto":
            result = translator.translate(text, dest=dest)
            detected_lang = result.src
            translated = result.text
            await update.message.reply_text(
                f"🔍 **زبان تشخیص داده شده:** {get_lang_name(detected_lang)}\n"
                f"🌍 **ترجمه به {get_lang_name(dest)}:**\n\n"
                f"✨ {translated}",
                parse_mode="Markdown"
            )
        else:
            result = translator.translate(text, src=src, dest=dest)
            await update.message.reply_text(
                f"🔄 **از {get_lang_name(src)} به {get_lang_name(dest)}:**\n\n"
                f"🌟 {result.text}",
                parse_mode="Markdown"
            )
    except Exception as e:
        logger.error(f"خطا در ترجمه: {e}")
        await update.message.reply_text(
            "❌ **خطا در ترجمه!**\n\n"
            "لطفاً دوباره تلاش کنید یا زبان‌های دیگری انتخاب کنید.",
            parse_mode="Markdown"
        )

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))
    
    print("🌟 ربات ترجمه‌گر با دکمه‌های شیشه‌ای رنگی راه‌اندازی شد...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
