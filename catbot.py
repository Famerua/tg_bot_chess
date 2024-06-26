import requests
import time

# fmt: off
API_URL = "https://api.telegram.org/bot"
TEXT = "Ты написал мне! Не пиши, заебал"
MAX_COUNTER = 100
CATS_API = 'https://api.thecatapi.com/v1/images/search'
# fmt: on

#create gile <Token.txt> and write into your token
BOT_TOKEN: str
with open("Token.txt") as f:
    BOT_TOKEN = f.read()

offset = -2
counter = 0
chat_id: int

while counter < MAX_COUNTER:
    print("attempt= ", counter)

    updates = requests.get(f"{API_URL}{BOT_TOKEN}/getUpdates?offset={offset+1}").json()

    if updates["result"]:
        print(updates['result'])
        for i in updates["result"]:
            offset = i["update_id"]
            chat_id = i["message"]["from"]["id"]
            name = i['message']['from']['first_name']

            cat = requests.get(f"{CATS_API}")
            if cat.status_code == 200:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat.json()[0]['url']}')
            else:
                requests.get(f"{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={'ERR, no cats? SORRY'}")

            requests.get(
                f"{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}, {name}"
            )

    time.sleep(1)
    counter += 1

