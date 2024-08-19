import os
import logging
from flask import Flask, render_template, request, jsonify
import main

app = Flask(__name__)

uploads = 'uploads'
app.config['uploads'] = uploads

@app.route("/")
def index():
    return render_template("index.html")

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