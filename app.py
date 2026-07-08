import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify

# Inicializamos a aplicação Flask
app = Flask(__name__)

# ROTA PRINCIPAL: Quando o usuário digita o endereço do site, ele cai aqui
@app.route('/')
def index():
    # Retorna o arquivo 'index.html' que deve estar na pasta 'templates'
    return render_template('index.html')

# CONFIGURAÇÕES DE E-MAIL (Exemplo usando Gmail)
# Dica: Para o Gmail, você precisará criar uma "Senha de App" nas configurações de segurança
EMAIL_QUE_ENVIA = "vinithomazelli@gmail.com"
SENHA_DE_APP = "drcr gbsz rjoa zlbv"
EMAIL_QUE_RECEBE = "contato.cia.dev@gmail.com"


def enviar_email_notificacao(conteudo):
    """Função que dispara o e-mail para você"""
    mensagem = MIMEMultipart()
    mensagem['From'] = EMAIL_QUE_ENVIA
    mensagem['To'] = EMAIL_QUE_RECEBE
    mensagem['Subject'] = "🚀 Novo Orçamento Recebido - Ultra Dev"

    mensagem.attach(MIMEText(conteudo, 'plain'))

    try:
        # Conectando ao servidor do Gmail (SMTP)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Camada de segurança
        server.login(EMAIL_QUE_ENVIA, SENHA_DE_APP)
        server.sendmail(EMAIL_QUE_ENVIA, EMAIL_QUE_RECEBE, mensagem.as_string())
        server.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


@app.route('/salvar_orcamento', methods=['POST'])
def salvar_orcamento():
    dados = request.json
    email_cliente = dados.get('email')
    descricao = dados.get('descricao')

    bloco_texto = (
        "_________________________________\n"
        f"NOVA SOLICITAÇÃO\n"
        f"E-mail do Cliente: {email_cliente}\n"
        f"Descrição do Projeto: {descricao}\n"
        "_________________________________\n"
    )

    # 1. Continua salvando no arquivo TXT local (como backup)
    with open("solicitacoes.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(bloco_texto + "\n")

    # 2. NOVA PARTE: Envia o e-mail para você em tempo real
    enviar_email_notificacao(bloco_texto)

    return jsonify({"status": "sucesso"})


if __name__ == '__main__':
    app.run(debug=True)