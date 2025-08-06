# 🦷 parser-convenios

Ferramenta para extrair dados de relatórios PDF de convênios odontológicos, convertendo-os em planilhas Excel para análise e integração.

---

## 📁 Estrutura do Projeto

```
parser-convenios/
├── extratores/
│   └── parser_unimed.py       # Script com parser da Unimed, comentado
│   └── parser_redeunna.py     # Script com parser da Rede Unna, comentado
<<<<<<< HEAD
│   └── parser_metlife.py      # Script com parser da Metlife, comentado
│   └── parser_metlife_s.py    # Script com parser da Metlife Sintetico, comentado
├── notebooks/
│   └── parser_unimed_colab.ipynb       # Notebook para execução no Google Colab
│   └── parser_redeunna_colab.ipynb     # Notebook para execução no Google Colab
│   └── parser_metlife_colab.ipynb      # Notebook para execução no Google Colab
│   └── parser_metlife_s_colab.ipynb    # Notebook para execução no Google Colab
├── requirements.txt                     # Dependências do projeto
├── README.md                            # Este arquivo
└── LICENSE                              # Licença de uso MIT
```

---

## ▶️ Como rodar no Google Colab

### 1 - UNIMED ODONTO

#### 1.1. Acesse o notebook no Colab:
👉 [Abrir Parser UnimedOdonto no Colab](https://colab.research.google.com/github/faguiarfaria/parser-convenios/blob/main/notebooks/parser_unimed_colab.ipynb)

#### 1.2. Execute o Passo 1 no notebook para instalar as dependências:
```python
!pip install pdfplumber openpyxl pandas
```

#### 1.3. Faça o upload do relatório PDF da Unimed Odonto (ex: `Relatorio_Unimed_2025_06.pdf`) ao executar o Passo 2 e clicar em "Escolher arquivo":
```python
from google.colab import files
uploaded = files.upload()
```

#### 1.4. Siga as células do notebook até o final. Ele irá gerar e exibir um botão para download do arquivo `procedimentos_unimed.xlsx`.

> 💡 *Para customizar ou salvar sua própria versão, clique no menu `Arquivo > Salvar uma cópia no Drive` (necessita conta Google).*

---

### 2 - REDE UNNA

#### 2.1. Acesse o notebook no Colab:
👉 [Abrir Parser RedeUnna no Colab](https://colab.research.google.com/github/faguiarfaria/parser-convenios/blob/main/notebooks/parser_redeunna_colab.ipynb)

#### 2.2. Siga o mesmo passo a passo usado na Unimed Odonto para instalar pacotes, fazer upload e baixar a planilha gerada.

---

### 3 - METLIFE

#### 3.1. Acesse o notebook no Colab:
👉 [Abrir Parser METLIFE no Colab](https://colab.research.google.com/github/faguiarfaria/parser-convenios/blob/main/notebooks/parser_metlife_colab.ipynb)

#### 3.2. Siga o mesmo passo a passo dos anteriores.

#### Caso esteja usando o relatório sintético, use o Parser METLIFE Sintetico: 
👉 [Abrir Parser METLIFE Sintético no Colab](https://colab.research.google.com/github/faguiarfaria/parser-convenios/blob/main/notebooks/parser_metlife_s_colab.ipynb)

---

## 📋 Requisitos

Se desejar rodar localmente, instale as dependências com:

```bash
pip install -r requirements.txt
```


## 📄 Licença

Este projeto está licenciado sob os termos da [Licença MIT](./LICENSE).
