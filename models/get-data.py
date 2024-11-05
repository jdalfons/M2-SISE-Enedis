import pandas as pd
import requests
import gc
import os
from config import fields
import time

# Constants
URL = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"
OUTPUT_FILE = 'data/data_output.csv'
ADDRESS_FILE = './data/adresses-69.csv'
ANNEES = [2021, 2022, 2023, 2024]
ETIQUETTES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def load_postal_codes(address_file):
    """
    Load unique postal codes from the address file.

    Parameters:
    address_file (str): Path to the address file.

    Returns:
    list: List of unique postal codes.
    """
    addresses_df = pd.read_csv(address_file, sep=';')
    return addresses_df['code_postal'].unique().tolist()

def remove_output_file(output_file):
    """
    Remove the output file if it exists.

    Parameters:
    output_file (str): Path to the output file.
    """
    if os.path.exists(output_file):
        os.remove(output_file)

def fetch_data(params):
    """
    Fetch data from the API with given parameters.

    Parameters:
    params (dict): Parameters for the API request.

    Returns:
    dict: JSON response from the API or None if the request fails.
    """
    result = requests.get(URL, params=params)
    if result.status_code == 200:
        return result.json()
    else:
        print(f"Error fetching data with params: {params}")
        return None

def process_postal_code(code_postal):
    """
    Process data for a given postal code.

    Parameters:
    code_postal (str): Postal code to process.

    Returns:
    list: List of results for the postal code.
    """
    full_content = []
    params = {
        "page": 1,
        "size": 10000,
        "select": (",").join(fields),
        "q": code_postal,
        "q_fields": "Code_postal_(BAN)"
    }
    content = fetch_data(params)
    
    if content and content['total'] <= 10000:
        full_content.extend(content['results'])
    else:
        for annee in ANNEES:
            process_year(code_postal, annee, full_content)
    
    return full_content

def process_year(code_postal, annee, full_content):
    """
    Process data for a given postal code and year.

    Parameters:
    code_postal (str): Postal code to process.
    annee (int): Year to process.
    full_content (list): List to store the results.
    """
    params_annee = {
        "page": 1,
        "size": 10000,
        "q": code_postal,
        "select": (",").join(fields),
        "q_fields": "Code_postal_(BAN)",
        "qs": f"Date_réception_DPE:[{annee}-01-01 TO {annee}-12-31]"
    }
    content_annee = fetch_data(params_annee)
    
    if content_annee and content_annee['total'] <= 10000:
        full_content.extend(content_annee['results'])
    else:
        for etiquette in ETIQUETTES:
            process_label(code_postal, annee, etiquette, full_content)

def process_label(code_postal, annee, etiquette, full_content):
    """
    Process data for a given postal code, year, and label.

    Parameters:
    code_postal (str): Postal code to process.
    annee (int): Year to process.
    etiquette (str): Label to process.
    full_content (list): List to store the results.
    """
    params_etiquette = {
        "page": 1,
        "size": 10000,
        "q": code_postal,
        "select": (",").join(fields),
        "q_fields": "Code_postal_(BAN)",
        "qs": f"Date_réception_DPE:[{annee}-01-01 TO {annee}-12-31] AND Etiquette_DPE:{etiquette}"
    }
    content_etiquette = fetch_data(params_etiquette)
    
    if content_etiquette and content_etiquette['total'] <= 10000:
        full_content.extend(content_etiquette['results'])
    else:
        print(f"Error: Too many results for postal code: {code_postal}, year: {annee}, label: {etiquette}")

def save_data_to_csv(data, output_file, first_iteration):
    """
    Save data to a CSV file.

    Parameters:
    data (list): Data to save.
    output_file (str): Path to the output file.
    first_iteration (bool): Whether this is the first iteration (to include header).
    """
    df = pd.DataFrame(data)[fields]
    df.to_csv(output_file, mode='a', header=first_iteration, index=False)

def main():
    """
    Main function to orchestrate the data fetching and saving process.
    """
    codes_postaux = load_postal_codes(ADDRESS_FILE)
    remove_output_file(OUTPUT_FILE)
    
    first_iteration = True
    
    for code_postal in codes_postaux:
        print(f"Processing postal code: {code_postal}")
        full_content = process_postal_code(code_postal)
        print(f"Saving data for postal code: {code_postal}")
        save_data_to_csv(full_content, OUTPUT_FILE, first_iteration)
        first_iteration = False
        full_content.clear()  # Clear the list for the next iteration
    
    print(f"Nombre total de lignes dans full_content : {len(full_content)}")
    gc.collect()

if __name__ == "__main__":
    # main()
    start_time = time.time()
    print("Starting the full process...")
    # Existing main function call
    main()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time taken for the full process: {total_time:.2f} seconds")