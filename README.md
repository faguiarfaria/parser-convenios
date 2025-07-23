# 🦷 Parser de Relatórios de Convênios Odontológicos

Este projeto tem como objetivo extrair e estruturar automaticamente os dados de faturamento contidos nos relatórios em PDF fornecidos por convênios odontológicos, como a **Unimed Odonto**.

---

## 📌 Funcionalidades

- Conversão de relatórios PDF em tabelas estruturadas.
- Extração de cada procedimento odontológico por linha.
- Geração de arquivos `.xlsx` organizados, prontos para análise.
- Suporte inicial ao modelo da **Unimed Odonto** (competência: Junho/2025).

---

## 🛠️ Estrutura do Projeto

```
parser-convenios/
├── extratores/
│   └── parser_unimed_comentado.py       # Script com parser da Unimed, comentado
│   └── parser_redeunna_comentado.py     # Script com parser da Rede Unna, comentado
├── notebooks/
│   └── parser_unimed_colab_xls.ipynb    # Notebook para execução no Google Colab
│   └── parser_redeunna_colab_xls.ipynb  # Notebook para execução no Google Colab
├── requirements.txt                     # Dependências do projeto
├── README.md                            # Este arquivo
```

---

## ▶️ Como rodar no Google Colab

1. Para Unimed Odonto, acesse o notebook no Colab:  
   👉 [Abrir Parser UnimedOdonto no Colab](https://colab.research.google.com/github/faguiarfaria/parser-convenios/blob/main/notebooks/parser_unimed_colab_xls.ipynb)

2. No menu superior, clique em `Arquivo > Salvar uma cópia no Drive` (opcional).

3. Execute primeiro a célula [1] para instalar as dependências (autorize e execute):
   ```python
   !pip install pdfplumber openpyxl pandas
   ```

4. Faça o upload do relatório PDF da Unimed Odonto ao executar a célula [2] (ex: `Relatorio_Unimed_2025_06.pdf`).
   ```python
   from google.colab import files
   uploaded = files.upload()
   ```

5. Execute as próximas células normalmente.

6. O notebook irá gerar e exibir um botão para download do arquivo `procedimentos_unimed.xlsx`.

Para Rede Unna, pelo Colab: 
   👉 [Abrir Parser RedeUnna no Colab](https://colab.research.google.com/github/faguiarfaria/parser-convenios/blob/main/notebooks/parser_redeunna_colab_xls.ipynb)


---

## 📄 Formato de Saída

Cada linha do Excel gerado representa um procedimento odontológico, com as seguintes colunas (os dados estarão em formato texto):

1. Data do atendimento  
2. Código do paciente  
3. Nome do paciente  
4. Descrição do procedimento  
5. Detalhe (DT/área anatômica)  
6. Face  
7. Número da GTO  
8. Status (realizado, glosado etc.)  
9. Valor do procedimento (R$)  
10. Valor glosado (R$)  
11. Valor final após glosa (R$)

---

## 🚧 Próximos passos

- Suporte a novos modelos de convênios (Amil, Rede Unna, etc.)
- Interface para seleção do convênio no início da execução
- Upload automático para planilhas online (ex: Google Sheets)

---

## 📋 Requisitos

Se desejar rodar localmente, instale os pacotes com:

```bash
pip install -r requirements.txt
```

---

## 👨‍💻 Autor

Fernando Faria  
🔗 [GitHub: @faguiarfaria](https://github.com/faguiarfaria)
