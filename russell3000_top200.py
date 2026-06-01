import pandas as pd
import yfinance as yf
from datetime import date

INPUT_FILE = "input.csv"
OUTPUT_FILE = "russell3000_top200_yahoo.csv"
MAX_ROWS = 200
AS_OF = date.today().isoformat()

def get_info_safe(ticker_obj):
    try:
        return ticker_obj.get_info()
    except Exception:
        try:
            return ticker_obj.info
        except Exception:
            return {}

def main():
    df_in = pd.read_csv(INPUT_FILE)

    if "Ticker" not in df_in.columns:
        raise ValueError("O input.csv precisa ter uma coluna chamada Ticker")

    rows = []

    for _, row in df_in.iterrows():
        ticker = str(row["Ticker"]).strip()
        if not ticker or ticker.lower() == "nan":
            continue

        name = str(row["Empresa"]).strip() if "Empresa" in df_in.columns and pd.notna(row.get("Empresa")) else ""

        t = yf.Ticker(ticker)
        info = get_info_safe(t)

        rows.append({
            "Ticker": ticker,
            "Empresa": name or info.get("shortName", "") or info.get("longName", ""),
            "Setor": info.get("sector", ""),
            "Indústria": info.get("industry", ""),
            "País": info.get("country", ""),
            "Market Cap": info.get("marketCap", None),
            "Preço": info.get("currentPrice", info.get("regularMarketPrice", None)),
            "Moeda": info.get("currency", ""),
            "Fonte": "Yahoo Finance",
            "Data": AS_OF,
        })

        if len(rows) >= MAX_ROWS:
            break

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("Nenhum dado foi gerado.")

    df["Market Cap"] = pd.to_numeric(df["Market Cap"], errors="coerce")
    df["Preço"] = pd.to_numeric(df["Preço"], errors="coerce")
    df = df.sort_values("Market Cap", ascending=False, na_position="last").head(MAX_ROWS).reset_index(drop=True)
    df.insert(0, "Rank", range(1, len(df) + 1))

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"CSV gerado: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
