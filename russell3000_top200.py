import pandas as pd
import yfinance as yf
from datetime import date
import time
import sys

INPUT_FILE = "input.csv"
OUTPUT_FILE = "russell3000_yahoo.csv" # Nome consistente com o YAML original
MAX_ROWS = 200
AS_OF = date.today().isoformat()

def get_info_safe(ticker_obj):
    # Tentar obter info de várias formas, pois o yfinance é instável
    try:
        return ticker_obj.info
    except Exception:
        try:
            return ticker_obj.get_info()
        except Exception:
            return {}

def main():
    try:
        df_in = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Erro: Ficheiro {INPUT_FILE} não encontrado.")
        sys.exit(1)

    if "Ticker" not in df_in.columns:
        print("Erro: O input.csv precisa ter uma coluna chamada Ticker")
        sys.exit(1)

    rows = []
    print(f"A processar {len(df_in)} tickers via Yahoo Finance...")

    for i, row in df_in.iterrows():
        ticker = str(row["Ticker"]).strip()
        if not ticker or ticker.lower() == "nan":
            continue

        name = str(row["Empresa"]).strip() if "Empresa" in df_in.columns and pd.notna(row.get("Empresa")) else ""

        print(f"[{i+1}/{len(df_in)}] A obter dados para: {ticker}")
        
        try:
            t = yf.Ticker(ticker)
            info = get_info_safe(t)
            
            # Se info estiver vazio, tentamos pelo menos manter o nome original
            rows.append({
                "Ticker": ticker,
                "Empresa": info.get("shortName", info.get("longName", name)),
                "Setor": info.get("sector", "N/A"),
                "Indústria": info.get("industry", "N/A"),
                "País": info.get("country", "N/A"),
                "Market Cap": info.get("marketCap", None),
                "Preço": info.get("currentPrice", info.get("regularMarketPrice", None)),
                "Moeda": info.get("currency", "USD"),
                "Fonte": "Yahoo Finance",
                "Data": AS_OF,
            })
        except Exception as e:
            print(f"Aviso: Falha ao processar {ticker}: {e}")
            # Adicionar linha básica mesmo com erro para não perder o ativo
            rows.append({
                "Ticker": ticker,
                "Empresa": name,
                "Setor": "Erro",
                "Indústria": "Erro",
                "País": "N/A",
                "Market Cap": None,
                "Preço": None,
                "Moeda": "USD",
                "Fonte": "Yahoo Finance (Falha)",
                "Data": AS_OF,
            })
        
        # Pequena pausa para evitar bloqueios de taxa (rate limiting)
        if (i + 1) % 10 == 0:
            time.sleep(1)

        if len(rows) >= MAX_ROWS:
            break

    df = pd.DataFrame(rows)
    if df.empty:
        print("Erro: Nenhum dado foi gerado.")
        sys.exit(1)

    # Conversão e ordenação
    df["Market Cap"] = pd.to_numeric(df["Market Cap"], errors="coerce")
    df["Preço"] = pd.to_numeric(df["Preço"], errors="coerce")
    
    # Ordenar por Market Cap (ativos sem market cap ficam no fim)
    df = df.sort_values("Market Cap", ascending=False, na_position="last").head(MAX_ROWS).reset_index(drop=True)
    df.insert(0, "Rank", range(1, len(df) + 1))

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Sucesso! CSV gerado: {OUTPUT_FILE} com {len(df)} linhas.")

if __name__ == "__main__":
    main()
