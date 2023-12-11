import requests

from time import sleep
import telebot
 
from telebot import util
 
 
CHAVE_API = "6800699046:AAHcnDlichubFIuNdUBvM0F114IPX_-Ql1Q"
 
bot = telebot.TeleBot(CHAVE_API)

array2 = ["\U00000031\U000020E3","\U00000032\U000020E3","\U00000033\U000020E3","\U00000034\U000020E3",
         "\U00000035\U000020E3", "\U00000036\U000020E3","\U00000037\U000020E3", "\U00000038\U000020E3","\U00000039\U000020E3","\U0001F51F" ]
 
def iniciar (mensagem):
    return True
 
@bot.message_handler(commands=["start"])
def responder(mensagem):
  teste = util.quick_markup(
    {   'Buscar Ferramenta': {'callback_data': 'ferramenta'}  
     }, row_width=1
     )
  bot.send_message(
        mensagem.chat.id,
        "\U0001F4A1 Olá, eu sou o ChatBot ConsultaIA, um chatbot desenvolvido pela Provider IT para te ajudar a encontrar a melhor ferramenta de IA para as suas necessidades. \n\n(Para continuar clique no botão ""Buscar Ferramenta)" "\U0001F447",
        reply_markup=(teste))
  
def verificar(mensagem):
    return True
 
@bot.message_handler(func=verificar)
def responder(mensagem):
    if mensagem.text != "":
        inf = requests.get(
            f"http://searchia.us-east-1.elasticbeanstalk.com/busca/{mensagem.text}")
        inf = inf.json()
 
    array = []
    for m in inf:
        obj = {
                "relevancia": inf[m]['Relevance'],
                "nomeFerramenta": inf[m]['PositionTitle'],
                # "descricao": inf[m]['Description'],
                "categoria": inf[m]['Category'],
                "link": inf[m]['PositionPlot'],
            },
        array.append(obj)
 
    if len(array) < 1:
        bot.reply_to(mensagem, " \U0000274C Desculpe, não foi possível processar sua solicitação. Certifique-se de seguir o formato correto, como no exemplo: ""Quero ferramentas de produção de imagens!")
    else:
        formater = """
                    Aqui estão as ferramentas que podem te ajudar:
                    """
        for indice in range(len(array)):
           
             formater += "\n" + array2[indice] +"  Nome: {}\n       Categoria: {}\n       Relevância: {}\n       Link: {}\n".format(
                            array[indice][0]['nomeFerramenta'],
                            array[indice][0]['categoria'],
                            array[indice][0]['relevancia'],
                            array[indice][0]['link']
                            )
 
        bot.reply_to(mensagem, formater)

        sleep(10)
        
        bot.send_message(mensagem.chat.id, " \U0001F44D\U0001F3FB Gostou dos resultados? Divulgue esta ferramenta com seus contatos e espalhe por ai esta novidade. \n\nProvider IT, sua parceira em soluções de Inteligência Artificial. \n\nQuer saber mais sobre nossa empresa? Estamos aqui para ajudar você a explorar as possibilidades da IA em sua vida cotidiana.\n\n Acesse: https://provider-it.com.br/nossas-ofertas/ia-consultoria-desenvolvimento-e-implementacao/")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # Lógica para manipular eventos de callback
        if call.data == 'ferramenta':
            bot.send_message(call.message.chat.id, " \U0001F31F Por favor, descreva a atividade para a qual você deseja uma recomendação, da seguinte forma: \n\n""Quero ferramentas de [descreva a tarefa ou área de interesse]!")
            

bot.polling()