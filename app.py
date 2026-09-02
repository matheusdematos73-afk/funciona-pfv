from flask import Flask, render_template, request, jsonify
import random
import ast
import operator

app = Flask(__name__)

# Memória simples enquanto o servidor estiver rodando
memoria = {}

saudacoes = [
    "oi", "olá", "ola", "oii", "oiii", "oiê",
    "e aí", "eai", "opa", "salve"
]

respostas_saudacao = [
    "Opa! 😎", "E aí! 👋", "Fala!", "Oi! 😄",
    "Olá!", "E aí, beleza?", "Opa, tudo certo?",
    "Fala aí! 😎", "Salve! 👋", "E aí! Como você tá?"
]

# Calculadora segura para operações básicas
operadores = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def calcular(expressao):
    expressao = expressao.replace("x", "*").replace("X", "*").replace("÷", "/")

    def avaliar(no):
        if isinstance(no, ast.Expression):
            return avaliar(no.body)
        if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)):
            return no.value
        if isinstance(no, ast.UnaryOp) and type(no.op) in operadores:
            return operadores[type(no.op)](avaliar(no.operand))
        if isinstance(no, ast.BinOp) and type(no.op) in operadores:
            esquerda = avaliar(no.left)
            direita = avaliar(no.right)
            return operadores[type(no.op)](esquerda, direita)
        raise ValueError

    arvore = ast.parse(expressao, mode="eval")
    return avaliar(arvore)

def responder(mensagem):
    mensagem = mensagem.lower().strip()

    if any(saudacao in mensagem for saudacao in saudacoes):
        return random.choice(respostas_saudacao)

    if mensagem in ["o que é um chatbot?", "o que e um chatbot?"]:
        return "Um chatbot é um programa de computador que conversa com pessoas e responde mensagens."

    if mensagem in [
        "o que voce consegue fazer?", "oq voce consegue fazer?",
        "oq vc consegue fazer?", "o que vc consegue fazer?",
        "o que vc faz?", "oq vc faz?"
    ]:
        return "Eu consigo conversar, responder perguntas e realizar algumas funções básicas."

    if mensagem.startswith("meu nome é ") or mensagem.startswith("meu nome e "):
        prefixo = "meu nome é " if mensagem.startswith("meu nome é ") else "meu nome e "
        nome = mensagem[len(prefixo):].strip()
        if nome:
            memoria["nome"] = nome
            return "Prazer, " + nome + "! Vou lembrar do seu nome."
        return "Você não colocou um nome."

    if "qual é meu nome?" in mensagem or "qual e meu nome?" in mensagem:
        if "nome" in memoria:
            return "Seu nome é " + memoria["nome"] + "."
        return "Você ainda não me disse seu nome."

    if any(simbolo in mensagem for simbolo in ["+", "-", "x", "÷", "*", "/"]):
        try:
            resultado = calcular(mensagem)
            return str(resultado)
        except Exception:
            return "Não consegui calcular essa conta porque está incompleta."

    return "Não entendi ainda, preciso aprender."

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/mensagem", methods=["POST"])
def mensagem():
    dados = request.get_json(silent=True) or {}
    texto = dados.get("mensagem", "")
    return jsonify({"resposta": responder(texto)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
