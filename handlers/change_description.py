from main import bot, dp 
from aiogram.types import Message
from cfg import admin_id
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from base.dishes_funcs import change_dish_description
from inline_keyboard.dishes_board import get_categories_menu_for_edit_desc, get_dishes_menu_for_edit_desc
from base.bd_funcs import set_message_id, get_message_id
from aiogram.types import CallbackQuery
from inline_keyboard.main_board import get_main_menu


#--- CHANGE DESC --- 
@dp.message_handler(text='Змінити опис')
async def edit_desc_dish_func(message:Message):
    user_id = message.from_user.id

    categories_menu = get_categories_menu_for_edit_desc()
    
    await bot.delete_message(chat_id=user_id, message_id=get_message_id(user_id))
    msg = await bot.send_message(chat_id=user_id, text='Спочатку виберіть категорію', reply_markup=categories_menu)
    set_message_id(user_id=user_id, message_id=int(msg["message_id"]))

@dp.callback_query_handler(text_contains='edit_desc_food_categori_')
async def edit_desc_dish_funcc(call: CallbackQuery):
    data = call.data
    user_id = call.from_user.id
    categori_name = data.replace('edit_desc_food_categori_', '')
    msg_id = get_message_id(user_id)


    menu = get_dishes_menu_for_edit_desc(categori_name)
    await bot.edit_message_text(message_id=msg_id, chat_id=user_id, text=f'Виберіть страву для якої ви хочете змінити опис', reply_markup=menu)

class change_desc_dish(StatesGroup):
    new_desc = State()
dish_name_for_desc = ''


@dp.callback_query_handler(text_contains='edit_desc_food_')
async def edit_desc_dish_func_end(call: CallbackQuery):
    global dish_name_for_desc
    data = call.data
    dish_name_for_desc = data.replace('edit_desc_food_', '')
    user_id = call.from_user.id
    msg_id = get_message_id(user_id)

    await bot.edit_message_text(message_id=msg_id, chat_id=user_id, text=f'Відправте новий опис до товару')
    await change_desc_dish.new_desc.set()

@dp.message_handler(state=change_desc_dish.new_desc)
async def handle_docs_desc(message: Message, state: FSMContext):
    global dish_name_for_desc
    user_id = message.from_id
    msg_id=get_message_id(user_id)

    new_desc = message.text

    try:
        answer = change_dish_description(dish_name=dish_name_for_desc, new_desc=new_desc)

        menu = get_main_menu()
        await bot.delete_message(chat_id=user_id, message_id=msg_id)

        msg = await bot.send_message(chat_id=user_id, text=answer, reply_markup=menu)
        set_message_id(user_id=user_id, message_id=int(msg['message_id']))

    except Exception as ex:
        await message.answer(text=ex)

    
    await state.finish()
