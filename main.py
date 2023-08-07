import schedule
import time
import vk_api
from datetime import datetime, date
import os
from dotenv import load_dotenv
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.utils import get_random_id
from pytz import timezone

load_dotenv()
f = open('anecs.txt', 'r', encoding="utf-8")

# Environment
vk_token = os.environ.get('VK_TOKEN')
vk_key = os.environ.get('VK_KEY')
group_id = os.environ.get('GROUP_ID')
chat_id = os.environ.get('CHAT_ID')

vk_session = vk_api.VkApi(token=vk_token)
longpoll = VkBotLongPoll(vk_session, group_id)
vk = vk_session.get_api()

anecs = f.read().split("\n\n")
bro_leave_us_date = datetime(2023, 7, 21)
start_day_number = 17

def get_days(date1, date2):
    return (date2 - date1).days

def get_days_without_bro():
    return get_days(bro_leave_us_date, datetime.utcnow())

def get_anec_index():
    return get_days_without_bro() - start_day_number

def get_anec_by_index(index):
    return anecs[index]

def get_message_text():
    return f'*Дней без уебана: {get_days_without_bro()}*\n{get_anec_by_index(get_anec_index())}'

def job():
    print('SEND!')
    print(get_message_text())
    vk.messages.send(
        key=vk_key,
        server=f'https://lp.vk.com/whp/{group_id}',
        ts='0',
        random_id=get_random_id(),
        message=get_message_text(),
        chat_id=chat_id
    )

#schedule.every().day.at("16:52", timezone("UTC")).do(job)
schedule.every(10).seconds.do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)