import tkinter as tk
import random

janela = tk.Tk()
janela.title("Meu Chatbot")
janela.geometry("600x900")
janela.configure(bg="#0D0D0D")


# =========================
# MEMÓRIA
# =========================

memoria = {}


# =========================
# TELA INICIAL
# =========================

tela_inicial = tk.Frame(
    janela,
    bg="#0D0D0D"
)

tela_inicial.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)


titulo = tk.Label(
    tela_inicial,
    text="Meu Chatbot",
    font=("Arial", 28, "bold"),
    bg="#0D0D0D",
    fg="#00D9FF"
)

titulo.place(
    relx=0.5,
    rely=0.35,
    anchor="center"
)


def abrir_chat():
    tela_inicial.place_forget()

    tela_chat.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

    caixa.focus_set()


botao_iniciar = tk.Button(
    tela_inicial,
    text="CHATBOT - INICIAR",
    font=("Arial", 18, "bold"),
    bg="#00D9FF",
    fg="black",
    command=abrir_chat
)

botao_iniciar.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# =========================
# TELA DO CHAT
# =========================

tela_chat = tk.Frame(
    janela,
    bg="#0D0D0D"
)


area_conversa = tk.Text(
    tela_chat,
    bg="#1A1A1A",
    fg="white",
    font=("Arial", 10)
)

area_conversa.place(
    x=10,
    y=650,
    relwidth=0.97,
    relheight=0.52
)


# =========================
# CAIXA DE MENSAGEM
# =========================

caixa = tk.Entry(
    tela_chat,
    bg="#303030",
    fg="white",
    insertbackground="white",
    font=("Arial", 15)
)

caixa.place(
    relx=0.01,
    rely=0.83,
    relwidth=0.73,
    height=100
)


# =========================
# ENVIAR
# =========================

def enviar_mensagem():

    mensagem = caixa.get().lower().strip()

    if mensagem == "":
        return

    # PRINT DA MENSAGEM
    print("Você:", mensagem)

    area_conversa.insert(
        "end",
        "Você: " + mensagem + "\n\n"
    )


    # =========================
    # SAUDAÇÕES
    # =========================

    saudacoes = [
        "oi",
        "olá",
        "ola",
        "oii",
        "oiii",
        "oiê",
        "e aí",
        "eai",
        "opa",
        "salve"
    ]

    respostas_saudacao = [
        "Opa! 😎",
        "E aí! 👋",
        "Fala!",
        "Oi! 😄",
        "Olá!",
        "E aí, beleza?",
        "Opa, tudo certo?",
        "Fala aí! 😎",
        "Salve! 👋",
        "E aí! Como você tá?"
    ]


    if any(saudacao in mensagem for saudacao in saudacoes):

        resposta = random.choice(
            respostas_saudacao
        )


    # =========================
    # O QUE É CHATBOT
    # =========================

    elif mensagem in [
        "o que é um chatbot?",
        "o que e um chatbot?"
    ]:

        resposta = (
            "Um chatbot é um programa de computador "
            "que conversa com pessoas e responde mensagens."
        )


    # =========================
    # FUNÇÕES
    # =========================

    elif mensagem in [
        "o que voce consegue fazer?",
        "oq voce consegue fazer?",
        "oq vc consegue fazer?",
        "o que vc consegue fazer?",
        "o que vc faz?",
        "oq vc faz?"
    ]:

        resposta = (
            "Eu consigo conversar, responder perguntas "
            "e realizar algumas funções básicas."
        )


    # =========================
    # MEMÓRIA
    # =========================

    elif mensagem.startswith("meu nome é "):

        nome = mensagem.replace(
            "meu nome é ",
            ""
        ).strip()

        memoria["nome"] = nome

        resposta = (
            "Prazer, " + nome +
            "! Vou lembrar do seu nome."
        )


    elif "qual é meu nome?" in mensagem:

        if "nome" in memoria:

            resposta = (
                "Seu nome é " +
                memoria["nome"] +
                "."
            )

        else:

            resposta = (
                "Você ainda não me disse seu nome."
            )


    # =========================
    # CALCULADORA
    # =========================

    elif any(
        simbolo in mensagem
        for simbolo in ["+", "-", "x", "÷"]
    ):

        try:

            conta = mensagem.replace(
                "x",
                "*"
            ).replace(
                "÷",
                "/"
            )

            resultado = eval(conta)

            resposta = str(resultado)

        except:

            resposta = (
                "Não consegui calcular essa conta "
                "porque está incompleta."
            )


    # =========================
    # NÃO ENTENDEU
    # =========================

    else:

        resposta = (
            "Não entendi ainda, preciso aprender."
        )


    # =========================
    # PRINT DA RESPOSTA
    # =========================

    print("Bot:", resposta)


    # =========================
    # MOSTRAR NA TELA
    # =========================

    area_conversa.insert(
        "end",
        "Bot: " + resposta + "\n\n"
    )


    caixa.delete(
        0,
        "end"
    )


# =========================
# BOTÃO ENVIAR
# =========================

botao_enviar = tk.Button(
    tela_chat,
    text="ENVIAR",
    font=("Arial", 12, "bold"),
    bg="#00D9FF",
    fg="black",
    command=enviar_mensagem
)

botao_enviar.place(
    relx=0.76,
    rely=0.83,
    relwidth=0.24,
    height=100
)


# =========================
# ENTER
# =========================

caixa.bind(
    "<Return>",
    lambda evento: enviar_mensagem()
)


janela.mainloop()