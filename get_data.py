import pandas as pd
import requests
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Base URL of the API
BASE_URL = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"
YEARS = [2021, 2022, 2023, 2024]
ETIQUETS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def get_unique_postal_codes(file_path):
    """Read the CSV file and return a list of unique postal codes."""
    try:
        addresses_df = pd.read_csv(file_path, sep=';')
        return addresses_df['code_postal'].unique().tolist()
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        return []

def fetch_data(params):
    """Fetch data from the API with the given parameters."""
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def fetch_all_data(params):
    """Fetch all data handling pagination with a loading bar."""
    full_content = []
    total_records = 0
    file_path = 'data/adresses-69.csv'
    postal_codes = get_unique_postal_codes(file_path)
    
    if not postal_codes:
        logging.error("No postal codes found. Exiting.")
        return
    
    with tqdm(total=100, desc="Fetching data", unit="record") as pbar:
        while True:
            for postal_code in postal_codes:
                data = fetch_data(params)
                data['q'] = postal_code
                if not data:
                    break
                results = data.get('results', [])
                full_content.extend(results)
                total_records += len(results)
                pbar.update(len(results))
                next_url = data.get('next')
                if not next_url:
                    break
                params = None  # Clear params for subsequent requests
                BASE_URL = next_url
        pbar.total = total_records
        pbar.refresh()
    return full_content

def main():

    params = {
        "size": 10000,
        "select": "N°DPE,Code_postal_(BAN),Etiquette_DPE,Date_réception_DPE",
    }

    full_content = fetch_all_data(params)
    
    if full_content:
        logging.info(f"Fetched {len(full_content)} records.")
        df = pd.DataFrame(full_content)
        df.to_excel('dpe.xlsx', index=False)
        logging.info("Data saved to dpe.xlsx")
    else:
        logging.error("Failed to fetch data.")

if __name__ == "__main__":
    main()
