import pandas as pd
import requests
import time
import os
from tqdm import tqdm

# Base URL of the API
API_URL = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"
DATA_FILE = 'data/adresses-69.csv'
OUTPUT_FILE = 'dpe.xlsx'


def fetch_data_for_zip(zip_code):
    """
    Fetch data from the API for a given zip code.
    
    Parameters:
    zip_code (str): The postal code to query.
    
    Returns:
    list: A list of results from the API.
    """
    params = {
        "size": 10000,
        "q": zip_code,
        "q_fields": "Code_postal_(BAN)",
    }
    
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        content = response.json()
        print(f"Nombre total de lignes : {content['total']}")
        results = content.get('results', [])
        print(f"Dimensions des données récupérées : {len(results)}, {len(results[0]) if results else 0}")
        
        # Handle pagination
        next_url = content.get('next', None)
        while next_url:
            new_content = requests.get(next_url).json()
            results.extend(new_content.get('results', []))
            print(f"Nombre total de lignes dans full_content : {len(results)}")
            next_url = new_content.get('next', None)
        
        return results
    else:
        print(f"Erreur lors de la requête pour le code postal {zip_code}")
        return []


def main():
    """
    Main function to orchestrate the data fetching and saving process.
    """
    
    # Check if the output file exists, if not create it
    if not os.path.exists(OUTPUT_FILE):
        pd.DataFrame().to_excel(OUTPUT_FILE, index=False)

    addresses_df = pd.read_csv(DATA_FILE, sep=';')
    codes_postals = addresses_df['code_postal'].unique().tolist()
    start_time = time.time()
    
    
    for zip_code in tqdm(codes_postals, desc="Fetching data"):
        data = fetch_data_for_zip(zip_code)
        df = pd.DataFrame(data)
        
        # Append data to the Excel file
        with pd.ExcelWriter(OUTPUT_FILE, mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
        
        # Clear the memory
        del df

    elapsed_time = time.time() - start_time
    print(f"Data saved to {OUTPUT_FILE}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()