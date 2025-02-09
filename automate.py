from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
import os

import ui_gui as ma

import threading

def Tcarregar():
    t1=threading.Thread(target=carregar)
    t1.start()

def Tlogar():
    t2=threading.Thread(target=logar)
    t2.start()

def Tenviar():
    t3=threading.Thread(target=enviar)
    t3.start()


class style():
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        UNDERLINE = '\033[4m'
        RESET = '\033[0m'

messagefile = "message.txt"
numerosfile = "numbers.txt"
numbers = [] 

def saveFiles(filetosave):
    if filetosave == "numeros":
        f = open(numerosfile, "w", encoding="utf-8")
        f.write(ma.tbNumeros.get("0.0", "end-1c"))
        f.close
        ma.send("Contatos Salvos...", "lightgreen")
    else:
        f = open(messagefile, "w", encoding="utf-8")
        f.write(ma.tbMensagem.get("0.0", "end-1c"))
        f.close
        ma.send("Mensagem Salva...", "lightgreen")

def carregar():    
    if os.path.exists(messagefile):
        f = open(messagefile, "r", encoding="utf8")
        message = f.read()
        f.close()
        ma.tbMensagem.delete("0.0", "end")
        ma.tbMensagem.insert("0.0", message)
        
    if os.path.exists(numerosfile):
        with open(numerosfile, "r") as f:
            loaded_numbers = [line.strip() for line in f.readlines() if line.strip()]
        ma.tbNumeros.delete("0.0", "end")
        ma.tbNumeros.insert("0.0", "\n".join(loaded_numbers))

delay = 30
driver = None
status = False

def logar():

    global driver
    options = webdriver.ChromeOptions()
    #options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--profile-directory=Default")
    options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

    os.system("")
    os.environ["WDM_LOG_LEVEL"] = "0"
    


    driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=options)
    print('Once your browser opens up sign in to web whatsapp')
    driver.get('https://web.whatsapp.com')
    #input(style.MAGENTA + "AFTER logging into Whatsapp Web is complete and your chats are visible, press ENVIAR..." + style.RESET)
    #ma.send("Logado, clica em ENVIAR para começar", "darkgreen")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='grid']"))  # Elemento principal do WhatsApp Web
        )
        ma.send("\nLogado com sucesso! Agora você pode clicar em ENVIAR.", "lightgreen")
    except Exception:
        ma.send("Erro ao detectar login. Certifique-se de estar logado no WhatsApp Web.", "red")

def pause(command):
    if command == "pausar": 
        ma.send("Pausado!", "yellow")
        ma.btPause.configure(image=ma.playicon, 
                             command=lambda: pause("continuar"))
    else:
        pass
        ma.send("Continuando!", "yellow")
        ma.btPause.configure(image=ma.pauseicon, 
                             command=lambda: pause("pausar"))
    
def parar():
    global status
    global driver
    if driver == None:
        ma.send("Macro não esta em operação", "red")
        status = False
    else:
        status = True
        driver.close()
        driver = None
        ma.send("Cancelado", "red")

def enviar():
    global driver
    if driver is None:
        ma.send("Erro: Você prescisa estar LOGADO", "red")
        return
    
    if ma.tbNumeros.get("0.0", "end-1c") == "":
        ma.send("Erro: Adicione os Numeros", "red")
        return
    
    if ma.tbMensagem.get("0.0", "end-1c") == "":
        ma.send("Erro: Adicione a Mensagem", "red")
        return
    
    numbers.clear()
    numbers.extend(ma.tbNumeros.get("0.0", "end").strip().split("\n"))

    total_number=len(numbers)
    ma.send('\nTotal de ' + str(total_number) + ' numeros', "red")

    message = ma.tbMensagem.get("0.0", "end")
    ma.send("\nEssa é a sua Mensagem:", "lightgreen")
    ma.send(message, "white")
    message = quote(message)

    for idx, number in enumerate(numbers):
        if status:
            return
        number = number.strip()
        if number == "":
            continue
        ma.send('{}/{} => Sending message to {}.'.format((idx+1), total_number, number), "yellow")
        try:
            url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message
            sent = False
            for i in range(1):
                if not sent:
                    driver.get(url)
                    try:
                        sleep(15)
                        #click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='compose-btn-send']")))
                        click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-tab='11']")))
                    except Exception as e:
                        retry = (i+1)
                        ma.send("Failed to send message to: " + number + ", retry ("+ str(retry) + "/1)", "red")
                        ma.send("Make sure your phone and computer is connected to the internet.", "red")
                        ma.send("If there is an alert, please dismiss it.", "red")
                    else:
                        sleep(1)
                        click_btn.click()
                        sent=True
                        sleep(3)
                        ma.send('Message sent to: ' + number, "green")
        except Exception as e:
            ma.send('Failed to send message to ' + number + str(e) , "red")

    ma.send("Concluído", "lightgreen")
