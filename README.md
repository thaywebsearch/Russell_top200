# 📊 Russell 3000 Analysis Dashboard

Bem-vindo ao projeto de monitorização automatizada das empresas que compõem o índice **Russell 3000**. Este repositório utiliza **GitHub Actions** para extrair e processar dados em tempo real, focando-se nos dois extremos do mercado americano: as 200 maiores e as 200 menores empresas por capitalização de mercado.

---

## 🚀 Navegação Rápida

Escolha uma das listas abaixo para visualizar os dados detalhados:

| Relatório | Descrição | Formato |
| :--- | :--- | :--- |
| [🔝 **As 200 Maiores Empresas**](./russell3000_yahoo.csv) | As gigantes do mercado (Top 200 por Market Cap) | [CSV] |
| [📉 **As 200 Menores Empresas**](./Russell%203000%20-%20As%20200%20Menores%20Empresas.md) | As micro-caps do índice (Bottom 200) | [Markdown] / [CSV](./russell3000-bottom-200.csv) |

---

## 🛠️ Como Funciona a Automação

Este projeto é 100% automatizado através de workflows que executam semanalmente:

1.  **Extração**: Os dados são obtidos diretamente dos ETFs da iShares (**IWL** para as maiores e **IWV** para o índice completo).
2.  **Processamento**: Utilizamos a biblioteca `yfinance` para obter dados fundamentais (Market Cap, Setor, Indústria e Preço) em tempo real.
3.  **Atualização**: O GitHub Actions gera novos relatórios e atualiza este repositório automaticamente todas as segundas-feiras às 08:00 UTC.

---

## 📂 Estrutura do Repositório

*   `extract_ishares.py`: Script de extração das holdings.
*   `russell3000_top200.py`: Processamento via Yahoo Finance.
*   `russell3000_yahoo.csv`: O resultado final das maiores empresas.
*   `russell3000-bottom-200.csv`: O resultado final das menores empresas.

---

## 📈 Visualização no GitHub Pages

Este repositório está configurado para ser visualizado como um site. Pode aceder à versão web aqui:
👉 [**Visualizar Dashboard Online**](https://thaywebsearch.github.io/Russell_top200/)

---
*Mantido por [Gilberto (thaywebsearch)](https://github.com/thaywebsearch)*
