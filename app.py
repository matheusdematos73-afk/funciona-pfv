from flask import Flask, request, jsonify, Response
import ast
import operator

app = Flask(__name__)

# =========================
# MEMÓRIA
# =========================

memoria = {}


# =========================
# CALCULADORA SEGURA
# =========================

operacoes = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def calcular(expressao):
    expressao = expressao.replace("x", "*")
    expressao = expressao.replace("X", "*")
    expressao = expressao.replace("÷", "/")

    try:
        arvore = ast.parse(expressao, mode="eval")
        return executar_calculo(arvore.body)
    except:
        return None


def executar_calculo(no):
    if isinstance(no, ast.Constant):
        if isinstance(no.value, (int, float)):
            return no.value
        raise ValueError

    if isinstance(no, ast.BinOp):
        operacao = operacoes.get(type(no.op))
        if not operacao:
            raise ValueError

        esquerda = executar_calculo(no.left)
        direita = executar_calculo(no.right)

        return operacao(esquerda, direita)

    if isinstance(no, ast.UnaryOp):
        operacao = operacoes.get(type(no.op))
        if not operacao:
            raise ValueError

        return operacao(executar_calculo(no.operand))

    raise ValueError


# =========================
# CHATBOT
# =========================

def responder(mensagem):
    mensagem_original = mensagem
    mensagem = mensagem.lower().strip()

    # -------------------------
    # SAUDAÇÕES
    # -------------------------

    if mensagem in [
        "oi",
        "olá",
        "ola",
        "opa",
        "eae",
        "e aí",
        "eai",
        "salve",
        "hello"
    ]:
        return "Olá! 😃 Como você está?"

    if mensagem in [
        "tudo bem",
        "tudo bem?",
        "como você está",
        "como vc está"
    ]:
        return "Estou bem! 😎 E você?"

    if mensagem in [
        "blz",
        "beleza",
        "tranquilo"
    ]:
        return "Boa! 😎"

    # -------------------------
    # NOME
    # -------------------------

    if mensagem.startswith("meu nome é "):
        nome = mensagem_original[11:].strip()

        if nome:
            memoria["nome"] = nome
            return f"Prazer em te conhecer, {nome}! 😃"

    if mensagem.startswith("meu nome e "):
        nome = mensagem_original[11:].strip()

        if nome:
            memoria["nome"] = nome
            return f"Prazer em te conhecer, {nome}! 😃"

    if "qual é meu nome" in mensagem or "qual meu nome" in mensagem:
        if "nome" in memoria:
            return f"Seu nome é {memoria['nome']}! 😎"
        return "Você ainda não me contou seu nome."

    # -------------------------
    # SOBRE O CHATBOT
    # -------------------------

    if "quem é você" in mensagem or "quem vc é" in mensagem:
        return "Eu sou um chatbot criado em Python! 🤖"

    if "o que é um chatbot" in mensagem:
        return (
            "Um chatbot é um programa que conversa com pessoas "
            "e responde mensagens automaticamente. 🤖"
        )

    if "o que você sabe fazer" in mensagem:
        return (
            "Posso conversar, lembrar algumas informações, "
            "responder perguntas simples e fazer cálculos. 😎"
        )

    # -------------------------
    # DESPEDIDA
    # -------------------------

    if mensagem in [
        "tchau",
        "até mais",
        "ate mais",
        "falou",
        "flw"
    ]:
        return "Até mais! 👋"

    # -------------------------
    # AGRADECIMENTOS
    # -------------------------

    if mensagem in [
        "obrigado",
        "obrigada",
        "valeu",
        "vlw"
    ]:
        return "De nada! 😎"

    # -------------------------
    # CALCULADORA
    # -------------------------

    resultado = calcular(mensagem)

    if resultado is not None:
        if isinstance(resultado, float) and resultado.is_integer():
            resultado = int(resultado)

        return f"O resultado é {resultado}"

    # -------------------------
    # RESPOSTA PADRÃO
    # -------------------------

    return (
        "Ainda não sei responder isso 😅\n"
        "Mas você pode me ensinar novas respostas!"
    )


# =========================
# SITE
# =========================

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">

<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Meu Chatbot</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #0D0D0D;
    color: white;
    font-family: Arial, sans-serif;
    height: 100vh;
    overflow: hidden;
}

#inicio {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

.titulo {
    font-size: 32px;
    margin-bottom: 30px;
    color: #00D9FF;
}

#botaoInicio {
    background: #00D9FF;
    color: #000;
    border: none;
    border-radius: 14px;
    padding: 16px 30px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
}

#botaoInicio:hover {
    opacity: 0.85;
}

#chat {
    display: none;
    height: 100vh;
    flex-direction: column;
}

.cabecalho {
    height: 65px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom: 1px solid #222;
    color: #00D9FF;
    font-size: 22px;
    font-weight: bold;
}

#mensagens {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.mensagem {
    max-width: 80%;
    padding: 12px 15px;
    border-radius: 15px;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.usuario {
    align-self: flex-end;
    background: #00D9FF;
    color: #000;
}

.bot {
    align-self: flex-start;
    background: #202020;
    color: white;
}

.areaEntrada {
    display: flex;
    gap: 10px;
    padding: 12px;
    border-top: 1px solid #222;
    background: #0D0D0D;
}

#entrada {
    flex: 1;
    min-width: 0;
    background: #1B1B1B;
    color: white;
    border: 1px solid #333;
    border-radius: 14px;
    padding: 14px;
    font-size: 16px;
    outline: none;
}

#entrada:focus {
    border-color: #00D9FF;
}

#enviar {
    background: #00D9FF;
    color: #000;
    border: none;
    border-radius: 14px;
    padding: 0 18px;
    font-weight: bold;
    cursor: pointer;
}

#enviar:active {
    transform: scale(0.96);
}

@media (max-width: 500px) {

    .titulo {
        font-size: 27px;
    }

    .cabecalho {
        font-size: 19px;
    }

    #mensagens {
        padding: 12px;
    }

    .mensagem {
        max-width: 88%;
    }

    .areaEntrada {
        padding: 8px;
    }

    #entrada {
        font-size: 15px;
        padding: 12px;
    }

    #enviar {
        padding: 0 14px;
    }
}

</style>
</head>

<body>

<!-- TELA INICIAL -->

<div id="inicio">

    <div class="titulo">
        Meu Chatbot
    </div>

    <button id="botaoInicio" onclick="iniciar()">
        CHATBOT - INICIAR
    </button>

</div>


<!-- CHAT -->

<div id="chat">

    <div class="cabecalho">
        Meu Chatbot 🤖
    </div>

    <div id="mensagens"></div>

    <div class="areaEntrada">

        <input
            id="entrada"
            type="text"
            placeholder="Digite uma mensagem..."
            autocomplete="off"
        >

        <button id="enviar" onclick="enviarMensagem()">
            ENVIAR
        </button>

    </div>

</div>


<script>

function iniciar() {

    document.getElementById("inicio").style.display = "none";

    document.getElementById("chat").style.display = "flex";

    adicionarMensagem(
        "bot",
        "Olá! 👋 Eu sou seu chatbot. Como posso ajudar?"
    );

    document.getElementById("entrada").focus();
}


function adicionarMensagem(tipo, texto) {

    const area = document.getElementById("mensagens");

    const mensagem = document.createElement("div");

    mensagem.classList.add("mensagem");

    if (tipo === "usuario") {
        mensagem.classList.add("usuario");
    } else {
        mensagem.classList.add("bot");
    }

    mensagem.textContent = texto;

    area.appendChild(mensagem);

    area.scrollTop = area.scrollHeight;
}


async function enviarMensagem() {

    const entrada = document.getElementById("entrada");

    const texto = entrada.value.trim();

    if (!texto) {
        return;
    }

    adicionarMensagem("usuario", texto);

    entrada.value = "";

    entrada.disabled = true;

    try {

        const resposta = await fetch("/mensagem", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                mensagem: texto
            })

        });

        const dados = await resposta.json();

        adicionarMensagem(
            "bot",
            dados.resposta
        );

    } catch (erro) {

        adicionarMensagem(
            "bot",
            "Erro ao conectar com o servidor. 😕"
        );

    }

    entrada.disabled = false;

    entrada.focus();
}


document
.getElementById("entrada")
.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        enviarMensagem();
    }

});

</script>

</body>
</html>
"""


# =========================
# ROTAS
# =========================

@app.route("/")
def inicio():
    return Response(HTML, mimetype="text/html")


@app.route("/mensagem", methods=["POST"])
def mensagem():

    dados = request.get_json()

    if not dados:
        return jsonify({
            "resposta": "Não recebi nenhuma mensagem."
        })

    texto = dados.get("mensagem", "")

    resposta = responder(texto)

    return jsonify({
        "resposta": resposta
    })


# =========================
# EXECUÇÃO LOCAL
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )