import logging
import random
import time
from datetime import datetime, timedelta
import telebot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

##
## AQUI SERÁ AONDE VOCE TEM QUE POR O TOKEN DO SEU BOT, OBS: TUDO DENTRO DA ''
##

bot = telebot.TeleBot('5812346741:AAH4GerkfybQMpKLuCTHmHOqmVNT8nGw4jw') 

grupo_id = -1001533104289  # ID DO GRUPO

canal_id = -1001533104289  # ID DO CANAL

admins_ids = [5587769057]  # ID DO DONO DO BOT

#  armazenar o ID da mensagem do sinal atual
mensagem_sinal_atual = None

def enviar_sinal(destino_id):
    minas = random.choice([3, 4])  # So gera sinal de 3 e 4 minas 
    hora_validade = datetime.now() + timedelta(minutes=5)  # Horário de validade é 5 minutos a partir do momento atual

    tabuleiro = [['🟦' for _ in range(5)] for _ in range(5)]
    estrelas = random.sample(range(25), minas)
    for posicao in estrelas:
        linha = posicao // 5
        coluna = posicao % 5
        tabuleiro[linha][coluna] = '⭐'

    mensagem = f"💰 Entrada Confirmada 💰\n"
    mensagem += f"💣 Minas: {minas}\n"
    mensagem += f"🕑 Válido até: {hora_validade.strftime('%H:%M')}\n"
    mensagem += f"🔁 Nº de tentativas: 3\n\n"
    mensagem += '\n'.join([''.join(linha) for linha in tabuleiro])

    global mensagem_sinal_atual
    mensagem_sinal_atual = bot.send_message(destino_id, mensagem, parse_mode='Markdown')
    agendar_novo_sinal(hora_validade, destino_id)

def agendar_novo_sinal(hora_validade, destino_id):
    agora = datetime.now()
    tempo_restante = hora_validade - agora
    time.sleep(tempo_restante.total_seconds())
    enviar_sinal(destino_id)
    remover_sinal_anterior(destino_id)

def remover_sinal_anterior(destino_id):
    global mensagem_sinal_atual
    if mensagem_sinal_atual is not None:
        horario_finalizado = datetime.now().strftime('%H:%M')
        mensagem_finalizado = f"🔹 Sinal Finalizado 🔹\n"
        mensagem_finalizado += f"🕑 Finalizado às {horario_finalizado}"
        bot.edit_message_text(chat_id=destino_id, message_id=mensagem_sinal_atual.message_id, text=mensagem_finalizado, parse_mode='Markdown')
        mensagem_sinal_atual = None
##
## gerenciar o comando /start
##
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Olá! Sou um bot de sinais de mines. Vou enviar sinais de mines  para o grupo e canal.")

##
## comando /resume
##
@bot.message_handler(commands=['resume'])
def handle_resume(message):
    if message.from_user.id in admins_ids:
        bot.reply_to(message, "O bot foi retomado. Novos sinais serão enviados.")

if __name__ == '__main__':
    logger.info("O Robo de sinal foi inicializado com sucesso!")
    logger.info("Bot criado por Xmroot")
    enviar_sinal(grupo_id) 
    enviar_sinal(canal_id)
bot.polling()
