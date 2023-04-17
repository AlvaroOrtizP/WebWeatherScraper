
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler

import os
TOKEN = ""

def fijarComentario(update, callback_context):
    message = update.message.reply_to_message
    callback_context.bot.pin_chat_message(message.chat.id, message.message_id)
    
# En el método main se inicializan
def main():
   
    print(os.getcwd())
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("saludo", fijarComentario))
    
    #updater.bot.send_message(CHAT_ID, "Bienvenido...")

    updater.start_polling()

    # Para mantener activo el bot hasta pulsar cntl c
    updater.idle()

if __name__ == "__main__":
    main()