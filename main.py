# telegram
import requests
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Final
# env
import os
from dotenv import load_dotenv
load_dotenv()


TOKEN: Final = os.getenv("TOKEN")
BOT_USERNAME: Final = '@BlockCodeBot'


# Set a higher timeout value (e.g., 10 seconds)
response = requests.get(
    f'https://api.telegram.org/bot<{TOKEN}>/getMe', timeout=30)

# Buttons
main_buttons = [[InlineKeyboardButton('About Me 👨‍💻', callback_data='info'),
                 InlineKeyboardButton('Skills  ⌨️ ', callback_data='skills')],
                [InlineKeyboardButton('Resume  🧾', callback_data='resume'),
                 InlineKeyboardButton('Projects  🌐', callback_data='project')],
                [InlineKeyboardButton('Contact  📞', callback_data='contact')]
                ]

contact_buttons = [
    [InlineKeyboardButton('GitHub 🔮', url='https://github.com/aliseyedi01'),
        InlineKeyboardButton('LinkedIn 👨‍💻', url='https://www.linkedin.com/in/aliseyedi01/')],
    [InlineKeyboardButton('Email  ✉', url='https://mail.google.com/mail/u/0/?view=cm&fs=1&to=aliseyedi07@gmail.com1'),
        InlineKeyboardButton('Chat  🗯', url='https://t.me/aliseyedi01')],
    [InlineKeyboardButton('Back 🔙', callback_data='back_contact')]
]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to My Bot!', reply_markup=InlineKeyboardMarkup(main_buttons))


async def handle_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data

    print(f"Received CallbackQuery: {query}")

    if data == "info":
        await send_information(update, context)
    elif data == "skills":
        await send_skills(update, context)
    elif data == "resume":
        await send_resume(update, context)
    elif data == "project":
        await send_projects(update, context)
    elif data == "contact":
        await send_contact(update, context)
    elif data == "back_contact":
        await send_back_contact(update, context)


async def send_back_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(text='Welcome to my bot!', reply_markup=InlineKeyboardMarkup(main_buttons))


async def send_information(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is where you can find information about me and my work.')


async def send_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(text='Select a contact option:', reply_markup=InlineKeyboardMarkup(contact_buttons))


async def send_projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Here you can find a list of my projects.')


async def send_skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Here you can find a list of my skills.')


async def send_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Here you can find my resume')


# Response
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return 'hey there!'

    return "I do not understand what you wrote ..."


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        # Process regular messages
        message_type: str = update.message.chat.type
        text: str = update.message.text

        # print(f'User ({update.message.chat.id}) in {message_type}: "{text}" ')

        if message_type == "group":
            if BOT_USERNAME in text:
                new_text: str = text.replace(BOT_USERNAME, '').strip()
                response: str = handle_response(new_text)
            else:
                return
        else:
            response: str = handle_response(text)

        print('Bot:', response)

        await update.message.reply_text(response)

    elif update.callback_query:
        # Process callback queries
        await handle_button_press(update, context)

    else:
        print("Unsupported update type")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('starting bot ...')
    app = Application.builder().token(TOKEN).build()

    # Handle inline button clicks
    app.add_handler(CallbackQueryHandler(handle_button_press))

    # commands
    app.add_handler(CommandHandler('start', start_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(error)

    print('polling ...')
    app.run_polling(timeout=10)
