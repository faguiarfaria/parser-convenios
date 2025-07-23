# Faturamento Convênios - Unimed Odonto 🦷

Este projeto é um piloto para extração automatizada de relatórios de faturamento odontológico da Unimed Odonto, com base em arquivos PDF.

## 📌 Funcionalidades

- Leitura de relatórios Unimed Odonto em PDF
- Extração de cada procedimento realizado em formato tabular
- Exportação dos dados para planilhas `.xls`
- Suporte a execução via script Python ou Google Colab

## 📁 Estrutura do Projeto

```
faturamento-convenios-unimed/
├── extratores/
│   └── parser_unimed_comentado.py
├── notebooks/
│   └── parser_unimed_colab_xls.ipynb
├── requirements.txt
├── README.md
```

## ▶️ Como usar localmente

1. Instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

2. Execute o script passando o caminho do PDF como argumento:
```bash
python extratores/parser_unimed_comentado.py "Relatorio_Unimed_Junho2025.pdf"
```

3. Será gerado o arquivo `procedimentos_unimed.xls` com os dados extraídos.

## ☁️ Como usar no Google Colab

Abra o notebook `parser_unimed_colab_xls.ipynb` no Colab, envie o PDF e siga as instruções passo a passo.

## 🛠 Requisitos

- Python 3.7+
- pdfplumber
- pandas
- xlwt

## 📄 Licença

Projeto livre para uso e adaptação.
