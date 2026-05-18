import telebot
import json
import os

from telebot import types
TOKEN = "8764413258:AAFk6AtNhyWvu7MDcrkpNIbSzDE8l_Oh13k"
bot = telebot.TeleBot(TOKEN)
FILE = "notes.json"
data = {}

def load():
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump([], f)
    with open(FILE, "r", encoding="utf-8") as f:
        return json,load(f)
    
def save(notes):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump (notes, f, ensure_ascii=False, indent=4)


def menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📄 Список")
    kb.add("➕ Создать")
    kb.add("✏ Рудактировать")
    kb.add("❌ Удалить")
    kb.add("ℹ Помощь")
    
    return kb

@bot.message_handler(commands=["start"])
def start(message):

    bot.send_message(
        message.chat.id,
        "Бот заметок",
        reply_markup=menu()
    )

@bot.message_handler(func=lambda m: m.text == "Помощь")
def help(message):
    bot.send_message(
        message.chat.id,
        "📄 Список\n"
        "➕ Создать\n"
        "✏ Рудактировать\n"
        "❌ Удалить\n"
        "ℹ Помощь"
    )

@bot.message_handler(func=lambda m: m.text == "Создать")
def create(message):
    msg = bot.send_message(
        message.chat.id,
        "Название:"
    )

    bot.register_next_step_handler(
        msg,
        title
    )

def title(message):
    data["title"] = message.text

    msg = bot.send_message(
        message.chat.id,
        "Текст:"
    )

    bot.register_next_step_handler(
        msg,
        text
    )

def text(message):
    notes = load()
    note = {
        "id": len(notes) + 1,
        "title": data["title"],
        "text": message.text
    }
    notes.append(note)
    save(notes)
    bot.send_message(
        message.chat.id,
        "Сохранено",
        reply_markup=menu()
    )

@bot.message_handler(func=lambda m: m.text == "Список")
def show(message):
    notes = load()
    if not notes:
        bot.send_message(
            message.chat.id,
            "Пусто"
        )
        return
    for note in notes:
        bot.send_message(
            message.chat.id,
            f"{note['id']}. "
            f"{note['title']}\n"
            f"{note['text']}"
        )

@bot.message_handler(func=lambda m: m.text == "Редактировать")
def edit_note(message):
    notes = load_notes()

    if not notes:
        bot.send_message(
            message.chat.id,
            "Нет заметок"
        )
        return
    
    text = "Введите ID заметки:\n\n"

    for note in notes:
        text += f"{note['id']} - {note['title']}\n"
    
    msg = bot.send_message(
        message.chat.id,
        text
    )
    bot.register_next_step_handler(
        msg,
        get_edit_id
    )
def get_edit_id(message):
    user_data[message.chat.id] = {
        "edit_id": int(message.text)
    }
    msg = bot.send_message(
        message.chat.id,
        "Новое название:"
    )
    bot.register_next_step_handler(
        msg,
        get_new_title
    )
def get_new_title(message):
    user_data[message.chat.id]["new_title"] = message.text
    msg = bot.send_message(
        message.chat.id,
        "Новый текст:"
    )
    bot.register_next_step_handler(
        msg,
        get_new_text
    )

def het_new_text(message):
    notes = load_notes()
    note_id = user_data[message.chat.id]["edit_id"]
    for note in notes:
        if note["id"] == note_id:
            note["title"] = user_data[message.chat.id]["new_title"]
            note["text"] = message.text
    save_notes(notes)
    bot.send_message(
        message.chat.id,
        "Заметка обновлеа",
        reply_markup=menu()
    )

bot.infinity_polling()