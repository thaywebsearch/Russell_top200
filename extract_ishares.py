import re
import pandas as pd
import requests
import sys

def download_and_extract(portfolio_id, output_csv):
    url = f"https://www.blackrock.com/varnish-api/blk-one01-product-data/product-data/api/v1/get-fund-document?appType=PRODUCT_PAGE&appSubType=ISHARES&targetSite=us-ishares&locale=en_US&portfolioId={portfolio_id}&component=fundDownload&userType=individual"
    
    print(f"A descarregar dados da iShares (Portfolio ID: {portfolio_id})...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        content = response.text

        # Dividir o conteúdo por linhas <ss:Row>
        rows_raw = re.findall(r'<ss:Row.*?>(.*?)</ss:Row>', content, re.DOTALL)
        
        data = []
        headers_list = []
        
        for row_str in rows_raw:
            # Extrair dados de cada célula <ss:Cell>
            cells = re.findall(r'<ss:Cell.*?>(.*?)</ss:Cell>', row_str, re.DOTALL)
            row_data = []
            for cell_str in cells:
                # Pegar o valor dentro de <ss:Data>
                match = re.search(r'<ss:Data.*?>(.*?)</ss:Data>', cell_str, re.DOTALL)
                if match:
                    row_data.append(match.group(1))
                else:
                    row_data.append("")
            
            # Identificar cabeçalho
            if "Ticker" in row_data and not headers_list:
                headers_list = row_data
                continue
                
            if headers_list and row_data:
                # Alinhar com o cabeçalho
                if len(row_data) >= len(headers_list):
                    data.append(row_data[:len(headers_list)])

        if headers_list and data:
            df = pd.DataFrame(data, columns=headers_list)
            # Limpeza básica: remover linhas sem ticker ou inválidas
            df = df[df['Ticker'].apply(lambda x: len(str(x)) > 0 and str(x) != "Accrual Date")]
            df.to_csv(output_csv, index=False)
            print(f"Sucesso! {len(df)} holdings extraídas para {output_csv}")
            return True
        else:
            print("Erro: Não foi possível encontrar a tabela de holdings no ficheiro.")
            return False
            
    except Exception as e:
        print(f"Ocorreu um erro durante a extração: {e}")
        return False

if __name__ == "__main__":
    # Portfolio ID para IWL (Russell Top 200) é 239721
    success = download_and_extract('239721', 'ishares_holdings_fixed.csv')
    if not success:
        sys.exit(1)
