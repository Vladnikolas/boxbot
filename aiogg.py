import json
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

logging.basicConfig(level=logging.INFO)

# Замените TOKEN на токен вашего бота
bot = Bot("6200644854:AAEZ6FAsqSJnbKVPnTTihlDRiWYWDfBBCvI")
dp = Dispatcher(bot)

jdgs = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
j1=KeyboardButton('Владислав Николенко')
j2=KeyboardButton('Александр Николенко')
j3=KeyboardButton('Елизавета Косенко')
j4=KeyboardButton('Георгий Понятенко')
j5=KeyboardButton('Станислав Карандей')
j6=KeyboardButton('Иван Гринь')
j7=KeyboardButton('Виктор Скоморохов')
j8=KeyboardButton('Андрей Яковенко')
j9=KeyboardButton('Артур Беладзе')
j10=KeyboardButton('Павел Василинчук')
j11=KeyboardButton('Вадим Гойтенюк')
j12=KeyboardButton('Владимир Кладько')
j13=KeyboardButton('Соколов Руслан')
j14=KeyboardButton('Анатолий Новоселец')
j15=KeyboardButton('Дмитрий Лазарев')
j16=KeyboardButton('Александр Власенко')
j17=KeyboardButton('Михаил Стахнив')
j18=KeyboardButton('Роман Чернышов')
j19=KeyboardButton('Сухебатор Жигжжавин')
j20=KeyboardButton('Антон Каракулов')
jdgskb = jdgs.add(j1, j2, j3, j4, j5, j6, j7, j8, j9, j10, j11, j12, j13, j14, j15, j16, j17, j18, j19, j20)
# Словарь для хранения данных о боях
fights_data = {}

# Функция для сохранения данных о боях в файл
def save_fights_data(fights_data):
    with open("fights_data.json", "w") as f:
        json.dump(fights_data, f)

# Функция для загрузки данных о боях из файла
def load_fights_data():
    global fights_data
    try:
        with open("fights_data.json", "r") as f:
            fights_data = json.load(f)
    except FileNotFoundError:
        pass

# Загрузка данных о боях из файла при запуске бота
load_fights_data()

# Ловим нажатие кнопки "Начать новый бой"
@dp.callback_query_handler(lambda query: query.data == "new_rating")
async def process_callback_new_rating(query: types.CallbackQuery):
    # Вызов функции обработки команды /start
    await start_cmd_handler(query.message)
    await bot.answer_callback_query(query.id)

# Создаём клавиатуру
def generate_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for i in range(1, 41):
        button = KeyboardButton(str(i))
        row.append(button)
        if i % 6 == 0:
            kb.add(*row)
            row = []
    if row:
        kb.add(*row)
    return kb

@dp.message_handler(commands=['start'])
async def start_cmd_handler(message: types.Message):
    chat_id = message.chat.id
    if chat_id in fights_data:
        del fights_data[chat_id]
    fights_data[chat_id] = {}
    kb = generate_keyboard()
    await message.answer("Введіть номер двобою", reply_markup=kb)

@dp.message_handler(lambda message: "fight_number" not in fights_data[message.chat.id])
async def fight_number_handler(message: types.Message):
    chat_id = message.chat.id
    fight_number = int(message.text)
    fights_data[chat_id]["fight_number"] = fight_number
    await message.answer("Оберіть, або введіть прізвище та ім'я судді:", reply_markup=jdgskb)

@dp.message_handler(lambda message: "judge_name" not in fights_data[message.chat.id])
async def judge_name_handler(message: types.Message):
    chat_id = message.chat.id
    judge_name = message.text
    fights_data[chat_id]["judge_name"] = judge_name
    if "judge_name" not in fights_data[chat_id]:
        return
        await message.answer("Оберіть, або введіть прізвище та ім'я судді", reply_markup=jdgskb)
    else:
        fight_number = fights_data[chat_id]["fight_number"]
        if fight_number in fights_data[chat_id]:
            await message.answer(f"Результаты боя №{fight_number} уже сохранены. Пожалуйста, введите другой номер боя.")
        else:
            fights_data[chat_id][fight_number] = {}
            keyboard = InlineKeyboardMarkup(resize_keyboard=False)
            keyboard.row(InlineKeyboardButton("10", callback_data=f"{fight_number}_1_red_10"), InlineKeyboardButton("9", callback_data=f"{fight_number}_1_red_9"))
            keyboard.row(InlineKeyboardButton("8", callback_data=f"{fight_number}_1_red_8"),InlineKeyboardButton("7", callback_data=f"{fight_number}_1_red_7"))
            keyboard.row(InlineKeyboardButton("KO", callback_data=f"{fight_number}_KO"))
            keyboard.row(InlineKeyboardButton("RSC", callback_data=f"{fight_number}_RSC"), InlineKeyboardButton("RSC-I", callback_data=f"{fight_number}_RSC-I"))
            keyboard.row(InlineKeyboardButton("ABD", callback_data=f"{fight_number}_ABD"), InlineKeyboardButton("DSQ", callback_data=f"{fight_number}_DSQ"))
            await message.answer(f"🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥\nРаунд 1. Оцініть боксера \nчервоного кута:\n🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥", reply_markup=keyboard)

@dp.callback_query_handler()
async def callback_query_handler(query: types.CallbackQuery):
    data = query.data.split("_")
    chat_id = query.message.chat.id
    fight_number = int(data[0])
    if len(data) == 2:
        # Досрочное завершение боя
        result = data[1]
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton("Червоний кут", callback_data=f"{fight_number}_{result}_червоного"), InlineKeyboardButton("Синій кут", callback_data=f"{fight_number}_{result}_синього"))
        await query.message.edit_text(f"Переможець у зв'язку з {result}:", reply_markup=keyboard)
    elif len(data) == 3:
        # Победитель досрочного завершения боя
        result = data[1]
        winner = data[2]
        red_total = 0
        blue_total = 0
        rounds_text = ""
        for round_number, round_data in fights_data[chat_id][fight_number].items():
                    red_score = round_data["red"]
                    blue_score = round_data["blue"]
                    red_total += red_score
                    blue_total += blue_score
                    rounds_text += f"\nРаунд {round_number}            |            {red_score}:{blue_score}"
        judge_name = fights_data[chat_id]["judge_name"]
        text = f"🥊Двобій номер - {fight_number}\n👨‍⚖️Суддя-{judge_name}\n{rounds_text}\n\nВсього-{red_total}🔴:🔵{blue_total}\nПеремога {winner} кута у зв'язку з {result}"
        # Создание кнопки
        button = InlineKeyboardButton("Почати нову оцінку", callback_data="new_rating")
        # Создание клавиатуры
        nr = InlineKeyboardMarkup().add(button)
        await query.message.edit_text(text, reply_markup=nr)
        # Отправка результата в указанный чат (замените CHAT_ID на ID чата)
        await bot.send_message(chat_id=807894109, text=text)
        save_fights_data(fights_data)
    else:
        round_number = int(data[1])
        corner = data[2]
        score = int(data[3])
        if round_number not in fights_data[chat_id][fight_number]:
            fights_data[chat_id][fight_number][round_number] = {}
        fights_data[chat_id][fight_number][round_number][corner] = score
        if corner == "red":
            # Оценка синего угла
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.row(InlineKeyboardButton("10", callback_data=f"{fight_number}_{round_number}_blue_10"), InlineKeyboardButton("9", callback_data=f"{fight_number}_{round_number}_blue_9"))
            keyboard.row(InlineKeyboardButton("8", callback_data=f"{fight_number}_{round_number}_blue_8"), InlineKeyboardButton("7", callback_data=f"{fight_number}_{round_number}_blue_7"))
            keyboard.row(InlineKeyboardButton("KO", callback_data=f"{fight_number}_KO"))
            keyboard.row(InlineKeyboardButton("RSC", callback_data=f"{fight_number}_RSC"), InlineKeyboardButton("RSC-I", callback_data=f"{fight_number}_RSC-I"))
            keyboard.row(InlineKeyboardButton("ABD", callback_data=f"{fight_number}_ABD"), InlineKeyboardButton("DSQ", callback_data=f"{fight_number}_DSQ"))
            await query.message.edit_text(f"🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦\nРаунд {round_number}. Оцініть боксера \nсинього кута:\n🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦", reply_markup=keyboard)
        else:
            if round_number < 3:
                # Следующий раунд
                next_round = round_number + 1
                keyboard = InlineKeyboardMarkup(resize_keyboard=True)
                keyboard.row(InlineKeyboardButton("10", callback_data=f"{fight_number}_{next_round}_red_10"), InlineKeyboardButton("9", callback_data=f"{fight_number}_{next_round}_red_9"))
                keyboard.row(InlineKeyboardButton("8", callback_data=f"{fight_number}_{next_round}_red_8"), InlineKeyboardButton("7", callback_data=f"{fight_number}_{next_round}_red_7"))
                keyboard.row(InlineKeyboardButton("KO", callback_data=f"{fight_number}_KO"))
                keyboard.row(InlineKeyboardButton("RSC", callback_data=f"{fight_number}_RSC"), InlineKeyboardButton("RSC-I", callback_data=f"{fight_number}_RSC-I"))
                keyboard.row(InlineKeyboardButton("ABD", callback_data=f"{fight_number}_ABD"), InlineKeyboardButton("DSQ", callback_data=f"{fight_number}_DSQ"))
                await query.message.edit_text(f"🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥\nРаунд {next_round}. Оцініть боксера \nчервоного кута:\n🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥", reply_markup=keyboard)
            else:
                    # Конец боя
                    red_total = 0
                    blue_total = 0
                    rounds_text = ""
                    for round_number, round_data in fights_data[chat_id][fight_number].items():
                        red_score = round_data["red"]
                        blue_score = round_data["blue"]
                        red_total += red_score
                        blue_total += blue_score
                        rounds_text += f"\nРаунд {round_number}            |            {red_score}:{blue_score}"
                        if red_total == blue_total:
                            result = f"рівною кількістю балів"
                            keyboard = InlineKeyboardMarkup()
                            keyboard.row(InlineKeyboardButton("Червоний кут", callback_data=f"{fight_number}_{result}_червоного"), InlineKeyboardButton("Синій кут", callback_data=f"{fight_number}_{result}_синього"))
                            await query.message.edit_text(f"Равное количество очков. Определите победителя.", reply_markup=keyboard)
                            save_fights_data(fights_data)
                        else:
                            judge_name = fights_data[chat_id]["judge_name"]
                            text = f"🥊Двобій номер - {fight_number}\n👨‍⚖️Суддя-{judge_name}\n{rounds_text}\n\nВсього-{red_total}🔴:🔵{blue_total}"
                            # Создание кнопки
                            button = InlineKeyboardButton("Почати нову оцінку", callback_data="new_rating")
                            # Создание клавиатуры
                            nr = InlineKeyboardMarkup().add(button)
                            await bot.send_message(chat_id=807894109, text=text)
                            await query.message.edit_text(text, reply_markup=nr)
                            # Сохранение данных о боях в файл
                            save_fights_data(fights_data)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
