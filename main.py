import customtkinter as ctk
import automate as auto
import threading

root = ctk.CTk()
root.geometry("800x600")
root.title("WhatsApp MALA DIRETA")
root.resizable(False,False)
root.iconbitmap("icon.ico")

def send(message, color):
    tbLog.configure(state="normal")  # Habilita a edição
    
    tag_name =  "color-" + str(id(message))
    tbLog.tag_config(tag_name, foreground=color)
    tbLog.insert("end", message + "\n", tag_name)
    #tbLog.tag_add("colored", "end-1c linestart", "end-1c lineend")

    tbLog.see("end")
    tbLog.configure(state="disabled")
    

labelTop = ctk.CTkLabel(root, 
                        text="WhatsApp MALA DIRETA", 
                        font=("Segoe UI", 20), 
                        height=10, width=10, 
                        text_color="lightgreen")
labelTop.place(x=10, y=10)

btLogar = ctk.CTkButton(root, 
                        text="LOGAR", 
                        fg_color="transparent", 
                        hover_color="green", 
                        border_width=1, 
                        border_color="white", 
                        command=auto.Tlogar)
btLogar.place(x=10, y=50)

btEnviar = ctk.CTkButton(root, 
                         text="ENVIAR", 
                         fg_color="transparent", 
                         hover_color="green", 
                         border_width=1, 
                         border_color="white", 
                         command=auto.Tenviar)
#btEnviar.configure(command=lambda: send("**********************************************************\n"
#                 "**********************************************************\n"
#                 "*****                                               ******\n"
#                "*****  THANK YOU FOR USING WHATSAPP BULK MESSENGER  ******\n"
#                 "*****      This tool was built by Anirudh Bagri     ******\n"
#                 "*****           www.github.com/anirudhbagri         ******\n"
#                 "*****                                               ******\n"
#                 "**********************************************************\n"
#                 "**********************************************************", "white"))
btEnviar.place(x=10, y=320)
#btEnviar.configure(hover_color="purple")


#TEXTBOX NUMEROS
tbNumeros = ctk.CTkTextbox(root, width=180, height=200)
tbNumeros.insert("0.0", "Adicione os contatos")
tbNumeros.place(x=10, y=100)

#TEXTBOX MENSAGEM
tbMensagem = ctk.CTkTextbox(root, width=590, height=200)
tbMensagem.insert("0.0", "Digite a mensagem")
tbMensagem.place(x=200, y=100)

#TEXTBOX LOG
tbLog = ctk.CTkTextbox(root, width=780, height=210, font=("Arial", 20))
tbLog.insert("0.0", "Clica em logar e entra na sua conta WhatsApp web...\n")
tbLog.place(x=10, y=380)
tbLog.configure(state="disabled", wrap="word")

auto.carregar()

root.mainloop()


def send():
    tbLog.insert("0.0","**********************************************************\n"
                 "**********************************************************\n"
                 "*****                                               ******\n"
                 "*****  THANK YOU FOR USING WHATSAPP BULK MESSENGER  ******\n"
                 "*****      This tool was built by Anirudh Bagri     ******\n"
                 "*****           www.github.com/anirudhbagri         ******\n"
                 "*****                                               ******\n"
                 "**********************************************************\n"
                 "**********************************************************")