from dotenv import load_dotenv
import os
import requests
import json
from src.data.DriveBot import DriveBot
from src.data.transform_dataframe import transform_data
from src.visualization.visualize import barv_npsmean_by, hist_nps

load_dotenv()


class BotTelegram:
    def __init__(self):
        TOKEN = os.getenv("API_KEY")
        self.url = f"https://api.telegram.org/bot{TOKEN}/"
        self.DriveBot = DriveBot()
    
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
                        answer_bot, figure_boolean = self.creat_answer(message_text)
                        self.send_answer(chat_id, answer_bot, figure_boolean)
                    except:
                        pass
            
    def get_message(self, update_id):
        link_request = f"{self.url}getUpdates?timeout=120"
        if update_id:
            link_request = f"{self.url}getUpdates?timeout=120&offset={update_id+1}"
        resultado = requests.get(link_request)
        return json.loads(resultado.content)
    
    def creat_answer(self, message_text):
        dataframe = transform_data(self.DriveBot.get_data())
        message_text = message_text.lower()
        if message_text in ["/start", "ola", "eae", "menu", "oi", "oie"]:
            return "Ola,seja bem-vindo ao Bot. Selecione o que deseja:" + "\n" + "1 - NPS interno mensal médio por setor" + "\n" + "2 - NPS interno mensal médio por contratação" + "\n" + "3 - Distribuição do NPS interno" + "\n",0
        elif message_text == '1':
            return barv_npsmean_by(dataframe, "Setor"), 1
        elif message_text == '2':
            return barv_npsmean_by(dataframe, "Tipo de Contratação"), 1
        elif message_text == '3':
            return hist_nps(dataframe), 1
        else:
            return "Comando não encontrado, tente novamente. Selecione o que deseja:" + "\n" + "1 - NPS interno mensal médio por setor" + "\n" + "2 - NPS interno mensal médio por contratação" + "\n" + "3- Distribuição do NPS interno" + "\n", 0
    
    def send_answer(self, chat_id, answer, figure_boolean):
        if figure_boolean == 0:
            link_para_enviar = f"{self.url}sendMessage?chat_id={chat_id}&text={answer}"
            requests.get(link_para_enviar)
            return
             
        else:
            figure = r"D:\Jonas\Documents\visua\python\novoProjeto\Projetoyt\graph_last_generate.png"
            files = {
                "photo": open(figure, "rb")
            }
            link_para_enviar = f"{self.url}sendphoto?chat_id={chat_id}"
            requests.post(link_para_enviar, files= files)
            return