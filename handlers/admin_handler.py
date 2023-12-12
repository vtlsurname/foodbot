from main import bot, dp 
from aiogram.types import Message
from keyboard.admin_kb import admin_menu, dishes_menu
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from inline_keyboard.dishes_board import get_categories_menu_for_adding_new_dish, get_categories_menu
from aiogram.types import CallbackQuery
from base.dishes_funcs import is_dish_in_bd, add_new_dish_in_bd, delete_dish
from base.bd_funcs import set_message_id, get_message_id, add_new_categori, delete_categori, change_price
from inline_keyboard.dishes_board import get_categories_menu_for_delete_dish, get_dishes_menu_for_delete, categories_menu_for_delete_cat
from inline_keyboard.main_board import get_main_menu
from inline_keyboard.dishes_board import get_categories_menu_for_edit_photo, get_dishes_menu_for_edit_photo
from inline_keyboard.dishes_board import get_categories_menu_for_edit_price, get_dishes_menu_for_edit_price
from base.dishes_funcs import change_dish_description
from inline_keyboard.dishes_board import get_categories_menu_for_edit_desc, get_dishes_menu_for_edit_desc
from base.bd_funcs import get_admin_ids_from_database
import os


@dp.message_handler(commands='admin')
async def repyl_admin_menu(message: Message):
    user_id = message.from_id
    admin_ids = get_admin_ids_from_database()

    if user_id in admin_ids:
        await message.answer(text='Ви перейшли в адмін меню', reply_markup=admin_menu)
    else:
        await message.answer(text='Ви не адмін!')


@dp.message_handler(text='Назад у меню')
async def back_in_user_menu(message: Message):
    user_id = message.from_id
    admin_ids = get_admin_ids_from_database()

    if user_id in admin_ids:
        await message.answer(text='Ви перешли у голвне меню', reply_markup=admin_menu)
    else:
        await message.answer(text='Ви не адмін')


@dp.message_handler(text='Налаштування страв')
async def reply_dishes_menu(message: Message):
    user_id = message.from_id
    admin_ids = get_admin_ids_from_database()

    if user_id in admin_ids:
        await message.answer(text='Ви перейшли у меню страви', reply_markup=dishes_menu)
    else:
        await message.answer(text='Ви не адмін!')




# --- ADD NEW DISH ---

class add_new_dish_class(StatesGroup):
        categori_name = State()
        dish_name = State()
        dish_photo = State()
        dish_description = State()
        dish_price = State()
categori_name = ''
dish_name = ''
dish_description = ''

@dp.message_handler(text='Додати нову страву')
async def add_new_dish(message: Message):
    user_id = message.from_id
    admin_ids = get_admin_ids_from_database()

    if user_id in admin_ids:
        menu = get_categories_menu_for_adding_new_dish()
        await message.answer(text='Виберіть категорію у яку ви хочете додати нову страву.', reply_markup=menu)
    else:
        await message.answer(text='Ви не адмін!')

@dp.callback_query_handler(text_contains='new_food_categori_')
async def add_new_dish(call: CallbackQuery):
    global categori_name
    data=call.data
    categori_name = data.replace('new_food_categori_', '')
    user_id = call.from_user.id
    
    await bot.send_message(user_id, text='Напишіть назву продукту.\nЩоб відмінити напишіть: cencel')
    await add_new_dish_class.dish_name.set()

@dp.message_handler(state=add_new_dish_class.dish_name)
async def get_name_new_dish(message: Message, state: FSMContext):
    global dish_name
    dish_name=message.text
    
    if dish_name == 'cencel':
        await message.answer(text='Дія завершена.', reply_markup=admin_menu)
        await state.finish()
    else: 
        await message.answer(text='Відправте фото для товару або напишіть cencel(додасте фото пізніше)')
        await add_new_dish_class.dish_photo.set()


@dp.message_handler(content_types=['photo'], state=add_new_dish_class.dish_photo)
async def handle_docs_photo(message: Message):
    global dish_name
    try:
        await message.photo[-1].download(destination_file=f'images/{dish_name}.png')
        await bot.send_message(chat_id=message.from_id, text="Напишіть опис для нового товару(обов'язково)")
        await add_new_dish_class.dish_description.set()
    except Exception as ex:
        await message.answer(text=ex)


@dp.message_handler(state=add_new_dish_class.dish_photo)
async def if_not_photo(message:Message):
    global dish_photo
    if message.text=='cencel':
        dish_name='None'
        await bot.send_message(chat_id=message.from_id, text="Напишіть опис для нового товару(обов'язково)")
        await add_new_dish_class.dish_description.set()

@dp.message_handler(state=add_new_dish_class.dish_description)
async def get_description(message:Message, state:FSMContext):
    global dish_description
    user_id = message.from_id
    dish_description = message.text

    await bot.send_message(chat_id=user_id, text='Напишіть ціну для нового товару')
    await add_new_dish_class.dish_price.set()

@dp.message_handler(state=add_new_dish_class.dish_price)
async def get_price_new_dish(message: Message, state:FSMContext):
    global categori_name, dish_name, dish_description
    dish_price = message.text
    
    check_dish = is_dish_in_bd(dish_name)
    if check_dish==1:
        await message.answer(text='Виникла помилка, можливо ця страва вже є у меню.', reply_markup=admin_menu)
    elif dish_price=='cencel':
        await message.answer(text='Дія завершена.', reply_markup=admin_menu)
        await state.finish()
    else:
        try:
            add_new_dish_in_bd(categori=categori_name, dish_name=dish_name, price=dish_price, img_url=dish_name, description=dish_description)
            await message.answer(text='Страву було успішно додано!', reply_markup=admin_menu)
            await state.finish()
        except Exception as ex:
            await message.answer(text='Виникла помилка при додаванні страви до бази данних.', reply_markup=admin_menu)
            await state.finish()
            print(ex)




# --- DELETIGN DISH ---
@dp.message_handler(text='Видалити страву')
async def delete_dish_func(message:Message):
    user_id = message.from_user.id

    categories_menu = get_categories_menu_for_delete_dish() # получаем клавиатуру Категорий
    
    await bot.delete_message(chat_id=user_id, message_id=get_message_id(user_id))
    msg = await bot.send_message(chat_id=user_id, text='Спочатку виберіть категорію', reply_markup=categories_menu) # делаем переменную для сохранения айди сообщения
    set_message_id(user_id=user_id, message_id=int(msg["message_id"])) # обновляем меседж айди



@dp.callback_query_handler(text_contains='delete_food_categori_')
async def delet_dish_funcc(call: CallbackQuery):
    data = call.data
    user_id = call.from_user.id
    categori_name = data.replace('delete_food_categori_', '')
    msg_id = get_message_id(user_id)


    menu = get_dishes_menu_for_delete(categori_name)
    await bot.edit_message_text(message_id=msg_id, chat_id=user_id, text=f'Виберіть страву', reply_markup=menu)


@dp.callback_query_handler(text_contains='delete_food_')
async def delet_dish_func_end(call: CallbackQuery):
    data = call.data
    dish_name = data.replace('delete_food_', '')
    user_id = call.from_user.id
    msg_id = get_message_id(user_id)

    try:
        delete_dish(dish_name)
        menu = get_categories_menu()
        # await bot.send_message(chat_id=call.from_user.id, text='Страву було успішно видалено.', reply_markup=menu)
        await bot.edit_message_text(message_id=msg_id, chat_id=user_id, text=f'Страва була видалена✔', reply_markup=menu)

    except Exception as ex:
        print(ex)


# --- EDIT DISH PHOTO---
@dp.message_handler(text='Змінити фото')
async def edit_photo_dish_func(message:Message):
    user_id = message.from_user.id

    categories_menu = get_categories_menu_for_edit_photo() # получаем клавиатуру Категорий
    
    await bot.delete_message(chat_id=user_id, message_id=get_message_id(user_id))
    msg = await bot.send_message(chat_id=user_id, text='Спочатку виберіть категорію щоб змінити фото', reply_markup=categories_menu) # делаем переменную для сохранения айди сообщения
    set_message_id(user_id=user_id, message_id=int(msg["message_id"])) # обновляем меседж айди


@dp.callback_query_handler(text_contains='edit_photo_food_categori_')
async def edit_photo_dish_funcc(call: CallbackQuery):
    data = call.data
    user_id = call.from_user.id
    categori_name = data.replace('edit_photo_food_categori_', '')
    msg_id = get_message_id(user_id)


    menu = get_dishes_menu_for_edit_photo(categori_name)
    await bot.edit_message_text(message_id=msg_id, chat_id=user_id, text=f'Виберіть страву для якої ви хочете змінити фото', reply_markup=menu)

class change_photo_dish(StatesGroup):
    photo = State()
dish_name_for_photo = ''

@dp.callback_query_handler(text_contains='edit_photo_food_')
async def edit_photo_dish_func_end(call: CallbackQuery):
    global dish_name_for_photo
    data = call.data
    dish_name_for_photo = data.replace('edit_photo_food_', '')
    user_id = call.from_user.id
    msg_id = get_message_id(user_id)

    await bot.edit_message_text(message_id=msg_id, chat_id=user_id, text=f'Відправте нове фото для товару')
    await change_photo_dish.photo.set()

@dp.message_handler(content_types=['photo'], state=change_photo_dish.photo)
async def handle_docs_photo(message: Message, state: FSMContext):
    global dish_name_for_photo
    user_id = message.from_id
    msg_id=get_message_id(user_id)
    
    try:
       os.remove(f'images/{dish_name_for_photo}.png')
    except:
        pass

    try:
        await message.photo[-1].download(destination_file=f'images/{dish_name_for_photo}.png')       
        
        try:
            await bot.delete_message(chat_id=user_id, message_id=msg_id)
        except:
            pass
        
        menu = get_main_menu()
        msg = await bot.send_message(chat_id=user_id, text='Фото було успішно оновлено', reply_markup=menu)
        set_message_id(user_id=user_id, message_id=int(msg["message_id"]))

        await state.finish()
        
    except Exception as ex:
        await message.answer(text=ex)


#--- CHANGE PRICE --- 
@dp.message_handler(text='Змінити ціну')
async def edit_photo_dish_func(message:Message):
    user_id = message.from_user.id

    categories_menu = get_categories_menu_for_edit_price() # получаем клавиатуру Категорий
    
    await bot.delete_message(chat_id=user_id, message_id=get_message_id(user_id))
    msg = await bot.send_message(chat_id=user_id, text='Спочатку виберіть категорію', reply_markup=categories_menu) # делаем переменную для сохранения айди сообщения
    set_message_id(user_id=user_id, message_id=int(msg["message_id"])) # обновляем меседж айди

@dp.callback_query_handler(text_contains='edit_price_food_categori_')
async def edit_photo_dish_funcc(call: CallbackQuery):
    data = call.data
    user_id = call.from_user.id
    categori_name = data.replace('edit_price_food_categori_', '')
    msg_id = get_message_id(user_id)


    menu = get_dishes_menu_for_edit_price(categori_name)
    await bot.edit_message_text(message_id=msg_id, chat_id=user_id, text=f'Виберіть страву для якої ви хочете змінити ціну', reply_markup=menu)

class change_price_dish(StatesGroup):
    new_price = State()
dish_name_for_price = ''

@dp.callback_query_handler(text_contains='edit_price_food_')
async def edit_photo_dish_func_end(call: CallbackQuery):
    global dish_name_for_price
    data = call.data
    dish_name_for_price = data.replace('edit_price_food_', '')
    user_id = call.from_user.id
    msg_id = get_message_id(user_id)

    await bot.edit_message_text(message_id=msg_id, chat_id=user_id, text=f'Відправте нову ціну для товару')
    await change_price_dish.new_price.set()

@dp.message_handler(state=change_price_dish.new_price)
async def handle_docs_photo(message: Message, state: FSMContext):
    global dish_name_for_price
    user_id = message.from_id
    msg_id=get_message_id(user_id)

    price = message.text

    try:
        change_price(dish_name=dish_name_for_price, new_price=price)

        menu = get_main_menu()
        await bot.delete_message(chat_id=user_id, message_id=msg_id)

        msg = await bot.send_message(chat_id=user_id, text='Ціну товару було успішно змінено!', reply_markup=menu)
        set_message_id(user_id=user_id, message_id=int(msg['message_id']))

    except Exception as ex:
        await message.answer(text=ex)

    
    await state.finish()


# --- ADD NEW CATEGORI --- 
class new_categori_class(StatesGroup):
    categori_name = State()
categori_name=''

@dp.message_handler(text='Додати нову категорію')
async def add_new_categori_func(message:Message):
    user_id = message.from_id
    admin_ids = get_admin_ids_from_database()

    if user_id in admin_ids:
        await message.answer(text='Напишіть назву нової категорії.\nЯкщо ви хочете відмінити, напишіть: cencel')
        await new_categori_class.categori_name.set()
    else:
        await message.answer(text='Ви не адмін!')

@dp.message_handler(state=new_categori_class.categori_name)
async def add_new_categori_end(message:Message, state:FSMContext):
    msg_txt=message.text
    if msg_txt == 'cencel':
        await message.answer(text='Дія завершена.')
        await state.finish()
    else:
        try:
            add_new_categori(msg_txt)
            await message.answer(text='Все прошло успішно, нова категорія додана.')
            await state.finish()
        except Exception as ex:
            print(ex)
            await message.answer(text='Щось пішло не по плану(\nЯ не зміг додати нову категорію.')
            await state.finish()




# --- DELETE CATEGORI --- 
@dp.message_handler(text='Видалити категорію')
async def delete_categori_start(message: Message):
    menu = categories_menu_for_delete_cat()
    await message.answer(text='Виберіть категорії для видалння', reply_markup=menu)

@dp.callback_query_handler(text_contains='delete_categori_')
async def delet_categori_end(call: CallbackQuery):
    data = call.data
    categori_name = data.replace('delete_categori_', '')
    user_id = call.from_user.id
    msg_id = get_message_id(user_id)

    delete_categori(categori_name)
    try:
        await bot.send_message(chat_id=user_id, text='Вдалося видалити категорію!✔')
    except:
        await bot.send_message(chat_id=user_id, text='Не вдалося видалити категорію!❌')


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
