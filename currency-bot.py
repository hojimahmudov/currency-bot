import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, filters, MessageHandler

url = "https://cbu.uz/oz/arkhiv-kursov-valyut/json/"


async def start(update, context):
    user = update.message.from_user
    await update.message.reply_text(f"Assalomu alaykum {user.first_name}\nXush kelibsiz botimizga")

    buttons = [
        [KeyboardButton("USD>UZS"), KeyboardButton("RUB>UZS")],
        [KeyboardButton("UZS>USD"), KeyboardButton("UZS>RUB")],
        [KeyboardButton("Barchasini ko'rish")]
    ]
    await update.message.reply_text("Valyutalar uchun tanlang",
                                    reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))


async def message_handler(update, context):
    text = update.message.text
    if text == "USD>UZS" or text == "RUB>UZS" or text == "UZS>USD" or text == "UZS>RUB":
        await update.message.reply_text(f"Siz {text} ni tanladingiz.\nMiqdorni kiriting: ")
    elif text == "Barchasini ko'rish":
        son = 1
        kurs = ""
        data = requests.get(url)
        for i in data.json():
            kurs += f"{son}.{i['CcyNm_UZ']} = {i['Rate']} so'm\n"
            son += 1
        await update.message.reply_text(kurs)
    else:
        pass


app = ApplicationBuilder().token('Your token').build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, message_handler))

app.run_polling()
