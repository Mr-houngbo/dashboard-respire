import os
from src.api_handler import (
    fetch_latest_data,
    append_new_data,
    save_data_to_csv,
    generate_daily_summary
)
from src.extract_vars import extract_ids_from_txt

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data/now')


# Configuration
token = "77a25676-a9ec-4a99-9137-f33e6776b590"

locations_list = extract_ids_from_txt("src/location_id.txt")

# location_id = "90104"   # Remplace par un ID valide

for i,location_id in enumerate(locations_list): 

    latest_measure = fetch_latest_data(location_id,token)
    save_data_to_csv(latest_measure,location_id)
    print(f"✅ Csv saved : {i} ")
    generate_daily_summary(location_id,f"{DATA_DIR}/{location_id}.csv")
    print(f"✅ daily summary generated : {i} ")
    


"""
# Étape 4 : Ajout de la dernière mesure dans le CSV
append_new_data(location_id, latest_measure)
print("✅ Dernière mesure ajoutée au fichier")
"""


