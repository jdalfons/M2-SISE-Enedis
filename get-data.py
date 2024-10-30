import pandas as pd
import requests
import gc

# URL de base de l'API
url = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"
full_content = list()

addresses_df = pd.read_csv('data/adresses-69.csv', sep=';')
codes_postaux = addresses_df['code_postal'].unique().tolist()

fields = ['Date_réception_DPE',
          'Etiquette_DPE',
          'Coût_chauffage',
          'Surface_habitable_logement',
          'Adresse_(BAN)',
          'Code_postal_(BAN)',
          'Identifiant__BAN',]

annees = [2021, 2022, 2023, 2024]
etiquettes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

for code_postal in codes_postaux:
    param = {
        "page": 1,
        "size": 10000,
        "select": ','.join(fields),
        "q": code_postal,
        "q_fields": "Code_postal_(BAN)"
    }
    result = requests.get(url, params=param)
    if result.status_code == 200:
        content = result.json()
        if content['total'] <= 10000:
            full_content.extend(content['results'])
        else:
            for annee in annees:
                param_ = {
                    "page": 1,
                    "size": 10000,
                    "select": ','.join(fields),
                    "q": code_postal,
                    "q_fields": "Code_postal_(BAN)",
                    "qs": f"Date_réception_DPE:[{annee}-01-01 TO {annee}-12-31]"
                }
                content_ = requests.get(url, params=param_)
                if content_.status_code == 200:
                    content_json = content_.json()
                    if content_json['total'] <= 10000:
                        full_content.extend(content_json['results'])
                    else:
                        for etiquette in etiquettes:
                            param_ = {
                                "page": 1,
                                "size": 10000,
                                "q": code_postal,
                                "select": ','.join(fields),
                                "q_fields": "Code_postal_(BAN)",
                                "qs": f"Date_réception_DPE:[{annee}-01-01 TO {annee}-12-31] AND Etiquette_DPE:{etiquette}"
                            }
                            content_ = requests.get(url, params=param_)
                            if content_.status_code == 200:
                                content_json = content_.json()
                                if content_json['total'] <= 10000:
                                    full_content.extend(content_json['results'])
                                else:
                                    print("error")
                else:
                    print(f"error in {code_postal}, {annee}")
    else:
        print("error")

# Convert to DataFrame and save to CSV
df = pd.DataFrame(full_content)[fields]

df.to_csv('data/data_output.csv', mode='a', header=False, index=False)

print(f"Nombre total de lignes dans full_content : {len(full_content)}")

# Reset garbage collector
gc.collect()
