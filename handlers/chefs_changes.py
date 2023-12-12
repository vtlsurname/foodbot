from main import bot, dp 
from base.bd_funcs import set_message_id, get_message_id, delete_chef_from_database, get_chef_list_from_database
from aiogram.types import Message
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from base.bd_funcs import add_new_chef_func
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from inline_keyboard.main_board import get_main_menu


class NewChef(StatesGroup):
    user_id = State()
    user_name = State()

@dp.message_handler(text='Додати кухаря')
async def add_new_chef(message: Message):
    await message.answer(text='Напишіть ID людини, яку ви хочете додати новим кухарем (/myid)\nАбо напишіть cencel для відміни')
    await NewChef.user_id.set()

@dp.message_handler(state=NewChef.user_id)
async def get_user_id(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'cencel':
            await state.finish()
            await message.answer(text='Дію було відмінено, напишіть /start')
        else:
            try:
                data['user_id'] = int(message.text)
                await message.answer(text="Напишіть ім'я працівника\nАбо напишіть cancel для відміни")
                await NewChef.next()
            except ValueError:
                await message.answer(text='Будь ласка, введіть числове значення або напишіть cancel для відміни')

@dp.message_handler(state=NewChef.user_name)
async def get_user_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'cencel':
            await state.finish()
            await message.answer(text='Дію було відмінено, напишіть /start')
        else:
            data['user_name'] = message.text
            answer = add_new_chef_func(user_id=data['user_id'], user_name=data['user_name'])
            await message.answer(text=answer)
            await state.finish()


class ChefDeletion(StatesGroup):
    chef_name = State()
    confirmation = State()

@dp.message_handler(text='Видалити кухаря')
async def delete_chef_start(message: types.Message):
    chefs = get_chef_list_from_database()

    if not chefs:
        await message.answer("Немає кухарів, яких можна видалити.")
        return

    keyboard = InlineKeyboardMarkup()
    for chef in chefs:
        keyboard.add(InlineKeyboardButton(chef, callback_data=chef))
    
    msg = await message.answer("Якого кухаря ви хочете видалити?", reply_markup=keyboard)
    set_message_id(user_id=message.from_id, message_id=msg['message_id'])

    await ChefDeletion.chef_name.set()

@dp.callback_query_handler(lambda c: c.data, state=ChefDeletion.chef_name)
async def delete_chef_selected(callback_query: types.CallbackQuery, state: FSMContext):
    chef_name = callback_query.data
    user_id = callback_query.from_user.id
    await state.update_data(chef_name=chef_name)
    
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton('Так', callback_data='yes'),
        InlineKeyboardButton('Ні', callback_data='no')
    )
    message = await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=get_message_id(user_id),text=f"Ви впевнені, що хочете видалити {chef_name}? Будь ласка, дайте відповідь 'так' або 'ні'.")
    
    
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id, message_id=message.message_id, reply_markup=keyboard)
    await ChefDeletion.confirmation.set()


@dp.callback_query_handler(lambda c: c.data in ['yes', 'no'], state=ChefDeletion.confirmation)
async def delete_chef_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    menu = get_main_menu()
    user_id = callback_query.from_user.id
    message_id = get_message_id(user_id)
    
    if callback_query.data == 'yes':
        data = await state.get_data()
        chef_name = data['chef_name']
        delete_chef_from_database(chef_name)
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=f"{chef_name} has been deleted.", reply_markup=menu)
    else:
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text="Chef deletion has been cancelled.", reply_markup=menu)
    await state.finish()
