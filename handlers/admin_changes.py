from main import bot, dp 
from base.bd_funcs import set_message_id, get_message_id, delete_admin_from_database, get_admin_list_from_database
from aiogram.types import Message
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from keyboard.admin_kb import team_menu
from base.bd_funcs import add_new_admin_func
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from inline_keyboard.main_board import get_main_menu


@dp.message_handler(text='/myid')
async def get_myid(message: Message):
    msg = await bot.send_message(chat_id=message.from_id, text=f'your id: {message.from_id}')
    set_message_id(user_id=message.from_id, message_id=msg['message_id'])


@dp.message_handler(text='Працівники')
async def staff_menu(message:Message):
    msg = await message.answer(text='Меню для роботи з працівниками', reply_markup=team_menu)
    set_message_id(user_id=message.from_id, message_id=msg['message_id'])


class NewAdmin(StatesGroup):
    user_id = State()
    user_name = State()

@dp.message_handler(text='Додати адміна')
async def add_new_admin(message: Message):
    await message.answer(text='Напишіть ID людини, яку ви хочете додати новим адміном (/myid)\nАбо напишіть cencel для відміни')
    await NewAdmin.user_id.set()

@dp.message_handler(state=NewAdmin.user_id)
async def get_user_id(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'cencel':
            await state.finish()
            await message.answer(text='Дію було відмінено, напишіть /start')
        else:
            try:
                data['user_id'] = int(message.text)
                await message.answer(text="Напишіть ім'я працівника\nАбо напишіть cancel для відміни")
                await NewAdmin.next()
            except ValueError:
                await message.answer(text='Будь ласка, введіть числове значення або напишіть cancel для відміни')


@dp.message_handler(state=NewAdmin.user_name)
async def get_user_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'cencel':
            await state.finish()
            await message.answer(text='Дію було відмінено, напишіть /start')
        else:
            data['user_name'] = message.text
            # Call the function that adds a new admin here
            answer = add_new_admin_func(user_id=data['user_id'], user_name=data['user_name'])
            await message.answer(text=answer)
            await state.finish()


class AdminDeletion(StatesGroup):
    admin_name = State()
    confirmation = State()

@dp.message_handler(text='Видалити адміна')
async def delete_admin_start(message: types.Message):
    admins = get_admin_list_from_database()

    if not admins:
        await message.answer("Немає адміністраторів для видалення.")
        return

    keyboard = InlineKeyboardMarkup()
    for admin in admins:
        keyboard.add(InlineKeyboardButton(admin, callback_data=admin))
    
    msg = await message.answer("Якого адміністратора ви хочете видалити?", reply_markup=keyboard)
    set_message_id(user_id=message.from_id, message_id=msg['message_id'])

    await AdminDeletion.admin_name.set()

@dp.callback_query_handler(lambda c: c.data, state=AdminDeletion.admin_name)
async def delete_admin_selected(callback_query: types.CallbackQuery, state: FSMContext):
    admin_name = callback_query.data
    user_id = callback_query.from_user.id
    await state.update_data(admin_name=admin_name)
    
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton('Так', callback_data='yes'),
        InlineKeyboardButton('Ні', callback_data='no')
    )
    message = await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=get_message_id(user_id),text=f"Ви впевнені, що хочете видалити {admin_name}? Будь ласка, дайте відповідь 'так' або 'ні'")
    
    
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=message.message_id, reply_markup=keyboard)
    await AdminDeletion.confirmation.set()

@dp.callback_query_handler(lambda c: c.data in ['yes', 'no'], state=AdminDeletion.confirmation)
async def delete_admin_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    menu = get_main_menu()
    user_id = callback_query.from_user.id
    message_id = get_message_id(user_id)
    
    if callback_query.data == 'yes':
        data = await state.get_data()
        admin_name = data['admin_name']
        delete_admin_from_database(admin_name)
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=f"{admin_name} було видалено.", reply_markup=menu)
    else:
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text="Видалення адміністратора скасовано.", reply_markup=menu)
    await state.finish()
