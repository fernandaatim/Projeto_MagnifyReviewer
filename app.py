import os
import logging
from flask import Flask, redirect, render_template, request, jsonify, url_for
from flask_mail import Mail, Message
from forms import ContactUsForm
import main

app = Flask(__name__, template_folder='templates')
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_USERNAME'] = 'magnifyreviewer@outlook.com'
app.config['MAIL_PASSWORD'] = 'Erosadonis2@'
app.config['SECRET_KEY'] = 'magnify'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'magnifyreviewer@outlook.com'
uploads = 'uploads'
app.config['uploads'] = uploads

mail = Mail(app)

@app.route("/", methods=["GET", "POST"])
def index():
    form = ContactUsForm()
    if form.validate_on_submit():
        name = form.name.data
        site = form.site.data
        email = form.email.data
        message = form.message.data
        try:
            msg = Message("Contact Form Submission", sender=app.config['MAIL_DEFAULT_SENDER'], recipients=["Fernanda.Berwald@br.bosch.com","eros.benkert@br.bosch.com"])
            msg.body = f"Nome: {name}\nSite: {site}\nEmail: {email}\nMensagem: {message}"
            mail.send(msg)
            return redirect(url_for('index'))
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            return render_template('index.html', form=form)
    return render_template('index.html', form=form)

@app.route("/processar_emails", methods=["POST"])
def processar_emails():
    try:
        if 'arquivo' not in request.files:
            logging.debug('Nenhum arquivo enviado!')
            return jsonify({'mensagem': 'Nenhum arquivo enviado!'})

        file = request.files['arquivo']
        logging.debug(f'Arquivo enviado: {file.filename}')
        
        if file.filename == '':
            logging.debug('Nenhum arquivo selecionado!')
            return jsonify({'mensagem': 'Nenhum arquivo selecionado!'})

        if not file.filename.endswith('.txt'):
            logging.debug('Arquivo inválido! Deve ser .txt')
            return jsonify({'mensagem': 'Arquivo inválido! Por favor, envie um arquivo .txt'})

        file_path = os.path.join(app.config['uploads'], 'emails.txt')
        file.save(file_path)
        logging.debug(f'Arquivo salvo em {file_path}')

        tamanho_arquivo = os.path.getsize(file_path)
        if tamanho_arquivo == 0:
            logging.debug('Arquivo vazio!')
            return jsonify({'mensagem': 'Arquivo vazio!'})

        resultados = main.processar_emails(file_path)
        main.salvar_resultados(os.path.join(app.config['uploads'], 'resultados.csv'), resultados)
        
        return jsonify({'mensagem': 'Avaliação finalizada! O arquivo foi salvo e processado com sucesso!'})

    except Exception as e:
        logging.error(f"Erro: {e}")
        return jsonify({'mensagem': 'Erro ao processar arquivo!'})

@app.route('/resultados', methods=['POST'])
def enviar_resultados():
    arquivo_resultados = 'uploads/resultados.csv'
    with open(arquivo_resultados, 'r') as csvfile:
        csv_data = csvfile.read()
    return csv_data


if __name__ == '__main__':
    app.run(debug=True)