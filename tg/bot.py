from api import app
import telebot
import requests
import urllib.parse
import os


bot_token = 'UR_BOT_TOKEN'
bot = telebot.TeleBot(bot_token)


def notify_contractor_in_telegram(request_data):
    """Оповестить исполнительные органы новой заявкой."""
    def generate_hash_tags_str(arr:list)->str:
        return ' '.join(['\\'+_.get('hash_tag')\
                for _ in arr if _.get('hash_tag') is not None])

    title = request_data.get('description','')
    c_hash_tag = generate_hash_tags_str(request_data.get("contractors",[]))
    hash_tags = generate_hash_tags_str( request_data.get("problem_categories",[]))
    location = request_data.get('location','Неизвестно')
    attachments = request_data.get('attachments',[])
    
    for contractor in request_data.get("contractors",[]):
        
        if contractor.get('type','')=="EXECUTIVE":

            if len(attachments) == 0:
                c_hash_tag = c_hash_tag.replace('_','\\_')
                hash_tags = hash_tags.replace('_','\\_')
                message = f"*Описание:* {title}\n*Адрес проблемы:* _{location}_\n*Хэштеги:* _{c_hash_tag} {hash_tags}_"
                send_message(contractor.get('telegram_chat_id'),message) 

            else:

                message = f"Описание: {title}\nАдрес проблемы: {location}\nХэштеги: {c_hash_tag} {hash_tags}"
                if attachments[0]['type'] == 'IMAGE':
                    send_photo(contractor.get('telegram_chat_id'), attachments[0]['url'],message)
                else:
                    send_video(contractor.get('telegram_chat_id'), attachments[0]['url'],message)
            

def send_message(tg_chat_id:str, message:str):
    """Отправка текстового сообщения в тг"""

    if tg_chat_id is None: 
        return

    json_data = {
                    'chat_id' : tg_chat_id,
                    'text' : message,
                    "parse_mode": "MarkdownV2"
                }
    header = {"Content-type":"application/json"}
    requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage',json=json_data, headers=header)
    

def send_photo(tg_chat_id:str, photo_url, caption=''):
    """Отправка телеграм сообщение с фото"""

    if tg_chat_id is None: 
        return

    files = {'photo': open(os.path.join(app.config['UPLOAD_FOLDER'], photo_url.split('/')[-1]), 'rb')}
    requests.post(f'https://api.telegram.org/bot{bot_token}/getUpdates')
    params = urllib.parse.quote(caption)
    res = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={tg_chat_id}&caption={params}&parse_mode=markdown',
        files=files
    )
    print(res.json())


def send_video(tg_chat_id:str, video_url, caption=''):
    """Отправка телеграм сообщения с видео"""

    if tg_chat_id is None: 
        return

    files = {'video': open(os.path.join(app.config['UPLOAD_FOLDER'], video_url.split('/')[-1]), 'rb')}
    requests.post(f'https://api.telegram.org/bot{bot_token}/getUpdates')
    params = urllib.parse.quote(caption)
    res = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={tg_chat_id}&caption={params}&parse_mode=markdown',
        files=files
    )
    print(res.json())