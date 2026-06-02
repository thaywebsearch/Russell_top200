import pandas as pd

INPUT_FILE = "ishares_holdings_fixed.csv"
OUTPUT_FILE = "input.csv"
MAX_ROWS = 200

df = pd.read_csv(INPUT_FILE)

df = df[df["Asset Class"].eq("Equity")].copy()
df = df[df["Ticker"].notna() & df["Name"].notna()]
df = df[~df["Ticker"].isin(["USD", "XTSLA", "JPFFT", "ESM6", "ESU6", "ESZ6", "ESH6"])]
df["Weight (%)"] = pd.to_numeric(df["Weight (%)"], errors="coerce")

df = df.sort_values("Weight (%)", ascending=False, na_position="last").head(MAX_ROWS).reset_index(drop=True)

out = df[["Ticker", "Name"]].rename(columns={"Name": "Empresa"})
out["Ticker"] = out["Ticker"].astype(str).str.strip()
out["Empresa"] = out["Empresa"].astype(str).str.strip()

out.to_csv(OUTPUT_FILE, index=False)
print(f"Gerado: {OUTPUT_FILE} com {len(out)} linhas")
