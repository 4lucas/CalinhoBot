import os
import random
import datetime
import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

def get_random_audio():
    audio_dir = "audios"
    audio_files = os.listdir(audio_dir)
    random_audio = random.choice(audio_files)
    return os.path.join(audio_dir, random_audio)

def get_random_photo():
    photo_dir = "fotos"
    photo_files = os.listdir(photo_dir)
    random_photo = random.choice(photo_files)
    return os.path.join(photo_dir, random_photo)

def get_greeting():
    current_hour = datetime.datetime.now().hour
    if 6 <= current_hour < 12:
        return "Bom dia"
    elif 12 <= current_hour < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

def handle_message(update, context):
    try:
        user_name = update.message.from_user.first_name
        user_id = update.message.from_user.id
        user_message = update.message.text
        greeting = get_greeting()
        
        # Verifica se a mensagem não é um comando conhecido
        if user_message not in ["/audio", "/foto"]:
            message = f"{greeting}, {user_name}!\nObrigado por sua mensagem\nAcesse o menu lateral e diga o que você quer receber"
            context.bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        logging.error(f"Erro durante o processamento: {e}")

def handle_audio_command(update, context):
    try:
        audio_file = get_random_audio()
        context.bot.send_audio(chat_id=update.message.chat_id, audio=open(audio_file, "rb"))
        
        log_message = f"Data/Hora: {datetime.datetime.now()}, Comando: /audio, Áudio: {audio_file}"
        logging.info(log_message)
    except Exception as e:
        logging.error(f"Erro durante o processamento: {e}")

def handle_photo_command(update, context):
    try:
        photo_file = get_random_photo()
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open(photo_file, "rb"))
        
        log_message = f"Data/Hora: {datetime.datetime.now()}, Comando: /foto, Foto: {photo_file}"
        logging.info(log_message)
    except Exception as e:
        logging.error(f"Erro durante o processamento: {e}")

def main():
    # Configure o log para registrar em um arquivo
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "bot_log.log")
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Insira o token do seu bot do Telegram aqui
    token = "TOKEN_AQUI"

    updater = Updater(token)
    dispatcher = updater.dispatcher

    # Vincular os handlers de comando e de mensagem ao bot
    dispatcher.add_handler(CommandHandler("audio", handle_audio_command))
    dispatcher.add_handler(CommandHandler("foto", handle_photo_command))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # Iniciar o bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
