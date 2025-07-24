
import pdfplumber  # Biblioteca para ler e extrair texto de arquivos PDF
import pandas as pd  # Biblioteca para manipulação de dados em tabelas (DataFrames)
import re  # Biblioteca para trabalhar com expressões regulares (padrões de texto)
import sys  # Biblioteca para ler argumentos passados via linha de comando

# Função principal que extrai os dados do PDF
def extrair_dados_metlife(pdf_path):
    resultados = []  # Lista onde vamos armazenar os dados extraídos

    # Junta o texto de todas as páginas do PDF em uma única string
    texto_completo = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()
            if texto:
                texto_completo += texto + "\n"

    # Divide o texto em linhas para análise linha a linha
    linhas = texto_completo.split('\n')

    # Função auxiliar que converte texto para número decimal (float)
    def to_float(valor):
        try:
            # Remove os pontos (separador de milhar) e troca a vírgula decimal por ponto
            return float(valor.replace('.', '').replace(',', '.').strip())
        except:
            return 0.0

    i = 0  # Índice da linha atual
    data_pgto = ""
   
    while i < len(linhas):

        # Captura a data de pagamento
        if linhas[i].strip() == "10 - Data do Pagamento 11 - Banco 12 - Agência 13 - Conta":

             # Verifica se há pelo menos 1 linhas seguinte disponível, pois data sempre está na linha abaixo
            if i + 1 < len(linhas):
                linha_data_pgto = linhas[i + 1].strip()
                data_pgto_match = re.search(r"\d{2}/\d{2}/\d{4}", linha_data_pgto)
                data_pgto = data_pgto_match.group(0) if data_pgto_match else data_pgto

        # Início de uma nova GTO é identificado por esta string
        if linhas[i].strip() == "Dados da Guia":

                # Verifica se há pelo menos 4 linhas seguintes disponíveis
                if i + 4 < len(linhas):
                    # Segunda linha abaixo da "Dados da Guia" → contém o código da GTO
                    linha_gto = linhas[i + 2].strip()
                    gto_match = re.match(r"\b\d{9}\b", linha_gto)
                    gto = gto_match.group(0) if gto_match else ""

                    # Quarta linha abaixo da "Dados da Guia" → código do paciente + nome
                    linha_paciente = linhas[i + 4].strip()
                    paciente_match = re.match(r"\b\d{14}\b", linha_paciente)
                    cod_paciente = paciente_match.group(0) if paciente_match else ""

                    # Nome do paciente logo após o código de 14 dígitos
                    nome_social = ""
                    if cod_paciente:
                        tokens = linha_paciente.split()
                        try:
                            idx = tokens.index(cod_paciente) + 1
                            while idx < len(tokens) and tokens[idx].isupper():
                                nome_social += tokens[idx] + " "
                                idx += 1
                            nome_social = nome_social.strip()
                        except ValueError:
                            pass

                    # Captura o texto da glosa (justificativa)
                    glosa = ""  # Metlife não apresenta glosa nos seus demonstrativos

                    # Procura os valores financeiros da GTO
                    valor_info = valor_glosa = valor_pago = ""
                    for j in range(i + 1, min(i + 30, len(linhas))):
                        if "Total da Guia" in linhas[j]:
                            if j + 2 < len(linhas):
                                tot_valores = linhas[j + 2].strip().split()
                                if len(tot_valores) >= 5:
                                    valor_info = tot_valores[0]
                                    valor_glosa = tot_valores[2]
                                    valor_pago = tot_valores[4]
                            break

                    # Adiciona os dados extraídos ao resultado
                    resultados.append({
                        "Data": data_pgto,
                        "Convênio": "MetLife",
                        "GTO": gto,
                        "Código do Paciente": cod_paciente,
                        "Nome Social do Paciente": nome_social,
                        "Glosas": glosa,
                        "Valor informado": to_float(valor_info),
                        "Valor glosado": to_float(valor_glosa),
                        "Valor pago": to_float(valor_pago)
                    })

        # Avança sempre uma linha após cada iteração
        i += 1

    # Converte os dados para um DataFrame do pandas
    return pd.DataFrame(resultados)


# Executa o script apenas se for rodado diretamente (não importado como módulo)
if __name__ == "__main__":
    # Verifica se o caminho do PDF foi passado como argumento
    if len(sys.argv) != 2:
        print("Uso: python parser_metlife.py caminho_para_pdf")
        sys.exit(1)

    # Recebe o caminho do PDF via linha de comando
    pdf_path = sys.argv[1]

    # Executa a extração dos dados
    df = extrair_dados_metlife(pdf_path)

    # Exporta os dados para uma planilha Excel
    saida = "procedimentos_metlife.xlsx"
    df.to_excel(saida, index=False, engine='openpyxl')

    print(f"Arquivo exportado com sucesso: {saida}")
