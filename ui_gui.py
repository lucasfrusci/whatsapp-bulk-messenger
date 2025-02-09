from tkinter import PhotoImage
import customtkinter as ctk
import automate as auto
import threading

def get_resource_path(relative_path):
    try:
        base_path = ctk.sys._MEIPASS
    except Exception:
        base_path = ctk.os.path.abspath(".")
    return ctk.os.path.join(base_path, relative_path)


root = ctk.CTk()
root.geometry("800x600")
ctk.set_default_color_theme("green")
root.title("WhatsApp - AUTO MENSAGENS")
root.resizable(False,False)
appicon = get_resource_path("icon.ico")
root.iconbitmap(appicon)

#ICONES
saveicon = get_resource_path("save.png")
saveicon = PhotoImage(file=saveicon)

#playicon = get_resource_path("play.png")
#playicon = PhotoImage(file=playicon)

#pauseicon = get_resource_path("pause.png")
#pauseicon = PhotoImage(file=pauseicon)

stopicon = get_resource_path("stop.png")
stopicon = PhotoImage(file=stopicon)

def send(message, color):
    tbLog.configure(state="normal")  # Habilita a edição
    
    tag_name =  "color-" + str(id(message))
    tbLog.tag_config(tag_name, foreground=color)
    tbLog.insert("end", message + "\n", tag_name)
    #tbLog.tag_add("colored", "end-1c linestart", "end-1c lineend")

    tbLog.see("end")
    tbLog.configure(state="disabled")


labelTop = ctk.CTkLabel(root, 
                        text="WhatsApp - AUTO MENSAGENS", 
                        font=("Segoe UI", 20), 
                        height=10, width=10, 
                        text_color="lightgreen")
labelTop.place(x=10, y=10)

btLogar = ctk.CTkButton(root, 
                        text="LOGAR", 
                        fg_color="transparent", 
                        #hover_color="green", 
                        border_width=1, 
                        border_color="white", 
                        command=auto.Tlogar)
btLogar.place(x=10, y=50)

btEnviar = ctk.CTkButton(root, 
                         text="ENVIAR", 
                         fg_color="transparent", 
                         #hover_color="green", 
                         border_width=1, 
                         border_color="white", 
                         command=auto.Tenviar)
btEnviar.place(x=10, y=315)


#TEXTBOX NUMEROS
tbNumeros = ctk.CTkTextbox(root, width=180, height=200, font=("", 16))
tbNumeros.insert("0.0", "Adicione os contatos")
tbNumeros.place(x=10, y=100)

#BOTAO SALVAR NUMEROS
BtNumeros = ctk.CTkButton(root, 
                    width=40,
                    height=40,
                    text="",
                    fg_color="transparent",
                    image=saveicon,
                    command=lambda: auto.saveFiles("numeros"))
BtNumeros.place(x=140, y=250)



#TEXTBOX MENSAGEM
tbMensagem = ctk.CTkTextbox(root, width=590, height=200, font=("", 16))
tbMensagem.insert("0.0", "Digite a mensagem")
tbMensagem.place(x=200, y=100)

#BOTAO SALVAR MENSAGEM
BtMensagem = ctk.CTkButton(root, 
                    width=40,
                    height=40,
                    text="",
                    fg_color="transparent",
                    image=saveicon,
                    command=lambda: auto.saveFiles("mensagem"))
BtMensagem.place(x=740, y=250)

#BOTOES PLAY, PAUSE E PARAR

#btPause = ctk.CTkButton(root, width=40, height=40,text="", fg_color="transparent", image=stopicon, command=lambda: auto.pause("pausar"))
#btPause.place(x=200, y=310)

btParar = ctk.CTkButton(root, 
                    width=40,
                    height=40,
                    text="",
                    fg_color="transparent",
                    image=stopicon,
                    command=auto.parar)
btParar.place(x=200, y=310)


#TEXTBOX LOG
tbLog = ctk.CTkTextbox(root, width=780, height=230, font=("Arial", 20))
tbLog.insert("0.0", "Clica em LOGAR e entra na sua conta WhatsApp web...\n")
tbLog.place(x=10, y=360)
tbLog.configure(state="disabled", wrap="word")

auto.carregar()

root.mainloop()


def send2():
    tbLog.insert("0.0","**********************************************************\n"
                 "**********************************************************\n"
                 "*****                                               ******\n"
                 "*****  THANK YOU FOR USING WHATSAPP BULK MESSENGER  ******\n"
                 "*****      This tool was built by Anirudh Bagri     ******\n"
                 "*****           www.github.com/anirudhbagri         ******\n"
                 "*****                                               ******\n"
                 "**********************************************************\n"
                 "**********************************************************")