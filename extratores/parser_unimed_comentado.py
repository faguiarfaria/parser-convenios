import pdfplumber  # Biblioteca para ler e extrair texto de arquivos PDF
import pandas as pd  # Biblioteca para manipulação de dados em tabelas (DataFrames)
import re  # Biblioteca para trabalhar com expressões regulares (padrões de texto)
import sys  # Biblioteca para ler argumentos passados via linha de comando

# Função principal que extrai os dados do PDF
def extrair_dados_unimed_corrigido(pdf_path):
    dados = []  # Lista onde vamos armazenar os procedimentos extraídos

    # Variáveis auxiliares para guardar dados do paciente atual
    gto_atual = ""
    codigo_paciente = ""
    nome_paciente = ""

    # Abrimos o PDF usando o pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        # Percorremos cada página do PDF
        for page in pdf.pages:
            # Extraímos todo o texto da página e quebramos por linha
            linhas = page.extract_text().split('\n')
            for linha in linhas:
                # Verificamos se a linha contém uma nova GTO (com paciente)
                match_gto = re.match(r"GTO:(\d+)\s+CÓDIGO E NOME DO BENEFICIÁRIO:\s+(\d+)\s+-\s+(.+)", linha)
                if match_gto:
                    # Se encontrou, atualizamos os dados do paciente
                    gto_atual = match_gto.group(1).strip()
                    codigo_paciente = match_gto.group(2).strip()
                    nome_paciente = match_gto.group(3).strip()
                    continue  # Vamos para a próxima linha

                # Verificamos se a linha contém um procedimento
                match_proc = re.match(
                    r"(\d{8}) (.+?)\s+(\S+)\s+(Pago|Glosado|Deferido|Indeferido)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+(\d{2}/\d{2}/\d{4})",
                    linha
                )

                if match_proc:
                    # Se encontrou um procedimento, extraímos os campos
                    cod_proc = match_proc.group(1)
                    desc_proc = match_proc.group(2).strip()
                    detalhe_face = match_proc.group(3).strip()
                    status = match_proc.group(4)
                    valor_proc = match_proc.group(5).replace(",", ".")
                    valor_glosa = match_proc.group(6).replace(",", ".")
                    valor_final = match_proc.group(7).replace(",", ".")
                    data = match_proc.group(8)

                    # Separar 'Detalhe' e 'Face' (às vezes vêm juntos)
                    if detalhe_face.isdigit():
                        detalhe = detalhe_face
                        face = ""
                    elif detalhe_face.isalpha():
                        detalhe = ""
                        face = detalhe_face
                    else:
                        detalhe = detalhe_face[:-2]
                        face = detalhe_face[-2:]

                    # Adicionamos os dados extraídos à lista
                    dados.append({
                        "Data do atendimento": data,
                        "Código do paciente": codigo_paciente,
                        "Nome do paciente": nome_paciente,
                        "Descrição do procedimento": desc_proc,
                        "Detalhe": detalhe,
                        "Face": face,
                        "Número da GTO": gto_atual,
                        "Status do procedimento": status,
                        "Valor do procedimento (R$)": valor_proc,
                        "Valor glosado (R$)": valor_glosa,
                        "Valor final (R$)": valor_final
                    })

    # Transformamos a lista em um DataFrame (tabela)
    return pd.DataFrame(dados)

# Ponto de entrada do script
if __name__ == "__main__":
    # Verifica se o usuário passou o nome do PDF como argumento
    if len(sys.argv) != 2:
        print("Uso: python parser_unimed.py caminho_para_pdf")
        sys.exit(1)

    # Caminho do PDF fornecido na linha de comando
    pdf_path = sys.argv[1]

    # Executa a função e obtém o DataFrame com os dados extraídos
    df = extrair_dados_unimed_corrigido(pdf_path)

    # Exporta para Excel moderno (.xlsx) com engine openpyxl
    saida = "procedimentos_unimed.xlsx"
    df.to_excel(saida, index=False, engine='openpyxl')

    print(f"Arquivo exportado com sucesso: {saida}")
