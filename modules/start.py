from os import environ

from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from _bot import bot

bot_name = environ.get('bot_name', 'Asisten DigitalOcean')


def start(d: Message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            text='Add account',
            callback_data='add_account'
        ),
        InlineKeyboardButton(
            text='Manage accounts',
            callback_data='manage_accounts'
        ),
        InlineKeyboardButton(
            text='Create droplets',
            callback_data='create_droplet'
        ),
        InlineKeyboardButton(
            text='Manage droplets',
            callback_data='manage_droplets'
        ),
    )
    t = f'Selamat Datang <b>{bot_name}</b>\n\n' \
        'Anda dapat mengelola akun DigitalOcean, membuat instance, dll.\n\n' \
        'Perintah cepat:\n' \
        '/start - start bot\n' \
        '/add_do - add account\n' \
        '/sett_do - manage accounts\n' \
        '/bath_do - batch test accounts\n' \
        '/add_vps - create droplets\n' \
        '/sett_vps - manage droplets\n' \
        ' \n' \
        '<b>Dev: @yha_bot</b>\n' \
        '<b>Support: @fightertunnell</b>'
    bot.send_message(
        text=t,
        chat_id=d.from_user.id,
        parse_mode='HTML',
        reply_markup=markup
    )
