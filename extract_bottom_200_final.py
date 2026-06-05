import re
import pandas as pd
import requests
import sys

def download_and_extract_bottom(portfolio_id, output_csv):
    # IWV (Russell 3000) portfolio ID is 239714
    url = f"https://www.blackrock.com/varnish-api/blk-one01-product-data/product-data/api/v1/get-fund-document?appType=PRODUCT_PAGE&appSubType=ISHARES&targetSite=us-ishares&locale=en_US&portfolioId={portfolio_id}&component=fundDownload&userType=individual"
    
    print(f"A descarregar dados do Russell 3000 para as menores empresas...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        content = response.text

        rows_raw = re.findall(r'<ss:Row.*?>(.*?)</ss:Row>', content, re.DOTALL)
        
        data = []
        headers_list = []
        
        for row_str in rows_raw:
            cells = re.findall(r'<ss:Cell.*?>(.*?)</ss:Cell>', row_str, re.DOTALL)
            row_data = []
            for cell_str in cells:
                match = re.search(r'<ss:Data.*?>(.*?)</ss:Data>', cell_str, re.DOTALL)
                if match:
                    row_data.append(match.group(1))
                else:
                    row_data.append("")
            
            if "Ticker" in row_data and not headers_list:
                headers_list = row_data
                continue
                
            if headers_list and row_data:
                if len(row_data) >= len(headers_list):
                    data.append(row_data[:len(headers_list)])

        if headers_list and data:
            df = pd.DataFrame(data, columns=headers_list)
            df = df[df['Asset Class'] == 'Equity'].copy()
            df['Weight (%)'] = pd.to_numeric(df['Weight (%)'], errors='coerce')
            df = df[df['Ticker'].apply(lambda x: len(str(x)) > 0 and str(x) != "Accrual Date")]
            
            # 200 menores por peso
            bottom_200 = df.sort_values('Weight (%)', ascending=True).head(200).reset_index(drop=True)
            bottom_200.insert(0, 'Rank', range(1, 201))
            
            bottom_200.to_csv(output_csv, index=False)
            print(f"Sucesso! {len(bottom_200)} empresas guardadas em {output_csv}")
            return True
        return False
    except Exception as e:
        print(f"Erro: {e}")
        return False

if __name__ == "__main__":
    success = download_and_extract_bottom('239714', 'russell3000_bottom200.csv')
    if not success:
        sys.exit(1)
