import time
import telebot
import qrcode
import random
import datetime
from telebot import types
from gtts import gTTS
from telebot.types import Message
from time import sleep

def hejri_to_miladi(jy, jm, jd):
    jy += 1595
    days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
    if (jm < 7):
        days += (jm - 1) * 31
    else:
        days += ((jm - 7) * 30) + 186
    gy = 400 * (days // 146097)
    days %= 146097
    if (days > 36524):
        days -= 1
        gy += 100 * (days // 36524)
        days %= 36524
        if (days >= 365):
            days += 1
    gy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        gy += ((days - 1) // 365)
        days = (days - 1) % 365
    gd = days + 1
    if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        kab = 29
    else:
        kab = 28
    sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    while (gm < 13 and gd > sal_a[gm]):
        gd -= sal_a[gm]
        gm += 1
    return [gy, gm, gd]

bot = telebot.TeleBot("2116895736:AAGZ1aYErix-2fxgTXiUEGNZxrY6YpsINYs")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, " به ربات فرزاد فروزان فر خوش آمدید " + message.from_user.first_name + "\n/help بزن تا وارد منو من بشی  :)")
@bot.message_handler(commands=['help'])
def show_menu(message):
    bot.reply_to(message,"""/start ---> پیام خوش آمد
/help ---> چاپ منو
/game ---> بازی حدس اعداد
/age ---> محاسبه سن 
/voice ---> تبدیل متن به صدا 
/max ---> مقدار ماکزیمم آرایه 
/argmax ---> اندیس بزرگترین مقدار آرایه
/qrcode ---> تبدیل متن به کد کیو آر
    """)

@bot.message_handler(commands=['game'])
def game(message):
    random_number = random.randint(0,50)
    guess_number = bot.send_message(message.chat.id, """قوانین بازی :
اول اینکه لطفا فقط اعداد صحیح وارد کن جونه دل
دومیشم اینه آرامشتو حفظ کن اروم اروم وبا فاصله زمانی پیام خودتو برام بفرست
هروقتم خسته شدی یا برنده شدی و میخواستی دوباره باهام بازی کنی یک دکمه اون زیر برای شروع دوباره برات گذاشتم عزیزدل
موفق باشی چند ثانیه دیگه بازی شروع میشه ...""")
    time.sleep(5)
    guess_number = bot.send_message(message.chat.id, "بازی شروع شد عدد را وارد کنید")
    bot.register_next_step_handler(guess_number, guess_number_game,random_number)

def guess_number_game(number,random_number):
    
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    exitButton = types.KeyboardButton('خروج از بازی')
    button = telebot.types.KeyboardButton('شروع دوباره')
    markup.add(button,exitButton)
    if number.text == 'خروج از بازی':
        markup = telebot.types.ReplyKeyboardRemove(selective=True)
        button = telebot.types.ReplyKeyboardRemove(selective=True)
        exitButton = telebot.types.ReplyKeyboardRemove(selective=True)
        bot.send_message(number.chat.id, "خب عزیز خارج شدی یک کامند دیگر انتخاب کن", reply_markup=markup)

    elif number.text == 'شروع دوباره':
        random_number = random.randint(0,50)
        bot.send_message(number.chat.id, "بازی شروع شد عدد را وارد کنید", reply_markup=markup)
        bot.register_next_step_handler(number, guess_number_game,random_number)
    
    else:
        try:
            if int(number.text) == random_number:
                markup = telebot.types.ReplyKeyboardRemove(selective=True)
                button = telebot.types.ReplyKeyboardRemove(selective=True)
                exitButton = telebot.types.ReplyKeyboardRemove(selective=True)
                bot.send_message(number.chat.id,"🏆😍 هوراااا خودشه .برنده شدی 😍🏆", reply_markup=markup)
            elif int(number.text) == random_number - 1:
                bot.send_message(number.chat.id,"😉نه یکم دیگه برو بالاتر😉", reply_markup=markup)
                bot.register_next_step_handler(number, guess_number_game,random_number)
            elif int(number.text) < random_number:
                bot.send_message(number.chat.id,"😐نه بابا!!! برو بالاتر😐", reply_markup=markup)
                bot.register_next_step_handler(number, guess_number_game,random_number)
            elif int(number.text) == random_number + 1:
                bot.send_message(number.chat.id,"👀 نه یکوچولو پایین تره👀", reply_markup=markup)
                bot.register_next_step_handler(number, guess_number_game,random_number)
            elif int(number.text) > random_number:
                bot.send_message(number.chat.id,"😑نه بابا!!! برو پایین تر😑", reply_markup=markup)
                bot.register_next_step_handler(number, guess_number_game,random_number)
        except:
            number = bot.send_message(number.chat.id,"😕بالاغیرتا عدد صحیح  وارد کن😕", reply_markup=markup)
            bot.register_next_step_handler(number, guess_number_game,random_number)
@bot.message_handler(commands=['age'])
def cal_age(message):
    b_day = bot.send_message(message.chat.id,"""قوانین:
    قراره شما تاریخ تولدتو دقیق و قشنگ مثل 1379/4/8 وارد کنی منم سنتو دقیق و کامل بهت میگیم جونه دل
    بعد دیگه حتما شمسی وارد کنی گلم که منم به اشتباه نندازی 
    منتظرتم تا همونجور که بهت گفتم تاریخ تولدتو وارد کنی😌""")
    bot.register_next_step_handler(b_day, calculate_age)

def calculate_age(b_day):
    try:
        now = datetime.datetime.now()
        today = []
        temp = []
        today.append(int(now.year))
        today.append(int(now.month))
        today.append(int(now.day))
        text = b_day.text
        text = text.split("/")
        temp.append(int(text[0]))
        temp.append(int(text[1]))
        temp.append(int(text[2]))
        miladi_birthday_user = hejri_to_miladi(temp[0],temp[1],temp[2])
        if miladi_birthday_user[2] > today[2]:
            if miladi_birthday_user[2] > today[2]:
                today[0] -= 1
                today[1] += 11
                today[2] += 30
        elif miladi_birthday_user[1] > today[1]:
            today[0] -= 1
            today[1] += 12
        age_year = today[0] - miladi_birthday_user[0]
        age_month = today[1] - miladi_birthday_user[1]
        age_day = today[2] - miladi_birthday_user[2]
        if age_month > 12 :
            age_month -= 12
            age_year += 1
        age_h = now.hour
        age_min = now.minute
        age_sec = now.second
        
        AGETXT = "سن شما " + str(age_year) + " سال و " + str(age_month) + " ماه و " + str(age_day) + " روز و " + str(age_h) + " ساعت و " + str(age_min) + " دقیقه و " + str(age_sec) + "ثانیه است ."
        
        bot.send_message(b_day.chat.id,AGETXT)
    except:
        b_day = bot.send_message(b_day.chat.id,"تاریخ تولدتم نمیتونی درست وارد کنی !!! یکبار دیگه تلاش بکن مثل نمونه 1379/4/8")
        bot.register_next_step_handler(b_day, calculate_age)

@bot.message_handler(commands=['voice'])
def text_to_voice(message):
    sentence = bot.send_message(message.chat.id, "😜خب جییگر یک متن خوانا و خوشگل انگلیسی بمویس تا به وویس تبدیلش کنم خدمتتون ارایه کنم😜")
    bot.register_next_step_handler(sentence, convertor_txt_to_voice)

def convertor_txt_to_voice(message):
    try:
        txt = message.text
        language = 'en'
        ojc = gTTS(text=txt, lang=language, slow=False)
        ojc.save("voice.mp3")
        voice = open('voice.mp3', 'rb')
        bot.send_voice(message.chat.id, voice)
    except:
        sentence = bot.send_message(message.chat.id, "😒قربون اون سوادت بشم بهت گفتم یک متن انگلیسی بده خب😒")
        bot.register_next_step_handler(sentence, convertor_txt_to_voice)

@bot.message_handler(commands=['max'])
def find_max(message):
    user_array = bot.send_message(message.chat.id, "خوب عزیز دل برادر ازت میخام یک آرایه مثل مثالی که برات میزنم برام بفرستی منم بزرگ ترین عنصر ارایه رو بهت میگم کدومه --- مثال:14,7,78,15,8,19,20")
    bot.register_next_step_handler(user_array, which_is_max)

def which_is_max(user_array):
    try:
        array = user_array.text.split(",")
        array_number = []
        for i in range(len(array)):
            array_number.append(int(array[i]))
        MAX = max(array_number)
        bot.send_message(user_array.chat.id,"👇 خدمت شما 👇")
        bot.send_message(user_array.chat.id,MAX)
    except:
        user_array = bot.send_message(user_array.chat.id,"عزیزدل دوتا نکته نتونستی رعایت کنی و منو به اشتباه انداختی لطفا فقط بهم عدد بده و به شکل مثالی که بهت گفتم برام بفرست ممنون")
        bot.register_next_step_handler(user_array, which_is_max)

@bot.message_handler(commands=['argmax'])
def find_index_max(message):
    array = bot.send_message(message.chat.id, "خوب عزیز دل برادر ازت میخام یک آرایه مثل مثالی که برات میزنم برام بفرستی منم اندیس بزرگ ترین عنصر ارایه رو بهت میگم کدومه --- مثال:14,7,78,15,8,19,20")
    bot.register_next_step_handler(array, which_is_index_max)

def which_is_index_max(user_array):
    try:
        array = user_array.text.split(",")
        array_number = []
        for i in range(len(array)):
            array_number.append(int(array[i]))
        MAX = max(array_number)
        index_max = 0
        for i in range(len(array_number)):
            if MAX == array_number[i]:
                index_max = i
        
        bot.send_message(user_array.chat.id,"👇 خدمت شما 👇")
        bot.send_message(user_array.chat.id,index_max)
    except:
        user_array = bot.send_message(user_array.chat.id,"عزیزدل دوتا نکته نتونستی رعایت کنی و منو به اشتباه انداختی لطفا فقط بهم عدد بده و به شکل مثالی که بهت گفتم برام بفرست ممنون")
        bot.register_next_step_handler(user_array, which_is_index_max)
@bot.message_handler(commands=['qrcode'])
def get_qrcode(message):
    qr_code = bot.send_message(
        message.chat.id, 'لطفا برام یک متن  بفرست تا تبدیلش کنم به کد کیو آر :')
    bot.register_next_step_handler(qr_code, make_qrcode)

def make_qrcode(message):
    try:
        qrcode_image = qrcode.make(message.text)
        qrcode_image.save('QR-Code.jpg')
        photo = open('QR-Code.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
    
    except:
        qr_code = bot.send_message(message.chat.id, ' لطفا فقط متن رو  وارد کن عزیز تا بتونم کد کیو آر بسازم')
        bot.register_next_step_handler(qr_code, make_qrcode)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, "من فارسی خوب نفهمید من کیلی کیلی انگلیش بلد بود و لطفا از کامند هام استفاد کن")
bot.infinity_polling()

