from class_osnova import Model
from telegram import Update
from telegram.ext import *

tk = "8964274325:AAF4S2FeKVqFpZoOvEWgGKEpA9m5ouOYq8I"
length = 4096
qwen3_code = Model("huihui_ai/qwen3-coder-abliterated:latest")

def length_message(text):
    parts = [text[i:i + length]
        for i in range(0, len(text), length)]
    return parts

async def qwen3_coder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["model"]  = "qwen3_coder"
    await update.message.reply_text("Вы выбрали модель qwen3_coder")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    model = context.user_data.get("model")
    text = update.message.text

    if model == "qwen3_coder":

        try:

            await update.message.reply_text(f"Qwen3_coder думает..")

            result = await  qwen3_code.model_ask(text)

            if len(result) > length:
               result_list  = length_message(result)
               for part in result_list:
                   await update.message.reply_text(part)

            else:
                await  update.message.reply_text(result)
        except Exception as ex:
            await update.message.reply_text(f"Что то пошло не так, код ошибки {ex}")

    else:

        await update.message.reply_text(
            "Выберите любую модель:\n"
            "/qwen3_coder\n"
        )

def main():

    app = Application.builder().token(tk).build()

    app.add_handler(CommandHandler("qwen3_coder", qwen3_coder))

    app.add_handler(
        MessageHandler(
            filters.TEXT &  filters.AUDIO & ~filters.COMMAND,
            message,
        )
    )

    print("start 0")

    app.run_polling()

if __name__ == "__main__":
    main()