import telebot
import random


def file_reader(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()


words = file_reader('words.txt')
images = ['stick_1.png', 'stick_2.png', 'stick_3.png', 'stick_4.png',
          '1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png']
bot = telebot.TeleBot('5707691226:AAG6wIp3HFaw7RDMxR96_efTthiRiP7Rt1U')
users = {}


@bot.message_handler(commands=['start'])
def start_game(message):
    bot.send_message(message.from_user.id, "Привет, меня зовут Gallows Bot!")
    bot.send_message(message.from_user.id, "Как вас зовут?")
    bot.register_next_step_handler(message, step_1)


def step_1(message):
    username = message.text
    user_data = []
    user_data.append(username)
    users.update({message.from_user.id: user_data})
    bot.send_message(message.from_user.id, f"Приятно познакомиться, {users[message.from_user.id][0]}!")
    bot.send_message(message.from_user.id, '''Сыграем в игру "Виселица"''')
    bot.send_message(message.from_user.id, "Чтобы узнать правила, напишите /rules.")
    bot.register_next_step_handler(message, rules)


@bot.message_handler(commands=['rules'])
def rules(message):
    global images
    if message.text == "/rules":
        bot.send_message(message.from_user.id, "Правила просты: Я загадываю слово, у вас есть несколько ходов, \
чтобы его отгадать. Если отгадаете букву, я её открою. В противном случае - дорисую одну палочку на эту картинку. \
У вас есть 10 попыток, чтобы отгадать слово!")

        bot.send_photo(message.from_user.id, open(images[0], 'rb'))
        bot.send_message(message.from_user.id, "Если готовы сыграть, нажмите /play!")
        bot.register_next_step_handler(message, play)
    else:
        bot.send_message(message.from_user.id, "Чтобы узнать правила, напишите /rules.")
        bot.register_next_step_handler(message, rules)


@bot.message_handler(commands=['play'])
def play(message):
    if message.text == "/play":
        n = 10
        random_word = random.choice(words).upper()
        secret_word = ''
        used_letters = []
        guessed_letters = []
        secret_word = '🔴' * len(random_word)
        users[message.from_user.id].append(random_word)
        users[message.from_user.id].append(secret_word)
        users[message.from_user.id].append(used_letters)
        users[message.from_user.id].append(guessed_letters)
        users[message.from_user.id].append(n)
        bot.send_message(message.from_user.id, users[message.from_user.id][2])
        bot.register_next_step_handler(message, letters)
    else:
        bot.send_message(message.from_user.id, "Если готовы сыграть, нажмите /play!")
        bot.register_next_step_handler(message, play)


@bot.message_handler(content_types=['text'])
def letters(message):
    if message.text == '/start':
        bot.register_next_step_handler(message, start_game)
    else:
        global images
        word = users[message.from_user.id][2]
        letter = message.text
        if len(letter) != 1:
            bot.send_message(message.from_user.id, 'Так нечестно! Вы ввели больше одной буквы!')

        elif letter.lower() not in 'ёйцукенгшщзхъфывапролджэячсмитьбю':
            bot.send_message(message.from_user.id, 'Так нечестно! Вы ввели символ, не являющийся буквой русского алфавита!')

        elif letter.upper() in users[message.from_user.id][3]:
            bot.send_message(message.from_user.id, 'Вы уже использовали эту букву!')

        elif letter.upper() not in users[message.from_user.id][1].upper():
            bot.send_message(message.from_user.id, 'Такой буквы нет в слове!')
            users[message.from_user.id][5] -= 1
            bot.send_photo(message.from_user.id, open(images[10 - users[message.from_user.id][5]], 'rb'))
            users[message.from_user.id][3].append(letter.upper())

        elif letter.upper() in users[message.from_user.id][1]:
            users[message.from_user.id][4].append(letter.upper())
            users[message.from_user.id][3].append(letter.upper())
            new_word = ''
            for elem in users[message.from_user.id][1]:
                if elem in users[message.from_user.id][4]:
                    new_word += elem.upper()
                else:
                    new_word += '🔴'
            word = new_word
            bot.send_message(message.from_user.id, new_word)

        if '🔴' not in word:
            bot.send_message(message.from_user.id, 'Поздравляю! Вы отгадали слово!')
            users[message.from_user.id][5] = 10
            users[message.from_user.id][1] = random.choice(words).upper()
            users[message.from_user.id][2] = ''
            users[message.from_user.id][3] = []
            users[message.from_user.id][4] = []
            users[message.from_user.id][2] = '🔴' * len(users[message.from_user.id][1])
            bot.send_message(message.from_user.id, 'Нажмите /play, чтобы сыграть ещё!')
            bot.register_next_step_handler(message, play)

        if users[message.from_user.id][5] == 0:
            bot.send_message(message.from_user.id, 'К сожалению, попытки закончились! Вы проиграли! :(')
            bot.send_message(message.from_user.id, f'Я загадал слово {users[message.from_user.id][1].upper()}')
            users[message.from_user.id][5] = 10
            users[message.from_user.id][1] = random.choice(words).upper()
            users[message.from_user.id][2] = ''
            users[message.from_user.id][3] = []
            users[message.from_user.id][4] = []
            users[message.from_user.id][2] = '🔴' * len(users[message.from_user.id][1])
            bot.send_message(message.from_user.id, 'Нажмите /play, чтобы сыграть ещё!')
            bot.register_next_step_handler(message, play)


if __name__ == '__main__':
    bot.polling(none_stop=True)
