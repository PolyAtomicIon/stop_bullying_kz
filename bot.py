#from flask import Flask,request
import telebot
from telebot import types
import random
import sys, time
import pickle
import os.path
#import pyexcel
import config
#from oauth2client.service_account import ServiceAccountCredentials


secret = 'sddsfsdfs5lkewepf'
url = 'https://stopbullyingkz.pythonanywhere.com/' + secret

'''
bot = telebot.TeleBot(config.token, threaded = False)

bot.remove_webhook()
bot.set_webhook(url = url)


app = Flask(__name__)
@app.route('/' + secret, methods = ['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

'''
bot = telebot.TeleBot(config.token)

bot.remove_webhook()


contents = config.content

def what_is_ur_name(chat_id):

    print('Hello')
    kb = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True, one_time_keyboard = True)
    btn = ['Что такое буллинг?', 'Как с ним бороться?', 'Права детей', 'Куда обратиться?']
    kb.add(*btn)

    bot.send_message(chat_id, 'StopBullying Bot - это бот для поддержки и информирования подростков в Казахстане🇰🇿💛 Поможет найти выход из трудных ситуаций и понять, что добро всегда побеждает зло🙌🏻🤗', reply_markup = kb)

@bot.message_handler(commands=['start'])
def start(msg):
    what_is_ur_name(msg.chat.id)

def crete_nav_buttons(buttons_text = []):
    
    if buttons_text == []:

        markup = types.InlineKeyboardMarkup(row_width = 2)

        buttons = []

        buttons.append(types.InlineKeyboardButton(text = 'previous', callback_data = 'prev'))
        buttons.append(types.InlineKeyboardButton(text='next', callback_data='next'))
    else:
        
        markup = types.InlineKeyboardMarkup(row_width = 1)

        buttons = []

        for button in buttons_text:
            a = button.split(' ')
            new_btn_callback_data = ''
            for i in range(0, min(2, len(a))):
                new_btn_callback_data += a[i] + ' '
            
            print(new_btn_callback_data)
            buttons.append(types.InlineKeyboardButton(text = button, callback_data = new_btn_callback_data[:-1]))
 
    markup.add(*buttons)

    return markup

'''
def query_handler(call):

    text = call.message.text

    array = []
    header = ''
    index = -1
    
    for key, value in contents.items():
        for i in range(len(value)):
            if text == value[i]:
                array = value
                header = key
                index = i
                break
        if index != -1:
            break

    if array == []:
        return
    
    if call.data == 'next':
        index += 1
        index %= len(value)
    elif call.data == 'prev':
        index -= 1
        if index < 0 :
            index = len(value) - 1

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = array[index], reply_markup = crete_nav_buttons() )
'''

@bot.message_handler(func=lambda msg: msg.text != 'ХЕХЕЙ')
def handler(msg):
    photo_name = str(random.randint(1, 6)) + '.jpg'

    texts = contents[msg.text]
    content_text = texts[0]

    buttons_text = []
    if( 'buttons' in content_text ):
        new_ind = content_text.find('buttons')
        print(new_ind)
        
        buttonsText = content_text[new_ind::]
        buttons_text = buttonsText.split('$')
        buttons_text = buttons_text[1::]

        content_text = content_text[0:new_ind]

    img = open(photo_name, 'rb')
    bot.send_photo(msg.chat.id, img)
    bot.send_message(msg.chat.id, content_text, reply_markup = crete_nav_buttons(buttons_text))

    ''' 
    if msg.text == 'Контакты':
        lat = 51.162564
        lon = 71.407020
        bot.send_location(msg.chat.id, lat, lon)
    '''

'''
def blog(msg):
    kb = types.InlineKeyboardMarkup(row_width = 2)

    btn = []

    counter = 0
    for title in config.blog_titles:
        btn.append( types.InlineKeyboardButton(title[0:30] + '...', callback_data = str(counter) + ' blog') )
        counter += 1

    kb.add(*btn)

    bot.send_message(msg.chat.id, 'Истории', reply_markup = kb)

@bot.callback_query_handler(func=lambda call: 'blog' in call.data)
def handling(call):
    msg = call.message

    text_id = int(call.data.split(' ')[0])
    texts = config.blog_texts
    if type(texts[text_id]) != type('test'):
        for text in texts[text_id]:
            bot.send_message(msg.chat.id, text)
    else:
        bot.send_message(msg.chat.id, texts[text_id])
'''

@bot.callback_query_handler(func=lambda call: 'next' in call.data or 'prev' in call.data)
def handling(call):


    text = call.message.text

    array = []
    header = ''
    index = -1
    
    for key, value in contents.items():
        for i in range(len(value)):
            #print(value[i])
            if text in value[i]:
                array = value
                header = key
                index = i
                break
        if index != -1:
            break

    if array == []:
        return
    
    if call.data == 'next':
        index += 1
        index %= len(value)
    elif call.data == 'prev':
        index -= 1
        if index < 0 :
            index = len(value) - 1

    content_text = array[index]

    buttons_text = []
    if( 'buttons' in content_text ):
        new_ind = content_text.find('buttons')
        print(new_ind)
        
        buttonsText = content_text[new_ind::]
        buttons_text = buttonsText.split('$')
        buttons_text = buttons_text[1::]

        content_text = content_text[0:new_ind]

    bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.message_id, text = content_text, reply_markup = crete_nav_buttons(buttons_text) )

@bot.callback_query_handler(func=lambda call: not ('next' in call.data or 'prev' in call.data))
def handling(call):
    texts = contents[call.data]
    bot.send_message(call.message.chat.id, texts[0], reply_markup = crete_nav_buttons())

'''
if __name__ == '__main__':
  bot.polling(none_stop=True)
'''