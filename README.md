# 🦷 Parser de Relatórios de Convênios Odontológicos

Este projeto tem como objetivo extrair e estruturar automaticamente os dados de faturamento contidos nos relatórios em PDF fornecidos por convênios odontológicos, cconvertendo-os em planilhas Excel para análise e integração.

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
└── LICENSE                              # Linceça de uso MIT

---

## ▶️ Como rodar no Google Colab

1 - UNIMED ODONTO

   1.1. Para Unimed Odonto, acesse o notebook no Colab:  
      👉 [Abrir Parser UnimedOdonto no Colab](https://colab.research.google.com/github/faguiarfaria/parser-convenios/blob/main/notebooks/parser_unimed_colab_xls.ipynb)

   1.2. Execute Passo 1 para instalar as dependências (autorize e execute):
      ```python
      !pip install pdfplumber openpyxl pandas
      ```

   1.3. Faça o upload do relatório PDF da Unimed Odonto (ex: `Relatorio_Unimed_2025_06.pdf`) ao executar o Passo 2 e clicar no botão que será gerado de "escolher arquivo" (choose file).
      ```python
      from google.colab import files
      uploaded = files.upload()
      ```

   1.4. Siga o passo a passo até a última célula, notebook irá gerar e exibir um botão para download do arquivo `procedimentos_unimed.xlsx`.

   IMPORTANTE: Caso queira customizar/alterar o código, no menu superior clique em `Arquivo > Salvar uma cópia no Drive` (opcional, e necessita de uma conta no google drive).

2 - REDE UNNA

   2.1. Para Rede Unna, pelo Colab: 
      👉 [Abrir Parser RedeUnna no Colab](https://colab.research.google.com/github/faguiarfaria/parser-convenios/blob/main/notebooks/parser_redeunna_colab_xls.ipynb)

   2.2. Siga o passo a passo como da unimed odonto.


---

## 🚧 Próximos passos

- Suporte a novos modelos de convênios (PASA, MetLife, etc.)
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
