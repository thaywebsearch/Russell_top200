# Russell Top 200 Data Pipeline

Pipeline automatizado para extrair, limpar e consolidar dados do índice Russell Top 200 usando Python, iShares e Yahoo Finance.

## Objetivo

O projeto gera um dataset com os 200 constituintes do Russell Top 200 e enriquece cada linha com dados de mercado como setor, indústria, país, preço e market cap.

## Como funciona

1. `build_input_csv.py` lê `ishares_holdings_fixed.csv`.
2. O script cria `input.csv` com os 200 tickers do universo selecionado.
3. `russell3000_top200.py` lê `input.csv`.
4. O script consulta Yahoo Finance via `yfinance`.
5. O resultado final é gravado em `russell3000_yahoo.csv`.
6. O GitHub Actions faz upload do CSV final como artifact.

## Ficheiros principais

- `ishares_holdings_fixed.csv`: holdings base extraídas do iShares.
- `build_input_csv.py`: gera o `input.csv`.
- `input.csv`: lista de tickers e nomes.
- `russell3000_top200.py`: enriquece os dados com Yahoo Finance.
- `requirements.txt`: dependências Python.
- `.github/workflows/run.yml`: workflow automatizado.
- `russell3000_yahoo.csv`: output final do pipeline.

## Dependências

Instale com:

```bash
pip install -r requirements.txt
```

## Execução local

```bash
python build_input_csv.py
python russell3000_top200.py
```

## GitHub Actions

O workflow `run.yml` executa automaticamente os passos acima e publica `russell3000_yahoo.csv` como artifact.

## Uso do CSV final

Depois de descarregar `russell3000_yahoo.csv`, pode importá-lo para Google Sheets para análise, filtragem e consolidação.

## Notas

- O projeto usa `yfinance` para obter dados públicos do Yahoo Finance.
- O CSV final pode ser atualizado manualmente ou por schedule no GitHub Actions.
- O artifact é temporário e fica associado ao workflow run.
