from main import bot, dp 
from aiogram.types import Message
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import sqlite3
import os
from aiogram.types import ContentType
from base.bd_funcs import get_admin_ids_from_database
from keyboard.admin_kb import newsletter_menu


@dp.message_handler(text='Розсилка')
async def start_menu_news(message:Message):
    admin_ids = get_admin_ids_from_database()
    user_id = message.from_id

    if user_id in admin_ids:
        await message.answer(text='Ви перейшли в меню розсилки', reply_markup=newsletter_menu)
    else:
        await message.answer(text='Ви не адміністратор!')

def get_users_ids():
    con = sqlite3.connect('base.db')
    cur = con.cursor()

    cur.execute("SELECT user_id FROM users_info_bd")

    user_ids = []

    for user in cur.fetchall():
        user_ids.append(user[0])

    con.close()

    return user_ids


class newsletter_without_photo(StatesGroup):
    text = State()
    yes_or_no = State()
newsletter_text = ''

@dp.message_handler(text='Розсилка без фото')
async def get_newsletter_text(message:Message):
    user_id = message.from_id
    admin_ids = get_admin_ids_from_database()

    if user_id in admin_ids:
        await message.answer(text='Надішліть текст для розсилання')
        await newsletter_without_photo.text.set()
    else:
        await message.answer(text='Ти не адмін!')


@dp.message_handler(state=newsletter_without_photo.text)
async def go_news(message:Message, state:FSMContext):
    global newsletter_text 

    newsletter_text = message.text
    await message.answer(text='Ви точно хочете розіслати це повідомлення? Так / Ні')

    await newsletter_without_photo.yes_or_no.set()

@dp.message_handler(state=newsletter_without_photo.yes_or_no)
async def lets_make_new(message:Message, state:FSMContext):
    global newsletter_text
    
    if message.text.lower() == 'так':
        users = get_users_ids()
        for user in users:
            try:
                await bot.send_message(chat_id=user, text=newsletter_text)
            except:
                pass

    elif message.text.lower() == 'ні':
        await message.answer(text='Розсилання було скасовано.')
        
        try:
            os.remove('temp2.png')
        except Exception as ex:
            print(ex)

    await state.finish()


class NewsletterWithPhoto(StatesGroup):
    text = State()
    photo = State()
    confirmation = State()

newsletter_text = ''
newsletter_photo = None

@dp.message_handler(text='Розсилка з фото')
async def get_newsletter_text(message: Message):
    user_id = message.from_id
    admin_ids = get_admin_ids_from_database()

    if user_id in admin_ids:
        await message.answer(text='Напишіть текст для розсилки')
        await NewsletterWithPhoto.text.set()
    else:
        await message.answer(text='Ти не адмін!')

@dp.message_handler(state=NewsletterWithPhoto.text)
async def get_newsletter_photo(message: Message, state: FSMContext):
    global newsletter_text
    newsletter_text = message.text
    await message.answer(text='Надішліть фото для розсилки')
    await NewsletterWithPhoto.photo.set()

@dp.message_handler(content_types=ContentType.PHOTO, state=NewsletterWithPhoto.photo)
async def confirm_newsletter(message: Message, state: FSMContext):
    global newsletter_photo
    newsletter_photo = await message.photo[-1].download('temp2.png')
    await message.answer(text='Ви впевнені, що хочете надіслати розсилку з цим фото і текстом? (Так/Ні)')
    await NewsletterWithPhoto.confirmation.set()

@dp.message_handler(state=NewsletterWithPhoto.confirmation)
async def send_newsletter(message: Message, state: FSMContext):
    if message.text.lower() == 'так':
        users = get_users_ids()
        for user in users:
            try:
                photo = open('temp2.png', 'rb')
                await bot.send_photo(chat_id=user, photo=photo, caption=newsletter_text)
            except Exception as ex:
                print(ex)
            finally:
                photo.close()

        await message.answer(text='Розсилку успішно надіслано')
    else:
        await message.answer(text='Розсилку скасовано')

    await state.finish()

    try:
        os.remove('temp2.png')
    except Exception as ex:
        print(ex)
