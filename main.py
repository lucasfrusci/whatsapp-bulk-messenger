import customtkinter as ctk
janela = ctk.CTk()
janela.geometry("800x600")
janela.title("WhatsApp Mensagem")
janela.resizable(False,False)

labelTop = ctk.CTkLabel(janela, text="WhatsApp MENSAGEM AUTO", font=("Segoe UI", 20), height=10, width=10, text_color="green").place(x=10, y=10)

#TEXTBOX NUMEROS
tbNumeros = ctk.CTkTextbox(janela, width=250, height=200)
tbNumeros.insert("0.0", "ADICIONE AQUI OS CONTATOS")
tbNumeros.place(x=10, y=50)

#TEXTBOX MENSAGEM
tbMensagem = ctk.CTkTextbox(janela, width=250, height=200)
tbMensagem.insert("0.0", "Digite a mensagem")
tbMensagem.place(x=280, y=50)

#TEXTBOX LOG
tbLog = ctk.CTkTextbox(janela, width=780, height=100)
tbLog.insert("0.0", "Logs")
tbLog.place(x=10, y=300)
tbLog.configure(state="disabled")

janela.mainloop()