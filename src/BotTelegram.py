from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()


class BotTelegram:
    def __init__(self):
        TOKEN = os.getenv("API_KEY")
        self.url = f"https://api.telegram.org/bot{TOKEN}/"
    
    def start(self):
        update_id = None
        while True:
            update = self.get_message(update_id)
            messages = update['result']
            if messages:
                for message in messages:
                    try:
                        update_id = message['update_id']
                        chat_id = message['message']['from']['id']
                        message_text = message['message']['text']
                        answer_bot = self.creat_answer(message_text)
                        self.send_answer(chat_id, answer_bot)
                    except:
                        pass
            
    def get_message(self, update_id):
        link_request = f"{self.url}getUpdates?timeout=120"
        if update_id:
            link_request = f"{self.url}getUpdates?timeout=120&offset={update_id+1}"
        resultado = requests.get(link_request)
        return json.loads(resultado.content)
    
    def creat_answer(self, message_text):
        if message_text in ["oi", "ola", "eae"]:
            return "Ola, o que deseja?"
        else:
            return "desculpe, nao entendi."
    
    def send_answer(self, chat_id, answer):
        link_para_enviar = f"{self.url}sendMessage?chat_id={chat_id}&text={answer}"
        requests.get(link_para_enviar)
        return