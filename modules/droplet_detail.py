from telebot.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

import digitalocean

from _bot import bot
from utils.db import AccountsDB
from utils.localizer import localize_region


def droplet_detail(call: CallbackQuery, data: dict):
    doc_id = data['doc_id'][0]
    droplet_id = data['droplet_id'][0]
    t = '<b>Informasi Server</b>\n\n'

    try:
        account = AccountsDB().get(doc_id=doc_id)
    except Exception as e:
        bot.edit_message_text(
            text=f'{t}'
                 '⚠️ Kesalahan saat mengambil akun: '
                 f'<code>{str(e)}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return

    bot.edit_message_text(
        text=f'{t}'
             f'Akun: <code>{account["email"]}</code>\n\n'
             'Mengambil informasi instan...',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    try:
        droplet = digitalocean.Droplet().get_object(
            api_token=account['token'],
            droplet_id=droplet_id
        )
    except Exception as e:
        bot.edit_message_text(
            text=f'{t}'
                 f'Akun: <code>{account["email"]}</code>\n\n'
                 '⚠️ Kesalahan saat mengambil informasi droplet: '
                 f'<code>{str(e)}</code>',
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )
        return
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='🗑️ Hapus',
            callback_data=f'droplet_actions?doc_id={doc_id}&droplet_id={droplet_id}&a=delete'
        ),
    )
    power_buttons = []
    if droplet.status == 'active':
        power_buttons.extend([
            InlineKeyboardButton(
                text='🛑 Matikan',
                callback_data=f'droplet_actions?doc_id={doc_id}&droplet_id={droplet_id}&a=shutdown'
            ),
            InlineKeyboardButton(
                text='🔄 Restart',
                callback_data=f'droplet_actions?doc_id={doc_id}&droplet_id={droplet_id}&a=reboot'
            ),
        ])
        power_buttons.extend([
            InlineKeyboardButton(
                text='🔨 Rebuild',
                callback_data=f'droplet_actions?doc_id={doc_id}&droplet_id={droplet_id}&a=rebuild'
            ),
            InlineKeyboardButton(
                text='🔑 Reset Password',
                callback_data=f'droplet_actions?doc_id={doc_id}&droplet_id={droplet_id}&a=reset_password'
            )
        ])
    else:
        power_buttons.append(
            InlineKeyboardButton(
                text='⚡ Nyalakan',
                callback_data=f'droplet_actions?doc_id={doc_id}&droplet_id={droplet_id}&a=power_on'
            )
        )
    markup.row(*power_buttons[:2])
    markup.row(*power_buttons[2:])
    markup.row(
        InlineKeyboardButton(
            text='🔄 Refresh',
            callback_data=f'droplet_detail?doc_id={account.doc_id}&droplet_id={droplet_id}'
        ),
        InlineKeyboardButton(
            text='🔙 Kembali',
            callback_data=f'list_droplets?doc_id={account.doc_id}'
        )
    )

    bot.edit_message_text(
        text=f'{t}'
             f'👤 Akun: <code>{account["email"]}</code>\n'
             f'🏷️ Nama: <code>{droplet.name}</code>\n'
             f'📏 Model: <code>{droplet.size_slug}</code>\n'
             f'🌍 Wilayah: <code>{localize_region(droplet.region["slug"])}</code>\n'
             f'💻 Sistem Operasi: <code>{droplet.image["distribution"]} {droplet.image["name"]}</code>\n'
             f'💾 Hard Disk: <code>{droplet.disk} GB</code>\n'
             f'🌐 IP Publik: <code>{droplet.ip_address}</code>\n'
             f'🔒 IP Privat: <code>{droplet.private_ip_address}</code>\n'
             f'📊 Status: <code>{droplet.status}</code>\n'
             f'📅 Dibuat pada: <code>{droplet.created_at.split("T")[0]}</code>\n',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )
