from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
import os

import main as ma

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

def carregar():
    
    if os.path.exists(messagefile):
        f = open("message.txt", "r", encoding="utf8")
        message = f.read()
        f.close()
        ma.tbMensagem.delete("0.0", "end")
        ma.tbMensagem.insert("0.0", message)
        
    if os.path.exists(numerosfile):
        f = open("numbers.txt", "r")
        for line in f.read().splitlines():
            if line.strip() != "":
                numbers.append(line.strip())
        f.close()
        ma.tbNumeros.delete("0.0", "end")
        ma.tbNumeros.insert("0.0", numbers)

delay = 30
driver = None

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
    ma.send("Logado, clica em ENVIAR para começar", "purple")

def enviar():

    global driver
    if driver is None:
        print("Error: You must log in first!")
        return
    
    numbers.append(ma.tbNumeros.get("0.0", "end"))
    total_number=len(numbers)
    ma.send('We found ' + str(total_number) + ' numbers in the file', "red")

    message = ma.tbMensagem.get("0.0", "end")
    ma.send("Essa é a sua Mensagem:", "green")
    ma.send(message, "green")
    message = quote(message)

    for idx, number in enumerate(numbers):
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
                        ma.send("Failed to send message to: {number}, retry ({i+1}/1)", "red")
                        ma.send("Make sure your phone and computer is connected to the internet.", "red")
                        ma.send("If there is an alert, please dismiss it.", "red")
                    else:
                        sleep(1)
                        click_btn.click()
                        sent=True
                        sleep(3)
                        ma.send('Message sent to: ' + number + style.RESET, "green")
        except Exception as e:
            ma.send('Failed to send message to ' + number + str(e) + style.RESET, "red")
