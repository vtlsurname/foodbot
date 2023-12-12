from main import bot, dp 
from aiogram.types import Message
from keyboard.admin_kb import bl_menu
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import sqlite3


@dp.message_handler(text='ЧС')
async def get_bl_menu(message:Message):
    await message.answer(text='Ви перейшли в меню Чорного Списку', reply_markup=bl_menu)


class AddToBlacklist(StatesGroup):
    waiting_for_user_id = State()

@dp.message_handler(text='Додати до ЧС')
async def start_add_to_bl(message: Message):
    await message.answer('Введіть user_id користувача, якого потрібно додати до ЧС. Якщо ви бажаєте відмінити дію, напишіть "cencel".')
    await AddToBlacklist.waiting_for_user_id.set()

@dp.message_handler(state=AddToBlacklist.waiting_for_user_id)
async def process_user_id(message: Message, state: FSMContext):
    user_id = message.text

    if user_id.lower() == 'cencel':
        await message.answer('Дія скасована.')
        await state.finish()
        return

    try:
        user_id = int(user_id)
    except ValueError:
        await message.answer('Будь ласка, введіть правильний user_id.')
        return

    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    # записываем user_id в таблицу black_list
    cursor.execute(f"INSERT INTO black_list (user_id) VALUES ('{user_id}')")

    # сохраняем изменения в бд
    conn.commit()

    # закрываем соединение
    conn.close()

    await message.answer(f'Користувач з user_id {user_id} доданий до ЧС.')
    await state.finish()


class RemoveFromBlacklist(StatesGroup):
    waiting_for_user_id = State()

@dp.message_handler(text='Видалити з ЧС')
async def start_remove_from_bl(message: Message):
    await message.answer('Введіть user_id користувача, якого потрібно видалити з ЧС. Якщо ви бажаєте відмінити дію, напишіть "cencel".')
    await RemoveFromBlacklist.waiting_for_user_id.set()

class RemoveFromBlacklist(StatesGroup):
    waiting_for_user_id = State()

    @staticmethod
    async def is_user_in_blacklist(user_id: int) -> bool:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM black_list WHERE user_id = '{user_id}'")
        result = cursor.fetchone()
        conn.close()
        return bool(result[0])

    @staticmethod
    async def remove_user_from_blacklist(user_id: int):
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM black_list WHERE user_id='{user_id}'")
        conn.commit()
        conn.close()

    @staticmethod
    async def send_user_not_found_message(message: Message):
        await message.answer('Користувача з таким user_id не знайдено.')

    @dp.message_handler(text='Видалити з ЧС')
    async def start_remove_from_bl(message: Message):
        await message.answer('Введіть user_id користувача, якого потрібно видалити з ЧС. Якщо ви бажаєте відмінити дію, напишіть "cencel".')
        await RemoveFromBlacklist.waiting_for_user_id.set()

    @dp.message_handler(state=RemoveFromBlacklist.waiting_for_user_id)
    async def process_remove_user_id(message: Message, state: FSMContext):
        user_id = message.text

        if user_id.lower() == 'cencel':
            await message.answer('Дія скасована.')
            await state.finish()
            return

        try:
            user_id = int(user_id)
        except ValueError:
            await message.answer('Будь ласка, введіть правильний user_id.')
            return

        if await RemoveFromBlacklist.is_user_in_blacklist(user_id):
            await RemoveFromBlacklist.remove_user_from_blacklist(user_id)
            await message.answer(f'Користувач з user_id {user_id} видалений з ЧС.')
        else:
            await RemoveFromBlacklist.send_user_not_found_message(message)

        await state.finish()
