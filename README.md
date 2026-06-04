📊 Russell Top 200 — Data Extraction & Processing
Pipeline automatizado para extrair, limpar e consolidar dados do índice Russell (Top 200 / 3000) usando Python, iShares e Yahoo Finance.
Inclui workflows GitHub Actions, scripts de scraping, geração de CSVs e preparação de datasets para análise financeira.

📌 Índice
Visão Geral

Funcionalidades

Arquitetura do Projeto

Fluxo de Dados

Instalação

Como Usar

Workflows GitHub Actions

Estrutura de Arquivos

Contribuições

Licença

🚀 Visão Geral
Este repositório automatiza a criação de datasets do Russell Top 200 e Russell 3000, combinando:

Extração de holdings iShares

Coleta de dados no Yahoo Finance

Construção de CSVs prontos para análise

Automação via GitHub Actions

Ideal para análises quantitativas, backtesting, machine learning financeiro e pipelines de dados.

🧩 Funcionalidades
Extração automática de holdings do Russell via iShares

Download de preços e métricas via Yahoo Finance

Limpeza e normalização dos dados brutos

Geração de input.csv com tickers atualizados

Criação de russell3000_yahoo.csv

Workflows automatizados para atualização contínua

🏗️ Arquitetura do Projeto
O pipeline segue esta lógica:

extract_ishares.py  
Extrai holdings do Russell diretamente do site da iShares.

build_input_csv.py  
Constrói o input.csv com tickers limpos e validados.

russell3000_top200.py  
Faz scraping + coleta de dados financeiros via Yahoo Finance.

GitHub Actions  
Automatiza todo o processo em cada push ou agendamento.

🔄 Fluxo de Dados
Código
iShares → ishares_holdings_fixed.csv
                ↓
        build_input_csv.py → input.csv
                ↓
    russell3000_top200.py → russell3000_yahoo.csv
⚙️ Instalação
bash
git clone <URL_DO_REPOSITORIO>
cd Russell_top200

pip install -r requirements.txt
Dependências principais:

pandas

yfinance

▶️ Como Usar
1. Extrair holdings da iShares
bash
python extract_ishares.py
2. Gerar input.csv
bash
python build_input_csv.py
3. Coletar dados do Yahoo Finance
bash
python russell3000_top200.py
4. Resultado final
Arquivo gerado:

Código
russell3000_yahoo.csv
Com colunas como:

Ticker

Nome

Setor

Market Cap

P/E

Beta

Preço atual

Etc.

⚡ Workflows GitHub Actions
Local: .github/workflows/

O workflow atual:

Faz checkout da versão correta

Executa scripts de extração

Atualiza CSVs automaticamente

Permite automação diária/semanal

Para ver detalhes:
Ver workflow

📁 Estrutura de Arquivos
Código
.github/workflows/
    └── workflow.yml

build_input_csv.py
extract_ishares.py
russell3000_top200.py

input.csv
ishares_holdings_fixed.csv
russell3000_yahoo.csv

requirements.txt
README.md
🤝 Contribuições
Pull requests são bem‑vindos.
Sugestões de melhorias, novas fontes de dados ou otimizações são encorajadas.

📄 Licença
Este projeto não possui licença explícita.
Recomenda-se adicionar uma licença (MIT, Apache 2.0, etc.).
