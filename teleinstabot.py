from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from instabot import InstagramBot


def start(update, context):
    keyboard = [[InlineKeyboardButton("Download instagram images.", callback_data="1")],
                [InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')],
                [InlineKeyboardButton('Option 4', callback_data='4')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query

    if query.data == '1':
        query.edit_message_text(text="Please enter user name for download his images "
                                     "by the syntax : /downloadimages username.\n"
                                     "Note: if the username is private,we cannot download his images.")


def download_images(update, context):
    # if the username of instagram is starting with __ (double underscore) and end with double underscore
    # the bot take without the underscores, so i have to figure out how to ignore that.
    chat_id = update.message.chat_id
    username = context.args

    if len(username) == 0:
        context.bot.send_message(chat_id=chat_id, text="You must enter at least one username.")
        return

    elif len(username) == 1:
        context.bot.send_message(chat_id=chat_id,
                                 text=f"Starting download images from: {username[0]} \n The process will take a few minutes. ")
        ig_bot = InstagramBot()
        images_urls = ig_bot.get_images(username[0])

        if len(images_urls) == 0:
            context.bot.send_message(chat_id=chat_id, text="My friend, check if the account is private.\n"
                                                           "Or the account has no images.")
        else:
            for image in images_urls:
                context.bot.send_photo(chat_id=chat_id, photo=image)

    elif username[1] is not None:
        update.message.reply_text("You cannot pass more than one username.")
        return


def main():
    updater = Updater('Your token', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('downloadimages', download_images))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
