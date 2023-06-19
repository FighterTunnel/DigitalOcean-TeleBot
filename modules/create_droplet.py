from typing import Union
from time import sleep

from telebot.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

import digitalocean

from _bot import bot
from utils.db import AccountsDB
from utils.localizer import localize_region
from utils.set_root_password_script import set_root_password_script
from utils.password_generator import password_generator

user_dict = {}

t = '<b>Buat instance</b>\n\n'


def create_droplet(d: Union[Message, CallbackQuery], data: dict = None):
    data = data or {}
    next_func = data.get('nf', ['select_account'])[0]
    if next_func in globals():
        data.pop('nf', None)
        args = [d]
        if len(data.keys()) > 0:
            args.append(data)

        globals()[next_func](*args)


def select_account(d: Union[Message, CallbackQuery]):
    accounts = AccountsDB().all()
    markup = InlineKeyboardMarkup()
    for account in accounts:
        markup.add(
            InlineKeyboardButton(
                text=account['email'],
                callback_data=f'create_droplet?nf=select_region&doc_id={account.doc_id}'
            )
        )

    bot.send_message(
        text=f'{t}'
             'Pilih Akun',
        chat_id=d.from_user.id,
        parse_mode='HTML',
        reply_markup=markup
    )


def select_region(call: CallbackQuery, data: dict):
    doc_id = data['doc_id'][0]

    account = AccountsDB().get(doc_id=doc_id)
    user_dict[call.from_user.id] = {
        'account': account
    }

    _t = t + f'Akun: <code>{account["email"]}</code>\n\n'

    bot.edit_message_text(
        text=f'{_t}'
             f'Dapatkan di Negara tersebut...',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    regions = digitalocean.Manager(token=account['token']).get_all_regions()

    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for region in regions:
        if region.available:
            buttons.append(
                InlineKeyboardButton(
                    text=localize_region(slug=region.slug),
                    callback_data=f'create_droplet?nf=select_size&region={region.slug}'
                )
            )
    markup.add(*buttons)

    bot.edit_message_text(
        text=f'{_t}'
             f'Pilih area tersebut',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode='HTML'
    )


def select_size(call: CallbackQuery, data: dict):
    region_slug = data['region'][0]

    user_dict[call.from_user.id].update({
        'region_slug': region_slug
    })

    _t = t + f'Akun: <code>{user_dict[call.from_user.id]["account"]["email"]}</code>\n' \
             f'Negara: <code>{region_slug}</code>\n\n'

    bot.edit_message_text(
        text=f'{_t}'
             f'Dapatkan Modelnya...',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    sizes = digitalocean.Manager(token=user_dict[call.from_user.id]['account']['token']).get_all_sizes()

    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for size in sizes:
        if region_slug in size.regions:
            buttons.append(
                InlineKeyboardButton(
                    text=size.slug,
                    callback_data=f'create_droplet?nf=select_image&size={size.slug}'
                )
            )
    markup.add(*buttons)
    markup.row(
        InlineKeyboardButton(
            text='Sebelumnya',
            callback_data=f'create_droplet?nf=select_region&doc_id={user_dict[call.from_user.id]["account"].doc_id}'
        )
    )

    bot.edit_message_text(
        text=f'{_t}'
             f'Pilih Modelnya',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode='HTML'
    )


def select_image(d: Union[Message, CallbackQuery], data: dict):
    size_slug = data['size'][0]

    user_dict[d.from_user.id].update({
        'size_slug': size_slug
    })

    _t = t + f'Akun: <code>{user_dict[d.from_user.id]["account"]["email"]}</code>\n' \
             f'Negara: <code>{user_dict[d.from_user.id]["region_slug"]}</code>\n' \
             f'Model: <code>{size_slug}</code>\n\n'

    def get_image_markup():
        images = digitalocean.Manager(token=user_dict[d.from_user.id]['account']['token']).get_distro_images()

        markup = InlineKeyboardMarkup(row_width=2)
        buttons = []
        for image in images:
            if image.distribution in ['Ubuntu', 'CentOS', 'Debian'] \
                    and image.public \
                    and image.status == 'available' \
                    and user_dict[d.from_user.id]["region_slug"] in image.regions:
                buttons.append(
                    InlineKeyboardButton(
                        text=f'{image.distribution} {image.name}',
                        callback_data=f'create_droplet?nf=get_name&image={image.slug}'
                    )
                )
        markup.add(*buttons)
        markup.row(
            InlineKeyboardButton(
                text='Sebelumnya',
                callback_data=f'create_droplet?nf=select_size&region={user_dict[d.from_user.id]["region_slug"]}'
            )
        )

        return markup

    if type(d) == Message:
        msg = bot.send_message(
            text=f'{_t}'
                 f'Dapatkan Sys Os...',
            chat_id=d.from_user.id,
            parse_mode='HTML'
        )
        bot.edit_message_text(
            text=f'{_t}'
                 f'Pilih Sys Os',
            chat_id=d.from_user.id,
            message_id=msg.message_id,
            reply_markup=get_image_markup(),
            parse_mode='HTML'
        )

    elif type(d) == CallbackQuery:
        bot.edit_message_text(
            text=f'{_t}'
                 f'Dapatkan Sys Os...',
            chat_id=d.from_user.id,
            message_id=d.message.message_id,
            parse_mode='HTML'
        )
        bot.edit_message_text(
            text=f'{_t}'
                 f'Pilih Sys Os',
            chat_id=d.from_user.id,
            message_id=d.message.message_id,
            reply_markup=get_image_markup(),
            parse_mode='HTML'
        )


def get_name(call: CallbackQuery, data: dict):
    image_slug = data['image'][0]

    user_dict[call.from_user.id].update({
        'image_slug': image_slug
    })

    _t = t + f'Akun: <code>{user_dict[call.from_user.id]["account"]["email"]}</code>\n' \
             f'Negara: <code>{user_dict[call.from_user.id]["region_slug"]}</code>\n' \
             f'Model: <code>{user_dict[call.from_user.id]["size_slug"]}</code>\n' \
             f'Sys Os: <code>{image_slug}</code>\n\n'

    msg = bot.edit_message_text(
        text=f'{_t}'
             'Harap balas nama contoh: FighterTunnel\n\n'
             '/back Sebelumnya',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )
    bot.register_next_step_handler(msg, ask_create)


def ask_create(m: Message):
    if m.text == '/back':
        select_image(m, data={'size': [user_dict[m.from_user.id]["size_slug"]]})
        return

    _t = t + f'Akun: <code>{user_dict[m.from_user.id]["account"]["email"]}</code>\n' \
             f'Negara: <code>{user_dict[m.from_user.id]["region_slug"]}</code>\n' \
             f'Model: <code>{user_dict[m.from_user.id]["size_slug"]}</code>\n' \
             f'Sys Os: <code>{user_dict[m.from_user.id]["image_slug"]}</code>\n' \
             f'Nama: <code>{m.text}</code>\n\n'
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            text='Sebelumnya',
            callback_data=f'create_droplet?nf=get_name&image={user_dict[m.from_user.id]["image_slug"]}'
        ),
        InlineKeyboardButton(
            text='Membatalkan',
            callback_data='create_droplet?nf=cancel_create'
        ),
    )
    markup.row(
        InlineKeyboardButton(
            text='membuat',
            callback_data=f'create_droplet?nf=confirm_create&name={m.text}'
        )
    )

    bot.send_message(
        text=_t,
        chat_id=m.from_user.id,
        reply_markup=markup,
        parse_mode='HTML'
    )


def cancel_create(call: CallbackQuery):
    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             '<b>Membatalkan</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )


def confirm_create(call: CallbackQuery, data: dict):
    droplet_name = data['name'][0]
    password = password_generator()

    bot.edit_message_text(
        text=f'{call.message.html_text}\n\n'
             '<b>Buat instance...</b>',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )

    droplet = digitalocean.Droplet(
        token=user_dict[call.from_user.id]['account']['token'],
        name=droplet_name,
        region=user_dict[call.from_user.id]['region_slug'],
        image=user_dict[call.from_user.id]['image_slug'],
        size_slug=user_dict[call.from_user.id]['size_slug'],
        user_data=set_root_password_script(password)
    )
    droplet.create()

    droplet_actions = droplet.get_actions()
    for action in droplet_actions:
        while action.status != 'completed':
            sleep(3)
            action.load()
    droplet.load()

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Periksa detailnya',
            callback_data=f'droplet_detail?'
                          f'doc_id={user_dict[call.from_user.id]["account"].doc_id}&'
                          f'droplet_id={droplet.id}'
        )
    )

    bot.edit_message_text(
        text=f'{call.message.html_text}\n'
             f'kata sandi: <code>{password}</code>\n'
             f'IP： <code>{droplet.ip_address}</code>\n\n'
             '<b>Penciptaan server selesai</b>',
        chat_id=call.from_user.id,
        reply_markup=markup,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )
