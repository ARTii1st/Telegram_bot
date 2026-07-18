import asyncio
from  menu_bota import  Menu
from class_osnova import Model
from telegram import Update
from telegram.ext import *

tk = ""
menu = Menu()
model = Model()


async def menu_model():
    print("потом реализую")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "settings" not in context.user_data or context.user_data["settings"]["model"] is None:
        context.user_data["settings"] = {
            "model": None,
            "border": 700,
            "creati": 0.7,
            "work": asyncio.Lock(),
        }

        await update.message.reply_text("Выберите модель:", reply_markup=menu.keyboard("model"))
        return

    if context.user_data["settings"]["work"].locked():
        await update.message.reply_text(f"Уже обрабатываю ваш запрос⏳")
        return

    async with context.user_data["settings"]["work"]:
        try:
            if update.message.text :

                await  model.model_ask(update,update.message.text,context.user_data["settings"])

            elif update.message.voice or update.message.audio :

                message = update.message.audio or update.message.voice

                file = await context.bot.get_file(message.file_id)

                await file.download_to_drive(f"{message.file_unique_id}.ogg")

                await model.decoder_voice(update,f"{message.file_unique_id}.ogg",context.user_data["settings"])

            elif update.message.document:
                document = update.message.document

                file = await context.bot.get_file(document.file_id)
                path = f"{document.file_name}"

                await file.download_to_drive(path)

                text = await model.read(update,path)

                await model.model_ask(update, text, context.user_data["settings"])

        except Exception as ex:
            await update.message.reply_text(f"Что то пошло не так, код ошибки {ex}")


def main():

    app = Application.builder().token(tk).build()


    app.add_handler(CommandHandler("menu",menu_model))
    app.add_handler(CallbackQueryHandler(menu.callback))

    app.add_handler(MessageHandler((filters.TEXT |  filters.VOICE | filters.AUDIO | filters.Document.ALL )
                                   & ~filters.COMMAND,message,))

    print("start 0")

    app.run_polling()

if __name__ == "__main__":
    main()