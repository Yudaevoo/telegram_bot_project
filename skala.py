import telebot
import random


def get_list_of_words(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()


words = get_list_of_words('words.txt')
images = ['stick_1.png', 'stick_2.png', 'stick_3.png', 'stick_4.png',
          '1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png']
bot = telebot.TeleBot('5707691226:AAG6wIp3HFaw7RDMxR96_efTthiRiP7Rt1U')
username = ''


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Привет, меня зовут Gallows Bot!")
    bot.send_message(message.from_user.id, "Как вас зовут?")
    bot.register_next_step_handler(message, step_1)


def step_1(message):
    global username
    username = message.text
    bot.send_message(message.from_user.id, f"Приятно познакомиться, {username}!")
    bot.send_message(message.from_user.id, '''Сыграем в игру "Виселица"''')
    bot.send_message(message.from_user.id, "Чтобы узнать правила, напишите /rules.")


@bot.message_handler(commands=['rules'])
def rules(message):
    global images
    if message.text == "/rules":
        bot.send_message(message.from_user.id, "Правила просты: Я загадываю слово, у вас есть несколько ходов, \
чтобы его отгадать. Если отгадаете букву, я её открою. В противном случае - дорисую одну палочку на эту картинку. \
У вас есть 10 попыток, чтобы отгадать слово!")

        bot.send_photo('1327245563', open(images[0], 'rb'))
        bot.send_message(message.from_user.id, "Если готовы сыграть, нажмите /play!")


@bot.message_handler(commands=['play'])
def play(message):
    global n, random_word, secret_word, used_letters, guessed_letters, images
    n = 10
    random_word = random.choice(words).upper()
    secret_word = ''
    used_letters = []
    guessed_letters = []
    secret_word = '🔴' * len(random_word)
    if message.text == "/play":
        bot.send_message(message.from_user.id, secret_word)
    bot.register_next_step_handler(message, letters)


@bot.message_handler(content_types=['text'])
def letters(message):
    global secret_word, random_word
    global n, images, new_word
    word = secret_word
    letter = message.text
    if len(letter) != 1:
        bot.send_message(message.from_user.id, 'Так нечестно! Вы ввели больше одной буквы!')
    elif letter.lower() not in 'ёйцукенгшщзхъфывапролджэячсмитьбю':
        bot.send_message(message.from_user.id, 'Так нечестно! Вы ввели символ, не являющийся буквой русского алфавита!')
    elif letter.upper() in used_letters:
        bot.send_message(message.from_user.id, 'Вы уже использовали эту букву!')
    elif letter.upper() not in random_word.upper():
        bot.send_message(message.from_user.id, 'Такой буквы нет в слове!')
        n -= 1
        bot.send_photo('1327245563', open(images[10 - n], 'rb'))
        used_letters.append(letter.upper())
    elif letter.upper() in random_word:
        guessed_letters.append(letter.upper())
        used_letters.append(letter.upper())
        new_word = ''
        for elem in random_word:
            if elem in guessed_letters:
                new_word += elem.upper()
            else:
                new_word += '🔴'
        word = new_word
        bot.send_message(message.from_user.id, new_word)
    if '🔴' not in word:
        bot.send_message(message.from_user.id, 'Поздравляю! Вы отгадали слово!')
        bot.send_message(message.from_user.id, 'Нажмите /play, чтобы сыграть ещё!')
        n = 6

    if n == 0:
        bot.send_message(message.from_user.id, 'К сожалению, попытки закончились! Вы проиграли! :(')
        bot.send_message(message.from_user.id, f'Я загадал слово {random_word.upper()}')
        bot.send_message(message.from_user.id, 'Нажмите /play, чтобы сыграть ещё!')
        n = 6


if __name__ == '__main__':
    bot.polling(none_stop=True)
