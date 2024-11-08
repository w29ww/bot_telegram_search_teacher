import telebot
import os


TOKEN = '7560968618:AAExeTUxQwIXh5BTGrNB9YbChpORNv41ejQ'
bot = telebot.TeleBot(TOKEN)
teachers = {}  # Словарь для хранения информации об учителях
authorized = False  # Флаг авторизации

@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, "Привет! Я бот для поиска учителей и кабинетов. "
                   "Введите /help для получения списка команд.")

@bot.message_handler(commands=['help'])
def send_help(message):
  bot.reply_to(message, "Доступные команды:\n"
                   "/add - добавить учителя\n"
                   "/find_by_room - найти учителя по номеру кабинета\n"
                   "/find_by_name - найти кабинет по имени учителя")

@bot.message_handler(func=lambda message: message.text == "kxojlvvxzjhwhrql" and not authorized)
def authorize(message):
  """Авторизует пользователя для добавления учителя."""
  global authorized
  authorized = True
  bot.reply_to(message, "Авторизация прошла успешно! Теперь вы можете добавлять учителей.")

@bot.message_handler(func=lambda message: message.text == "/add" and authorized)
def add_teacher(message):
  """Добавляет учителя и его кабинет в словарь."""
  bot.reply_to(message, "Введите имя учителя:")
  bot.register_next_step_handler(message, get_teacher_name)

def get_teacher_name(message):
  """Получает имя учителя."""
  name = message.text
  bot.reply_to(message, "Введите номер кабинета:")
  bot.register_next_step_handler(message, lambda m: add_teacher_to_dict(m, name))

def add_teacher_to_dict(message, name):
  """Добавляет учителя в словарь."""
  room = message.text
  teachers[name] = room
  bot.reply_to(message, f"Учитель {name} добавлен в кабинет {room}.")
  send_help(message)  # Выводит справку после добавления учителя

@bot.message_handler(commands=['find_by_room'])
def find_teacher_by_room(message):
  """Находит учителя по номеру кабинета."""
  bot.reply_to(message, "Введите номер кабинета:")
  bot.register_next_step_handler(message, find_teacher)

def find_teacher(message):
  """Находит учителя по номеру кабинета."""
  room = message.text
  for name, teacher_room in teachers.items():
    if teacher_room == room:
      bot.reply_to(message, f"Учитель в кабинете {room}: {name}")
      send_help(message)  # Выводит справку после поиска учителя
      return
  bot.reply_to(message, f"Учитель в кабинете {room} не найден.")
  send_help(message)  # Выводит справку, если учителя не нашли

@bot.message_handler(commands=['find_by_name'])
def find_room_by_teacher(message):
  """Находит кабинет по имени учителя."""
  bot.reply_to(message, "Введите имя учителя:")
  bot.register_next_step_handler(message, find_room)

def find_room(message):
  """Находит кабинет по имени учителя."""
  name = message.text
  if name in teachers:
    bot.reply_to(message, f"Кабинет учителя {name}: {teachers[name]}")
  else:
    bot.reply_to(message, f"Учитель {name} не найден.")
  send_help(message)  # Выводит справку после поиска кабинета

@bot.message_handler(func=lambda message: message.text == "/add" and not authorized)
def request_password(message):
  """Просит ввести пароль."""
  bot.reply_to(message, "Введите пароль для авторизации:")
  bot.register_next_step_handler(message, authorize)

bot.polling(none_stop=True)