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

class colors():
    FUNDO = "#242424"
    CINZA = "#3b3b3b"
    VRANCO = "#ffffff"
    WHATSAPP = "#25D366"


root = ctk.CTk()
root.geometry("800x600")
ctk.set_default_color_theme("green")
root.title("WhatsApp - AUTO MENSAGENS")
root.resizable(False,False)
root.configure(fg_color= colors.FUNDO)
appicon = get_resource_path("icon.ico")
root.iconbitmap(appicon)

#ICONES
class ICONES():
    saveicon = get_resource_path("save.png")
    saveicon = PhotoImage(file=saveicon)

    playicon = get_resource_path("play.png")
    playicon = PhotoImage(file=playicon)

    pauseicon = get_resource_path("pause.png")
    pauseicon = PhotoImage(file=pauseicon)

    stopicon = get_resource_path("cancel.png")
    stopicon = PhotoImage(file=stopicon)

    delicon = get_resource_path("delete.png")
    delicon = PhotoImage(file=delicon)

    filtericon = get_resource_path("filter.png")
    filtericon = PhotoImage(file=filtericon)

    openicon = get_resource_path("open.png")
    openicon = PhotoImage(file=openicon)

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
#btEnviar.place(x=10, y=315)

#TEXTBOX NUMEROS
tbNumeros = ctk.CTkTextbox(root, width=230, height=200, font=("", 16))
tbNumeros.insert("0.0", "Adicione os contatos")
tbNumeros.place(x=10, y=100)

#BOTAO SALVAR NUMEROS
BtNumeros = ctk.CTkButton(tbNumeros, 
                    width=40,
                    height=40,
                    text="",
                    fg_color=colors.FUNDO,
                    image=ICONES.saveicon,
                    command=lambda: auto.saveFiles(tbNumeros, 1))
BtNumeros.place(x=180, y=150)

BtNfiltrar = ctk.CTkButton(tbNumeros, 
                    width=40,
                    height=40,
                    text="",
                    fg_color=colors.FUNDO,
                    image=ICONES.filtericon,
                    command=lambda: auto.filtrar(tbNumeros))
BtNfiltrar.place(x=130, y=150)

btNcarrecar = ctk.CTkButton(tbNumeros, 
                    width=40,
                    height=40,
                    text="",
                    fg_color=colors.FUNDO,
                    image=ICONES.openicon,
                    command=lambda: auto.abrir(tbNumeros))
btNcarrecar.place(x=180, y=50)

btNdel = ctk.CTkButton(tbNumeros, 
                    width=40,
                    height=40,
                    text="",
                    fg_color=colors.FUNDO,
                    image=ICONES.delicon,
                    command=lambda: auto.deletar(tbNumeros))
btNdel.place(x=180, y=100)

btcontatos = ctk.CTkButton(tbNumeros, 
                    width=60,
                    height=40,
                    font=("", 10, "bold"), 
                    text="BUSCAR NUMEROS",
                    fg_color= colors.FUNDO,
                    #image=stopicon,
                    command=lambda:auto.Tcontatos(tbNumeros, send))
btcontatos.place(x=10, y=150)



#TEXTBOX MENSAGEM
tbMensagem = ctk.CTkTextbox(root, width=540, height=200, font=("", 16))
tbMensagem.insert("0.0", "Digite a mensagem")
tbMensagem.place(x=250, y=100)

#BOTAO SALVAR MENSAGEM
BtMensagem = ctk.CTkButton(tbMensagem, 
                    width=40,
                    height=40,
                    text="",
                    fg_color=colors.FUNDO,
                    image=ICONES.saveicon,
                    command=lambda: auto.saveFiles(tbMensagem, 2))
BtMensagem.place(x=490, y=150)

#BOTAO APAGAR MENSAGEM
BtmDEL = ctk.CTkButton(tbMensagem, 
                    width=40,
                    height=40,
                    text="",
                    fg_color=colors.FUNDO,
                    image=ICONES.delicon,
                    command=lambda: auto.deletar(tbMensagem))
BtmDEL.place(x=440, y=150)

#BOTOES PLAY, PAUSE E PARAR

btPause = ctk.CTkButton(root, width=40, 
                        height=40,
                        text="ENVIAR", 
                        fg_color="transparent", 
                        image=ICONES.playicon, 
                        command=lambda: auto.pause("continuar"))
btPause.place(x=10, y=310)

btParar = ctk.CTkButton(root, 
                    width=40,
                    height=40,
                    text="CANCELAR",
                    fg_color="transparent",
                    image=ICONES.stopicon,
                    command=auto.parar)
btParar.place(x=200, y=310)



entryLabel = ctk.CTkLabel(root,
                          text="INTERVALO",
                          #font=("", 14), 
                          )
entryLabel.place(x=395, y=316)

entryTempo = ctk.CTkEntry(root, 
                    width=38,
                    height=20,
                    font=("", 20), 
                    )
                    #font=("", 10, "bold"), 
                    #text="FILTRAR NUMEROS")
                    #fg_color="transparent",
                    #image=stopicon,
                    #command=lambda:auto.Tcontatos(tbNumeros, send))
entryTempo.place(x=350, y=315)
entryTempo.insert(0, 15)


#TEXTBOX LOG
tbLog = ctk.CTkTextbox(root, width=780, height=230, font=("Cascadia Mono", 16))
tbLog.insert("0.0", "Clica em LOGAR e entra na sua conta WhatsApp Web.\n")
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