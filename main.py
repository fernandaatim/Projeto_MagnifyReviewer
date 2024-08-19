import csv
import openai
import os
import logging
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Obter a chave da API do ambiente
api_key = os.environ.get("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("A chave da API do OpenAI não foi encontrada nas variáveis de ambiente.")
openai.api_key = api_key

def lidar_com_erros(e):
    logging.error(f"Erro: {e}")
    return f"Erro: {e}"

def extrair_conteudo_email(bloco):
    if '===START EMAIL===' in bloco:
        return bloco.split('===START EMAIL===\n', 1)[-1].strip()
    return None

def processar_email(email_text):
    try:
        resultado = avaliar_email(email_text)
        return resultado
    except Exception as e:
        return lidar_com_erros(e)

def avaliar_email(email_text):
    # print(f"Analisando o e-mail: {email_text}\n")
    
    linguagem = "Inglês, EUA"

    criterios = (
        "Gramática: 1 ponto por erro encontrado em uma palavra ou expressão. \n"
        "Falta de saudação: 1 ponto por erro encontrado devido à falta de uma saudação apropriada. \n"
        "Confusão de espaçamento inicial, médio ou final: 1 ponto por erro encontrado relacionado a espaçamento confuso ou incorreto ou ausente.\n"
        "Final ausente: 1 ponto por erro encontrado relacionado à falta de uma finalização apropriada ou uso inadequado de finalizações.\n"
        "Pontuação inicial: 100 por e-mail.\n"
        "Siga o padrão formal empresarial.\n"
    )
    
    exemplo_email_certo=(
        "\nHello,\n\n"

        "Your order has been shipped."

        "\n\nSupport Team"
        
        "\n\nAnálise: Aqui está com tudo separado corretamente, além de uma finalização e saudação aceitável. Siga como exemplo de certo!"
        )
    
    exemplo_email_errado = (
    "\nHi there\n\n"

    "Your order was dispatched yesterday. If you need anything else, just let us know.\n"

    "\nCheers,"
    "\nAlex"
    "\n\nAnálise: Possui falta de saudação, pois 'Hi there' é incorreto e inapropriado, Erro gramatical pela informalidade em 'just let us know' e ausência de finalização por ter usado 'Cheers'. Soma-se 1 ponto pra cada critério, exceto o de espaçamento confuso.")

    regras = (
        f"Veja um exemplo incorreto: {exemplo_email_errado}"
        f"Veja um exemplo correto: {exemplo_email_certo}"
        "Palavras informais devem ser consideradas como erros gramaticais e somar pontos.\n"
        "O uso de palavras em uma língua diferente da estabelecida deve contar como erro gramatical.\n"
        "Letras aleatórias ou palavras sem sentido devem ser consideradas como erros gramaticais.\n"
        "Todo erro gramatical que se encaixe nas categorias citadas podem também ser contabilizado como um erro de saudação ou finalização, dependendo de sua posição no texto, mas não pode em hipotese alguma receber mais de 1 erro por gramática.\n"
        "O uso inadequado de letras maiúsculas ou minúsculas deve ser considerado como erro gramatical, exceto se forem letras aleatórias sem sentido algum.\n"
        "Não considere uma frase errada se todas as regras gramaticais estão sendo respeitadas!\n"
        "Assinatura após agradecimento não pode contabilizar como um erro de finalização ausente, mesmo que a assinatura seja o nome da pessoa. Inclusive, não tem problema a assinatura não estar 100 por cento formal!\n"
        "Falta de agradecimento é erro de ausencia de finalização!\n"
    )

    padrao_lista = (
        "Gramática: Apenas o número total de erros gramaticais encontrados, incluindo erros múltiplos por palavra e uso inadequado de maiúsculas.\n"
        "Falta de saudação: Apenas o número total de erros devido à falta de saudação apropriada.\n"
        "Confusão de espaçamento: Apenas o número total de erros devido à confusão de espaçamento.\n"
        "Final ausente: Apenas o número total de erros devido à falta de finalização apropriada.\n"
    )

    mensagens = [
        {"role": "system", "content": (
            f"Você é um assistente de correção de e-mails empresariais. Para cada e-mail encontrado, você deve considerar os seguintes critérios:\n{criterios}\n\n"
            f"O conteúdo deve ser avaliado no idioma: {linguagem}.\n"
        )},
        
        {"role": "system", "content": f"Siga também essas regras adicionais: {regras}. Aqui está o conteúdo do e-mail: {email_text}"},
        {"role": "user", "content": (f"Liste exatamente neste formato:\n{padrao_lista}\n.")},
        {"role": "user", "content": (f"Explique no final como chegou a cada resultado, listando seus erros.")},
    ]

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            messages=mensagens,
        )

        escolhas = resposta.get('choices', [])
        if escolhas:
            primeira_escolha = escolhas[0]
            mensagem = primeira_escolha.get('message', {})
            conteudo = mensagem.get('content', '').strip()

            conteudo = '\n'.join(linha.strip() for linha in conteudo.split('\n'))
            return conteudo
        else:
            return "Resposta inválida: Nenhuma escolha encontrada."
    except Exception as e:
        logging.error(f"Erro ao processar a resposta: {e}", exc_info=True)
        return f"Erro ao processar a resposta: {e}"
    
def formatar_resultados(resultados):
    formatado = []

    for i, resultado in enumerate(resultados):
        linhas = resultado.split('\n')
        resultado_formatado = f"E-mail {i+1}\n"

        critérios = {
            "Gramática": 0,
            "Falta de saudação": 0,
            "Confusão de espaçamento": 0,
            "Final ausente": 0,
            "Pontuação Final": 100
        }

        for linha in linhas:
            linha = linha.strip()
            if ":" in linha:
                chave, valor = linha.split(":", 1)
                chave = chave.strip()
                valor = valor.strip()
                if chave in critérios:
                    try:
                        critérios[chave] = int(valor)
                    except ValueError:
                        critérios[chave] = 0
            else:
                print(f"Ignorando linha inválida: {linha}")

        penalidades = {
            "Gramática": critérios["Gramática"] * 2,
            "Falta de saudação": critérios["Falta de saudação"] * 1,
            "Confusão de espaçamento": critérios["Confusão de espaçamento"] * 1,
            "Final ausente": critérios["Final ausente"] * 1
        }

        pontuacao_final = critérios["Pontuação Final"]
        for penalidade in penalidades.values():
            pontuacao_final -= penalidade

        pontuacao_final = max(pontuacao_final, 0)
        print(f"Pontuação Final do E-mail {i+1}: {pontuacao_final}")

        del critérios["Pontuação Final"]

        resultado_formatado += "\n".join(
            f"{chave}: {valor}" for chave, valor in critérios.items()
        )
        resultado_formatado += f"\nPontuação Final: {pontuacao_final}\n"

        formatado.append(resultado_formatado)

    return "\n".join(formatado)

def salvar_resultados(arquivo_resultados, resultados):
    with open(arquivo_resultados, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        header = ['E-mail', 'Gramática', 'Falta de saudação', 'Confusão de espaçamento', 'Final ausente', 'Pontuação Final']
        writer.writerow(header)
        for i, resultado in enumerate(resultados):
            linhas = resultado.split('\n')
            email_data = [f'{i+1}']  # Adiciona o identificador do e-mail
            critérios = {
                "Gramática": 0,
                "Falta de saudação": 0,
                "Confusão de espaçamento": 0,
                "Final ausente": 0,
                "Pontuação Final": 100
            }
            for linha in linhas:
                linha = linha.strip()
                if ":" in linha:
                    chave, valor = linha.split(":", 1)
                    chave = chave.strip()
                    valor = valor.strip()
                    if chave in critérios:
                        try:
                            critérios[chave] = int(valor)
                        except ValueError:
                            critérios[chave] = 0
            penalidades = {
                "Gramática": critérios["Gramática"] * 2,
                "Falta de saudação": critérios["Falta de saudação"] * 1,
                "Confusão de espaçamento": critérios["Confusão de espaçamento"] * 1,
                "Final ausente": critérios["Final ausente"] * 1
            }
            pontuacao_final = critérios["Pontuação Final"]
            for penalidade in penalidades.values():
                pontuacao_final -= penalidade
            pontuacao_final = max(pontuacao_final, 0)
            email_data.extend([critérios["Gramática"], critérios["Falta de saudação"], critérios["Confusão de espaçamento"], critérios["Final ausente"], pontuacao_final])
            writer.writerow(email_data)
    
def processar_emails(arquivo_emails):
    resultados = []
    try:
        with open(arquivo_emails, 'r', encoding='utf-8') as file:
            conteudo = file.read()
            blocos_emails = conteudo.split('===END EMAIL===\n')
            for bloco in blocos_emails:
                email_text = extrair_conteudo_email(bloco)
                if email_text:
                    resultado = processar_email(email_text)
                    resultados.append(resultado)
    except Exception as e:
        logging.error(f"Erro ao processar o arquivo de e-mails: {e}")
    return resultados

def main():
    arquivo_emails = 'emails.txt'
    resultados = processar_emails(arquivo_emails)
    resultados_formatados = formatar_resultados(resultados)
    salvar_resultados(arquivo_resultados, resultados_formatados)
    
    upload = 'upload'
    os.makedirs(upload)
    
    arquivo_resultados = os.path.join(upload, 'resultados.csv')