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
            text='➕ Tambah akun',
            callback_data='add_account'
        ),
        InlineKeyboardButton(
            text='⚙️ Kelola akun',
            callback_data='manage_accounts'
        ),
        InlineKeyboardButton(
            text='💧 Buat droplets',
            callback_data='create_droplet'
        ),
        InlineKeyboardButton(
            text='🛠️ Kelola droplets',
            callback_data='manage_droplets'
        ),
    )
    t = f'Selamat Datang <b>{bot_name}</b> 👋\n\n' \
        'Anda dapat mengelola akun DigitalOcean, membuat instance, dll.\n\n' \
        'Perintah cepat:\n' \
        '/start - Memulai bot\n' \
        '/add_do - Tambah akun\n' \
        '/sett_do - Kelola akun\n' \
        '/bath_do - Uji batch akun\n' \
        '/add_vps - Buat droplets\n' \
        '/sett_vps - Kelola droplets\n' \
        ' \n' \
        '<b>Dev: @yha_bot</b> 👨‍💻\n' \
        '<b>Support: @fightertunnell</b> 🛡️'
    bot.send_message(
        text=t,
        chat_id=d.from_user.id,
        parse_mode='HTML',
        reply_markup=markup
    )
