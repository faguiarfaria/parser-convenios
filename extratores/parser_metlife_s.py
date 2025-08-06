
import pdfplumber  # Biblioteca para ler e extrair texto de arquivos PDF
import pandas as pd  # Biblioteca para manipulação de dados em tabelas (DataFrames)
import re  # Biblioteca para trabalhar com expressões regulares (padrões de texto)
import sys  # Biblioteca para ler argumentos passados via linha de comando

# Função principal que extrai os dados do PDF - Demonstrativo Sintético Metlife
def extrair_dados_metlife_s(pdf_path):
    resultados = []  # Lista onde vamos armazenar os dados extraídos
    repasses = []  # Lista onde vamos armazenar os dados de repasse

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

    # Primeiro loop: extrai todos os repasses (cada PRESTADOR: pode trazer um novo repasse)
    i = 0  
    while i < len(linhas):
        if linhas[i].strip().startswith("PRESTADOR:"): 
            repasse_match = re.search(r"REPASSE:\s*(\d{7})", linhas[i].strip())
            num_repasse = repasse_match.group(1) if repasse_match else ""
        
            # se encontrou um numero de repasse, armazena 1 por linha
            if num_repasse:
                repasses.append({"Repasses": num_repasse}) 
        # Avança sempre uma linha após cada iteração
        i += 1

    # Segundo loop: extrai as GTOs e seus dados
    i = 0  # reseta índice
    while i < len(linhas):
        # Início de uma nova GTO é identificado por esta string
        if linhas[i].strip().startswith("GTO:"): 

            gto_match = re.search(r"GTO:\s*(\d{9})", linhas[i].strip())
            gto = gto_match.group(1) if gto_match else ""

           # Verifica se há pelo menos 1 linha seguinte disponível (para pegar dados do paciente)
            if i + 1 < len(linhas):
                # A linha abaixo da "GTO" → código do paciente + nome
                linha_paciente = linhas[i + 1].strip()
                #cod do paciente tem 14 dígitos, e fica logo após o texto CÓDIGO/NOME BENEFICIÁRIO:
                paciente_match = re.search(r"CÓDIGO/NOME BENEFICIÁRIO:\s*(\d{14})", linha_paciente)
                cod_paciente = paciente_match.group(1) if paciente_match else ""

                # Nome do paciente logo após o código de 14 dígitos
                nome_social = ""
                if cod_paciente:
                    tokens = linha_paciente.split()
                    try:
                        idx_ini = tokens.index("-") + 1     # Início do nome (logo após o hífem)
                        idx_fim = tokens.index("TITULAR:")     # Fim do nome (antes de "TITULAR:")
                        nome_tokens = tokens[idx_ini:idx_fim]
                        nome_social = " ".join(nome_tokens)
                    except ValueError:
                        pass

        # Captura o texto da glosa (justificativa)
        glosa = ""  # Metlife não apresenta glosa nos seus demonstrativos

        # Procura os valores financeiros da GTO
        valor_info = valor_glosa = valor_pago = 0.0
        situação_gto = "P"  

        if linhas[i].strip().startswith("TOTAL DA GTO"): 
            linha_valores = linhas[i].strip()

            # valores da GTO logo após TOTAL DA GTO
            if linha_valores:
                tokens = linha_valores.split()
                try:
                    valor_glosa = to_float(tokens[3])
                    valor_pago = to_float(tokens[4])
                    valor_info = valor_glosa + valor_pago
                    if valor_glosa > 0:
                        situação_gto = "GL"
                except ValueError:
                    pass


        # Adiciona os dados extraídos ao resultado
        if valor_info > 0:
            resultados.append({
                "Data": "",
                "Mariana": "",
                "Repetida?": "",
                "GTO": gto,
                "Plano": "MetLife",
                "Situação": situação_gto,
                "Cod Glosa": "",
                "Detalhes": glosa,
                "Valor GTO": valor_info,
                "Valor Glosa": valor_glosa,
                "Valor Final": valor_pago,
                "Localidade": "",
                "Acesso": "",
                "Paciente": nome_social,
                "ID": cod_paciente,
                "Procedimento": "",
                "Index": "Metlife." + gto,

            })

        # Avança sempre uma linha após cada iteração
        i += 1

    # DataFrame dos repasses:
    df_repasse = pd.DataFrame(repasses)

    # DataFrame principal das GTOs
    df_gto = pd.DataFrame(resultados)  # resultados = lista de dicts com as GTOs

    # Escreve ambos os DataFrames em um único arquivo Excel, um abaixo do outro
    saida = "procedimentos_metlife_sintetico.xlsx"
    with pd.ExcelWriter(saida, engine='openpyxl') as writer:
        # Repasse primeiro
        df_repasse.to_excel(writer, index=False)
        # GTOs logo depois (pula 2 linhas após os repasses)
        df_gto.to_excel(writer, index=False, startrow=len(df_repasse) + 2)
    print(f"Arquivo exportado com sucesso: {saida}")        


# Executa o script apenas se for rodado diretamente (não importado como módulo)
if __name__ == "__main__":

    # Caminho usado nos testes
    # pdf_path = "/home/fernando/Downloads/metlife 2025-08-05 sintetico 9.pdf"

    # Caminho do PDF pode ser passado como argumento ou definido aqui
    if len(sys.argv) != 2:
        print("Uso: python parser_metlife.py caminho_para_pdf")
        sys.exit(1)
    pdf_path = sys.argv[1]

    # Executa a extração dos dados
    extrair_dados_metlife_s(pdf_path)
