import matplotlib.pyplot as plt
import datetime
import telebot
import yaml
import os

pathDir = '/path/to/dir/LaTeXitbot/'

def openBot():
    inputFile = pathDir + 'botToken.yml'
    conf = yaml.safe_load(open(inputFile,'r'))
    bot = telebot.TeleBot(conf['user']['token'])
    return bot

def pltSetUp():
    plt.switch_backend('Agg')
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

def createPath(IDUser):
    ts = datetime.datetime.now().strftime('%H-%M-%S-%f')
    return pathDir + ts + IDUser + '.png'

def sendImage(path,id):
    try:
        photo = open(path, 'rb')
        bot.send_photo(id, photo)
        os.remove(path)
    except:
        erroreMessage = "Can't sent the image :("
        bot.send_message(id,erroreMessage)

bot = openBot()
pltSetUp()

@bot.message_handler(commands=['start'])
def handle_start_help(message):
    reply = "LaTeX bot to compile and get images of the result"
    bot.send_message(message.chat.id,reply)

@bot.message_handler(commands=['info'])
def handle_info(message):
    reply = "in fieri"
    bot.send_message(message.chat.id,reply)

@bot.message_handler(commands=['latexit'])
def handle_LaTeXit(message):
    tex = message.text[8:]
    if len(tex)<=1:
        return
    print(message.text, message.chat.username)
    id = message.chat.id

    plt.text(0.5, 0.5, tex, horizontalalignment='center',verticalalignment='center',fontsize=20)
    ax = plt.gca()
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    plt.box(False)
    path = createPath(str(id))
    
    error = False
    try:
        plt.savefig(path, bbox_inches='tight', dpi=300)
    except:
        erroreMessage = "Compilation error :("
        bot.send_message(id,erroreMessage)
        error = True

    plt.close()
    
    if error == False:
        sendImage(path,id)

bot.polling()

