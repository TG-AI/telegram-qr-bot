import pyqrcode
import qrtools
from PIL import Image, ImageDraw
import os
import telebot
from colorama import Fore, Back, Style
import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time


date_today = datetime.datetime.now()
bottoken = "TOKEN"


bot = telebot.TeleBot(bottoken)


bluecolor_dict =	{
  "maincolor": "84, 137, 153",
  "bgcolor": "230, 239, 246"
}

color_dict =	{
  "maincolor": "blue"
}







def add_corners(im, rad):
  circle = Image.new('L', (rad * 2, rad * 2), 0)
  draw = ImageDraw.Draw(circle)
  draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
  alpha = Image.new('L', im.size, 255)
  w, h = im.size
  alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
  alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
  alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
  alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
  im.putalpha(alpha)
  return im

# def add_label(im):
#     draw = ImageDraw.Draw(im)
#     font = ImageFont.truetype("GillSans.ttc", 16)
#     w, h = im.size
#     draw.text((0, 0), "https://t.me/qrcodebot_bot", ((h / 80), (w / 2), 255), font=font)
#
#
#     return im
#



def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print("\n")
            print(Fore.BLACK + "––––––––––––––––––––––––––––––––––––––––––––––––––––––")
            print(Fore.LIGHTRED_EX + f"{m.chat.first_name}[{m.chat.id}][{date_today}]: {m.text}")
            print(Fore.BLACK + "––––––––––––––––––––––––––––––––––––––––––––––––––––––")
            print("\n")
bot.set_update_listener(listener) 

@bot.message_handler(commands=['start'])
def command_start(m):
  msg = m.text
  cid = m.chat.id
  bot.send_message(cid, "Привет! Я телеграм бот, который поможет сделать качественный qrcode!")

@bot.message_handler(commands=['help'])
def command_help(m):
  msg = m.text
  cid = m.chat.id
  bot.send_message(cid, "Список доступных команд:\n/color - для выбора цвета qrcod\'a\n/create <ваш текст // ссылка> - для создания qrcod\'а\n ----------------------------------------- \n@uglycuteanddying 🌊🌊🌊")


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("white", callback_data="white_cb"),
                               InlineKeyboardButton("blue", callback_data="blue_cb"), InlineKeyboardButton("yellow", callback_data="yellow_cb"), InlineKeyboardButton("green", callback_data="green_cb"))
    return markup


@bot.message_handler(commands=['color'])
def color_pick(m):
  msg = m.text
  cid = m.chat.id  
  bot.send_message(cid, "Выберите цвет:", reply_markup=gen_markup())


def upload_photo():
  im = Image.open('timefiles/test.jpg').convert('RGB')
  im = add_corners(im, 85)
  # im = add_label(im)
  im.save('main.png')




# @bot.message_handler(func=lambda m: True)
# def ping(m):
#     msg = m.text
#     cid = m.chat.id
#     if msg == "/ping":
#         import time
#         time_then = time.monotonic()
#         ping = '%.2f' % (1000 * (time.monotonic() - time_then))
#         lastMessageId = m[-1].message_id
#         bot.send_message(cid, "Понг! 🐁")
#         bot.edit_message_text(f"{ping} мл/с", cid,lastMessageId)




@bot.message_handler(func=lambda m: True)

def qr_create(m):
    msg = m.text
    cid = m.chat.id
    try:
        if msg.startswith("/create"):
            user_message = msg.split(" ", 1)[1]
            if len(user_message) > 128:
                bot.send_message(cid, "Слишком длинный текст!")
            elif len(user_message) < 3:
                bot.send_message(cid, "Слишком короткий текст!")
            else:
                qr = pyqrcode.create(f'{user_message}')
                color_qr = color_dict['maincolor']
                if color_qr == 'blue':
                    qr.png('timefiles/test.jpg', scale=20, module_color=[84, 137, 153], background=[230, 239, 246])
                    upload_photo()
                    bot.send_photo(cid, open('main.png', 'rb'))
                    os.remove("timefiles/test.jpg")
                    time.sleep(5)
                    os.remove("main.png")

                elif color_qr == 'white':
                    qr.png('timefiles/test.jpg', scale=20, module_color=[171, 166, 168], background=[244, 246, 245])
                    upload_photo()
                    bot.send_photo(cid, open('main.png', 'rb'))
                    os.remove("timefiles/test.jpg")
                    time.sleep(5)
                    os.remove("main.png")

                elif color_qr == 'yellow':
                    qr.png('timefiles/test.jpg', scale=20, module_color=[188, 143, 70], background=[227, 217, 173])
                    upload_photo()
                    bot.send_photo(cid, open('main.png', 'rb'))
                    os.remove("timefiles/test.jpg")
                    time.sleep(5)
                    os.remove("main.png")

                elif color_qr == 'green':
                    qr.png('timefiles/test.jpg', scale=20, module_color=[75, 76, 44], background=[160, 166, 89])
                    upload_photo()
                    bot.send_photo(cid, open('main.png', 'rb'))
                    os.remove("timefiles/test.jpg")
                    time.sleep(5)
                    os.remove("main.png")

    except UnicodeEncodeError:
        bot.send_message(cid, "Бот принимает текст только на английском!")
    except IndexError:
        bot.send_message(cid, "Whoopsie! Ошибка! Попробуйте снова!")






@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
  if call.data == "white_cb":
      bot.answer_callback_query(call.id, "Белый выбран по умолчанию 🐁")
      color_dict.update(maincolor='white')
  elif call.data == "blue_cb":
      bot.answer_callback_query(call.id, "Голубой выбран по умолчанию 🦋")
      color_dict.update(maincolor='blue')
  elif call.data == "green_cb":
      bot.answer_callback_query(call.id, "Зеленый выбран по умолчанию 🦎")
      color_dict.update(maincolor='green')
  elif call.data == "yellow_cb":
      bot.answer_callback_query(call.id, "Желтый выбран по умолчанию 🐥")
      color_dict.update(maincolor='yellow')




# @bot.message_handler(content_types=["photo"])
# def handle_photo(m):
#     photo_id = m.photo[-1].file_id
#     file_info = bot.get_file(photo_id)
#     print(file_info)
#     downloaded_file = bot.download_file(file_info.file_path)
#     with open(src, 'wb') as new_file:
#         new_file.write(downloaded_file)
#     bot.reply_to(m, "Пожалуй, я сохраню это")


@bot.message_handler(content_types=['photo'])
def photo(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)


    image_name = f"image{date_today}"

    with open(f"{image_name}.png", 'wb') as new_file:
        new_file.write(downloaded_file)

    from pyzbar.pyzbar import decode
    from PIL import Image
    decode_m = decode(Image.open(f'{image_name}.png'))

    pt_1 = str(decode_m[0].data)
    pt_2 = pt_1.replace("b", '')
    pt_3 = pt_2.replace("'", '')



    bot.reply_to(message,f"{pt_3}")

    os.remove(f"{image_name}.png")






bot.polling()
