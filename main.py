import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ChatMemberHandler, MessageHandler, filters

token = ''

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Fonction pour gérer les messages texte dans le groupe spécifié
def handle_text_messages(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Fonction pour accueillir les nouveaux membres du groupe
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.new_chat_members[0]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Bienvenue {user.first_name}!")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Vérifiez si l'utilisateur a le droit d'expulser des membres (administrateur)
    if context.bot.get_chat_member(update.effective_chat.id, update.message.from_user.id).status in ['administrator', 'creator']:
        # Récupérez l'ID de l'utilisateur mentionné
        user_id = update.message.reply_to_message.from_user.id
        # Bannissez l'utilisateur
        context.bot.kick_chat_member(update.effective_chat.id, user_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"L'utilisateur a été banni.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Vous n'avez pas les droits nécessaires pour bannir des membres.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()

    # Ajoutez un gestionnaire pour les messages texte
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Chat(chat_id=1757619197), handle_text_messages))

    # Ajoutez un gestionnaire pour les nouveaux membres du groupe
    application.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler('ban', ban_user)
    
    application.run_polling()

