from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import gmtime, sleep, strftime, time
from urllib.parse import quote
import os
from collections import Counter
from tkinter import filedialog

import ui_gui as ma
import contatos as contatos

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

def Tcontatos(tbNumeros, send):
    t4=threading.Thread(target=contatos.scrool, args=(driver, tbNumeros, send))
    t4.start()

def userProfile():
    sleep(5)
    perfil_btn = driver.find_element(By.XPATH, '//header//button[@aria-label="Profile"]')
    perfil_btn.click()
        
    sleep(2)

    nome_usuario = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/span/div/div/span/div/div/div[2]/div[2]/div/div/span/span').text
    ma.user.configure(text="LOGADO: " + nome_usuario)
    ma.btLogar.place(x=-300, y=50)
    ma.user.place(x=10, y=50)

messagefile = "message.txt"
numerosfile = "numbers.txt"
numbers = [] 
current_number = 0

#variaveis tempo
tempo = 19
t1 = None
t2 = None
t3 = None
t4 = None

def calcule_time(tempo):
    global t1, t3, t4
    t1 = (tempo * .79)
    t2 = tempo - t1
    t3 = t2 * .75
    t4 = t2 - t3
    print(t1, "\n", t2,t3,t4)

#################################

def saveFiles(componente, filetosave):
    if filetosave == 1:
        f = open(numerosfile, "w", encoding="utf-8")
        f.write(componente.get("0.0", "end-1c"))
        f.close
        ma.send("Contatos Salvos...", "lightgreen")
    else:
        f = open(messagefile, "w", encoding="utf-8")
        f.write(componente.get("0.0", "end-1c"))
        f.close
        ma.send("Mensagem Salva...", "lightgreen")

def filtrar(componente):
    texto = componente.get("0.0", "end")
    texto = texto.split()
    palavras = Counter(texto)
    print(texto)

    palavras_filtradas = [palavra for palavra in texto if palavras[palavra] > 0]
    deletar(componente)
    resultado ="\n".join(dict.fromkeys(palavras_filtradas))
    componente.insert("0.0", resultado)

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
chromeuserdata = os.getenv("APPDATA")

def logar():
    ma.send("\nEscaneie o QR CODE e faça o LOGIN, aguarde o CHAT aparecer.", "yellow")
    global driver
    options = webdriver.ChromeOptions()
    #options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--profile-directory=Default")
    #options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")
    options.add_argument(f'--user-data-dir={chromeuserdata}\\ChromeDriver')

    os.system("")
    os.environ["WDM_LOG_LEVEL"] = "0"
    
    driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=options)
    #driver = webdriver.Chrome(options=options)
    #print('Once your browser opens up sign in to web whatsapp')
    driver.get('https://web.whatsapp.com')
    #input(style.MAGENTA + "AFTER logging into Whatsapp Web is complete and your chats are visible, press ENVIAR..." + style.RESET)
    #ma.send("Logado, clica em ENVIAR para começar", "darkgreen")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='grid']"))  # Elemento principal do WhatsApp Web
        )
        ma.send("\nLogado com sucesso! Agora você pode clicar em ENVIAR.", "lightgreen")
    except Exception:
        sleep(0.01)
        #ma.send("\nErro ao detectar login. Certifique-se de estar logado no WhatsApp Web.", "red")

def deletar(componente):
    componente.delete("0.0", "end")

def abrir(componente):
    componente.delete("0.0", "end")
    file = filedialog.askopenfile(mode="r", defaultextension=".txt")
    with file as f:
        loaded_numbers = [line.strip() for line in f.readlines() if line.strip()]
        componente.delete("0.0", "end")
        componente.insert("0.0", "\n".join(loaded_numbers))

        
def pause(command):
    global status
    if command == "pausar": 
        status = True
        ma.send("Pausando...", "yellow")
        ma.btPause.configure(image=ma.ICONES.playicon, 
                             text="RETOMAR",
                             command=lambda: pause("continuar"))
    else:
        status = False
        #ma.send("Continuando!", "yellow")
        Tenviar()
        #ma.btPause.configure(image=ma.ICONES.pauseicon, 
        #                    command=lambda: pause("pausar"))
    
def parar():
    global current_number
    global status
    global driver
    if driver == None:
        ma.send("Nenhuma operação em andamento.", "red")
        status = False
    else:
        status = True
        driver.close()
        driver = None
        current_number = 0
        ma.send("Cancelado!", "red")
        ma.btPause.configure(image=ma.ICONES.playicon, 
                             text="ENVIAR",
                            command=lambda: pause("continuar"))

def enviar():
    global current_number
    global driver
    if driver == None:
        options = webdriver.ChromeOptions()
        options.add_argument("--profile-directory=Default")
        options.add_argument(f'--user-data-dir={chromeuserdata}\\ChromeDriver')
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=options)

    if driver is None:
        ma.send("Erro: Você prescisa estar LOGADO", "red")
        return
    
    if ma.tbNumeros.get("0.0", "end-1c") == "":
        ma.send("Erro: Adicione os Numeros", "red")
        return
    
    if ma.tbMensagem.get("0.0", "end-1c") == "":
        ma.send("Erro: Adicione a Mensagem", "red")
        return
    
    ma.btPause.configure(image=ma.ICONES.pauseicon, 
                         text="PAUSAR",
                         command=lambda: pause("pausar"))
    
    numbers.clear()
    numbers.extend(ma.tbNumeros.get("0.0", "end").strip().split("\n"))
    
    #CAPTURA INTERVALO TEMPO
    tempo = int(ma.entryTempo.get())
    calcule_time(tempo)
    ma.send(str(t1), "red")
    start = time() #inicia a contagem da duração
    ########################
    total_number=len(numbers)
    ma.send('\nTotal de ' + str(total_number) + ' numeros', "yellow")

    message = ma.tbMensagem.get("0.0", "end")
    ma.send("\nEssa é a sua Mensagem:", "lightgreen")
    ma.send(message, "white")
    message = quote(message)

    while current_number < total_number:
        
    #for idx, number in enumerate(numbers):
        number = numbers[current_number]
        if status:
            ma.send("PAUSADO!", "red")
            return
        number = number.strip()
        if number == "":
            continue
        ma.send('{}/{} => Sending message to {}.'.format((current_number+1), total_number, number), "yellow")
        try:
            url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message
            sent = False
            for i in range(1):
                if not sent:
                    driver.get(url)
                    try:
                        sleep(t1)
                        #click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='compose-btn-send']")))
                        click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-tab='11']")))
                    except Exception as e:
                        if status:
                            return
                        retry = (i+1)
                        ma.send("Failed to send message to: " + number + ", retry ("+ str(retry) + "/1)", "red")
                        ma.send("Make sure your phone and computer is connected to the internet.", "red")
                        ma.send("If there is an alert, please dismiss it.", "red")
                        if retry == 1:
                            current_number += 1
                    else:
                        sleep(t4)
                        click_btn.click()
                        sent=True
                        sleep(t3)
                        current_number = (current_number+1)
                        ma.send('Message sent to: ' + number, "green")
                        
        except Exception as e:
            ma.send('Failed to send message to ' + number + str(e) , "red")
    #CONCLUIDO RESETA A CONTAGEM E RESTAURA O BOTAO
    current_number = 0
    driver.close()
    driver = None
    ma.send("Concluído", "lightgreen")
    end = time()
    duracao(start, end)
    ma.btPause.configure(image=ma.ICONES.playicon, 
                             text="ENVIAR",
                            command=lambda: pause("continuar"))
    
def duracao(start, end):
    total = end - start
    total = strftime("%H:%M:%S", gmtime(total))
    ma.send('Duração: ' + total, "White")