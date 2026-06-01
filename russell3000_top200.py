import yfinance as yf
import pandas as pd
from datetime import date

INDEX_SYMBOL = "^RUA"
MAX_ROWS = 200
AS_OF = date.today().isoformat()
OUTPUT_FILE = "russell3000_top200_yahoo.csv"

def get_info_safe(ticker_obj):
    try:
        return ticker_obj.get_info()
    except Exception:
        try:
            return ticker_obj.info
        except Exception:
            return {}

def get_components():
    index_ticker = yf.Ticker(INDEX_SYMBOL)
    raw = get_info_safe(index_ticker)

    for key in ("components", "constituents", "holdings"):
        if isinstance(raw, dict) and raw.get(key):
            return raw[key]

    raise RuntimeError(
        "Não foi possível obter os componentes do ^RUA via Yahoo Finance. "
        "Use uma lista externa de constituintes e mantenha este script para enriquecimento."
    )

def normalize_component(item):
    if isinstance(item, dict):
        ticker = item.get("symbol") or item.get("ticker") or item.get("ric") or ""
        name = item.get("name") or item.get("longName") or item.get("shortName") or ""
    else:
        ticker = str(item)
        name = ""
    return ticker, name

def main():
    components = get_components()
    rows = []

    for item in components:
        ticker, name = normalize_component(item)
        if not ticker:
            continue

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
        raise RuntimeError("Nenhum dado foi coletado.")

    df["Market Cap"] = pd.to_numeric(df["Market Cap"], errors="coerce")
    df["Preço"] = pd.to_numeric(df["Preço"], errors="coerce")
    df = df.sort_values("Market Cap", ascending=False, na_position="last").head(MAX_ROWS).reset_index(drop=True)
    df.insert(0, "Rank", range(1, len(df) + 1))

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"CSV gerado: {OUTPUT_FILE}")
    print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
