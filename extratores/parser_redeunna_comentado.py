
import pdfplumber  # Biblioteca para ler e extrair texto de arquivos PDF
import pandas as pd  # Biblioteca para manipulação de dados em tabelas (DataFrames)
import re  # Biblioteca para trabalhar com expressões regulares (padrões de texto)
import sys  # Biblioteca para ler argumentos passados via linha de comando

# Caminho do arquivo PDF com os dados do convênio Rede Unna
pdf_path = "Relatorio de convenio - modelos - redeunna - 2025_07.pdf"

# Função principal que extrai os dados do PDF
def extrair_dados_unimed_corrigido(pdf_path):
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
            return float(valor.strip())  # Usa ponto como separador decimal (formato americano)
        except:
            return 0.0

    i = 0  # Índice da linha atual
    while i < len(linhas):
        # Início de uma nova GTO é identificado por esta string
        if linhas[i].strip().startswith("Dados do Pagamento"):

            # Verifica se há pelo menos duas linhas seguintes disponíveis
            if i + 2 < len(linhas):
                cabecalho = linhas[i + 1]  # Não usado no código, mas mantido como possível referência
                valores = linhas[i + 2]  # Contém informações principais: GTO, código do paciente, nome e data
                val_split = valores.split()  # Divide a linha em palavras (tokens)

                # Busca dois números longos consecutivos: GTO e código do paciente
                num_grandes_idx = [idx for idx, val in enumerate(val_split) if re.fullmatch(r"\d{8,12}", val)]
                gto = val_split[num_grandes_idx[0]] if len(num_grandes_idx) > 0 else ""
                cod_carteira = val_split[num_grandes_idx[1]] if len(num_grandes_idx) > 1 else ""

                # Extrai nome social (logo após o código do paciente)
                nome_social = ""
                if len(num_grandes_idx) > 1:
                    idx_nome_inicio = num_grandes_idx[1] + 1
                    nome_tokens = []
                    token_max = 10  # limite de palavras para evitar erros
                    for idz, token in enumerate(val_split[idx_nome_inicio:]):
                        if token.isupper() and not re.fullmatch(r"\d{8,12}", token):
                            if nome_tokens and token == nome_tokens[0]:
                                break  # Evita repetição duplicada do nome
                            nome_tokens.append(token)
                            if idz + 1 >= token_max:
                                break
                        else:
                            break
                    nome_social = " ".join(nome_tokens)

                # Captura a data de pagamento logo após a string "Dt. Pagto."
                try:
                    dt_pgto_idx = val_split.index("Dt.") if "Dt." in val_split else val_split.index("Dt. Pagto.")
                    data_pgto = val_split[dt_pgto_idx + 2] if val_split[dt_pgto_idx + 1] == "Pagto." else val_split[dt_pgto_idx + 1]
                except ValueError:
                    data_pgto = ""

            # Se o bloco não tiver as duas linhas seguintes, ignora
            else:
                continue

            # Captura o texto da glosa (justificativa)
            glosa = ""
            for j in range(i, min(i + 20, len(linhas))):
                if linhas[j].strip().startswith("27 - Observação / Justificativa"):
                    if j + 1 < len(linhas):
                        glosa_texto = linhas[j + 1].strip()
                        if glosa_texto.startswith("Total de Pontos:"):
                            glosa = ""  # Ignora glosas irrelevantes
                            break
                        glosa = glosa_texto
                    break  # Finaliza a leitura da glosa

            # Procura os valores financeiros da GTO
            valor_info = valor_glosa = valor_pago = ""
            for j in range(i + 1, min(i + 15, len(linhas))):
                if "28 - Valor Total Informado Guia" in linhas[j]:
                    if j + 1 < len(linhas):
                        tot_valores = linhas[j + 1].strip().split()
                        if len(tot_valores) >= 5:
                            valor_info = tot_valores[0]
                            valor_glosa = tot_valores[2]
                            valor_pago = tot_valores[4]
                    break

            # Adiciona os dados extraídos ao resultado
            resultados.append({
                "Data": data_pgto,
                "Convênio": "Rede Unna",
                "GTO": gto,
                "Código do Paciente": cod_carteira,
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
        print("Uso: python parser_redeunna.py caminho_para_pdf")
        sys.exit(1)

    # Recebe o caminho do PDF via linha de comando
    pdf_path = sys.argv[1]

    # Executa a extração dos dados
    df = extrair_dados_unimed_corrigido(pdf_path)

    # Exporta os dados para uma planilha Excel
    saida = "procedimentos_redeunna.xlsx"
    df.to_excel(saida, index=False, engine='openpyxl')

    print(f"Arquivo exportado com sucesso: {saida}")
