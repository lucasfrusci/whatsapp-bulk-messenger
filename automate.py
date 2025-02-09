from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
import os

#import ui_gui as ma

import threading

def Tcarregar():
    t1=threading.Thread(target=carregar)
    t1.start()

def Tlogar(send, btLogar):
    t2=threading.Thread(target=lambda:logar(send))
    t2.start()

def Tenviar(send,btPause,playicon, tbNumeros,tbMensagem,pauseicon):
    t3=threading.Thread(target=lambda:enviar(send,btPause,playicon, tbNumeros,tbMensagem,pauseicon))
    t3.start()

def userProfile():
    sleep(5)
    perfil_btn = driver.find_element(By.XPATH, '//header//button[@aria-label="Profile"]')
    perfil_btn.click()
        
    sleep(2)  # Tempo para abrir o menu do perfil

    # Obter o nome do usuário
    nome_usuario = driver.find_element(By.XPATH, '//span//div[contains(@class, "xs83m0k x1g77sc7 xeuugli")]/div/div').text
    #print(nome_usuario)
    ma.user.configure(text=nome_usuario)
    ma.user.place(x=10, y=50)

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
current_number = 0

def saveFiles(filetosave, send, tbMensagem, tbNumeros):
    if filetosave == "numeros":
        f = open(numerosfile, "w", encoding="utf-8")
        f.write(tbNumeros.get("0.0", "end-1c"))
        f.close
        send("Contatos Salvos...", "lightgreen")
    else:
        f = open(messagefile, "w", encoding="utf-8")
        f.write(tbMensagem.get("0.0", "end-1c"))
        f.close
        send("Mensagem Salva...", "lightgreen")

def carregar(tbMensagem, tbNumeros):    
    if os.path.exists(messagefile):
        f = open(messagefile, "r", encoding="utf8")
        message = f.read()
        f.close()
        tbMensagem.delete("0.0", "end")
        tbMensagem.insert("0.0", message)
        
    if os.path.exists(numerosfile):
        with open(numerosfile, "r") as f:
            loaded_numbers = [line.strip() for line in f.readlines() if line.strip()]
        tbNumeros.delete("0.0", "end")
        tbNumeros.insert("0.0", "\n".join(loaded_numbers))

delay = 30
driver = None
status = False

def logar(send):
    send("\nEscaneie o QR CODE e faça o LOGIN ou aguarde o CHAT aparecer", "yellow")
    global driver
    options = webdriver.ChromeOptions()
    #options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--profile-directory=Default")
    options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

    os.system("")
    os.environ["WDM_LOG_LEVEL"] = "0"
    
    driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=options)
    #driver = webdriver.Chrome(options=options)
    print('Once your browser opens up sign in to web whatsapp')
    driver.get('https://web.whatsapp.com')
    #input(style.MAGENTA + "AFTER logging into Whatsapp Web is complete and your chats are visible, press ENVIAR..." + style.RESET)
    #ma.send("Logado, clica em ENVIAR para começar", "darkgreen")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='grid']"))  # Elemento principal do WhatsApp Web
        )
        send("\nLogado com sucesso! Agora você pode clicar em ENVIAR.", "lightgreen")
    except Exception:
        sleep(0.01)
        #ma.send("\nErro ao detectar login. Certifique-se de estar logado no WhatsApp Web.", "red")

def pause(command,send,btPause,playicon, tbNumeros,tbMensagem,pauseicon):
    global status
    if command == "pausar": 
        status = True
        send("Pausando...", "yellow")
        btPause.configure(image=playicon, 
                             text="RETOMAR",
                             command=lambda: pause("continuar"))
    else:
        status = False
        #ma.send("Continuando!", "yellow")
        Tenviar(send,btPause,playicon, tbNumeros,tbMensagem,pauseicon)
        #ma.btPause.configure(image=ma.pauseicon, 
        #                    command=lambda: pause("pausar"))
    
def parar(send,btPause,playicon):
    global current_number
    global status
    global driver
    if driver == None:
        send("Macro não esta em operação", "red")
        status = False
    else:
        status = True
        driver.close()
        driver = None
        current_number = 0
        send("Cancelado!", "red")
        btPause.configure(image=playicon, 
                             text="ENVIAR",
                            command=lambda: pause("continuar"))

def enviar(send,btPause,playicon, tbNumeros,tbMensagem,pauseicon):
    global current_number
    global driver
    
    options = webdriver.ChromeOptions()
    options.add_argument("--profile-directory=Default")
    options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=options)

    if driver is None:
        send("Erro: Você prescisa estar LOGADO", "red")
        return
    
    if tbNumeros.get("0.0", "end-1c") == "":
        send("Erro: Adicione os Numeros", "red")
        return
    
    if tbMensagem.get("0.0", "end-1c") == "":
        send("Erro: Adicione a Mensagem", "red")
        return
    
    btPause.configure(image=pauseicon, 
                         text="PAUSAR",
                         command=lambda: pause("pausar"))
    
    numbers.clear()
    numbers.extend(tbNumeros.get("0.0", "end").strip().split("\n"))

    total_number=len(numbers)
    send('\nTotal de ' + str(total_number) + ' numeros', "red")

    message = tbMensagem.get("0.0", "end")
    send("\nEssa é a sua Mensagem:", "lightgreen")
    send(message, "white")
    message = quote(message)

    while current_number < total_number:
    #for idx, number in enumerate(numbers):
        number = numbers[current_number]
        if status:
            #ma.send("PAUSADO!", "red")
            return
        number = number.strip()
        if number == "":
            continue
        send('{}/{} => Sending message to {}.'.format((current_number+1), total_number, number), "yellow")
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
                        send("Failed to send message to: " + number + ", retry ("+ str(retry) + "/1)", "red")
                        send("Make sure your phone and computer is connected to the internet.", "red")
                        send("If there is an alert, please dismiss it.", "red")
                        if retry > 1:
                            current_number = (current_number+1)
                    else:
                        sleep(1)
                        click_btn.click()
                        sent=True
                        sleep(3)
                        current_number = (current_number+1)
                        send('Message sent to: ' + number, "green")
        except Exception as e:
            send('Failed to send message to ' + number + str(e) , "red")
    #CONCLUIDO RESETA A CONTAGEM E RESTAURA O BOTAO
    current_number = 0
    driver.close()
    send("Concluído", "lightgreen")
    btPause.configure(image=playicon, 
                             text="ENVIAR",
                            command=lambda: pause("continuar"))