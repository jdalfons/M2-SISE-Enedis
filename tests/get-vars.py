import json

# Load the notebook content
with open('Chap1.ipynb', 'r', encoding='utf-8') as f:
    notebook_content = json.load(f)

# Provided list of variable names
variable_list = [
    "Cage_d'escalier", 'Nom__commune_(BAN)', 'Description_générateur_ECS_n°1', 
    'Type_énergie_générateur_n°1_installation_n°1', 'Nombre_appartement', 
    'Emission_GES_5_usages_énergie_n°2', 'N°DPE_remplacé', 'Conso_auxiliaires_é_finale', 
    'Etiquette_DPE', 'Modèle_DPE', 'Déperditions_ponts_thermiques', 'Coût_chauffage_énergie_n°2', 
    'Hauteur_sous-plafond', 'Type_installation_ECS(général)', 'Type_générateur_n°2_installation_n°2', 
    'Coût_ECS_énergie_n°1', 'Type_installation_ECS', 'Conso_5_usages_é_primaire', 
    'Type_installation_chauffage_n°2', 'Conso_ECS_é_finale', 'Type_bâtiment', 'Coût_chauffage', 
    'Système_production_électricité_origine_renouvelable', 'Coût_refroidissement_dépensier', 
    'Conso_chauffage_dépensier_générateur_n°2_installation_n°2', 'Version_DPE', 
    'Conso_refroidissement_annuel', 'Conso_ECS_dépensier_é_primaire', 'Inertie_lourde_(0/1)', 
    'Année_construction', 'Nom_résidence', 'Production_ecs_solaire_installation', 
    'Conso_refroidissement_dépensier_é_primaire', 'N°DPE_immeuble_associé', 'Date_établissement_DPE', 
    'Type_générateur_ECS_n°2', 'Surface_chauffée_installation_chauffage_n°2', 
    'Surface_habitable_immeuble', 'Position_logement_dans_immeuble', 'N°voie(BAN)', 
    'Surface_climatisée', 'Typologie_logement', 'Emission_GES_refroidissement', 
    'Volume_stockage_générateur_ECS_n°1', 'Conso_chauffage_installation_chauffage_n°1', 
    'Etiquette_GES', 'Type_générateur_n°1_installation_n°2', 'Emission_GES_éclairage', 
    'COP_générateur_ECS_n°2', 'Code_postal(brut)', 'Usage_générateur_n°1_installation_n°1', 
    'Emission_GES_5_usages', 'Usage_générateur_ECS_n°1', 'Usage_générateur_ECS_n°2', 
    'Emission_GES_5_usages_énergie_n°3', 'Conso_chauffage_générateur_n°2_installation_n°1', 
    'Nom__rue_(BAN)', 'Méthode_application_DPE', 'Isolation_toiture_(0/1)', 
    'Appartement_non_visité_(0/1)', 'Qualité_isolation_murs', 'Qualité_isolation_plancher_haut_comble_aménagé', 
    'Score_BAN', 'Surface_habitable_desservie_par_installation_ECS', 'Conso_ECS_é_primaire', 
    'COP_générateur_ECS_n°1', 'Nombre_niveau_immeuble', 'Logement_traversant_(0/1)', 
    'Configuration_installation_chauffage_n°1', 'Statut_géocodage', 'Conso_é_finale_installation_ECS', 
    'Coût_chauffage_dépensier', 'Coordonnée_cartographique_Y_(BAN)', 'Deperditions_planchers_bas', 
    'Description_installation_chauffage_n°2', 'Besoin_ECS', 'Besoin_chauffage', 'Conso_5_usages_é_finale', 
    'Description_installation_chauffage_n°1', 'Surface_chauffée_installation_chauffage_n°1', 
    'Besoin_refroidissement', "Complément_d'adresse_logement", 'Nombre_niveau_logement', 
    'Emission_GES_auxiliaires', 'Adresse_brute', 'Type_émetteur_installation_chauffage_n°1', 
    'Code_postal_(BAN)', 'Conso_éclairage_é_finale', 'Conso_auxiliaires_é_primaire', 'Type_énergie_n°3', 
    'Surface_tertiaire_immeuble', 'Classe_inertie_bâtiment', 'Type_générateur_ECS_n°1', 
    'Emission_GES_chauffage_dépensier', 'Coordonnée_cartographique_X_(BAN)', 
    'Protection_solaire_exterieure_(0/1)', 'Indicateur_confort_été', 'Conso_ECS_dépensier_é_finale', 
    'Usage_générateur_n°2_installation_n°1', 'N°immatriculation_copropriété', 'Présence_brasseur_air(0/1)', 
    'Type_générateur_n°1_installation_n°1', 'Identifiant__BAN', 'Configuration_installation_ECS', 
    'Electricité_PV_autoconsommée', 'Classe_altitude', 'Présence_production_PV_(0/1)', 
    'Conso_chauffage_dépensier_générateur_n°1_installation_n°1', 'Description_installation_ECS', 
    'Type_énergie_générateur_n°1_installation_n°2', 'Deperditions_enveloppe', 
    'Ventilation_postérieure_2012_(0/1)', 'Type_énergie_générateur_ECS_n°1', 'Ubat_W/m²_K', 
    'Type_énergie_générateur_ECS_n°2', 'N°région(BAN)', 'Qualité_isolation_menuiseries', 
    'Conso_refroidissement_é_finale', 'Emission_GES_5_usages_énergie_n°1', 
    'Conso_chauffage_générateur_n°2_installation_n°2', 'Volume_stockage_générateur_ECS_n°2', 
    'Date_réception_DPE', 'N°département(BAN)', 'Type_générateur_n°2_installation_n°1', 'Type_générateur_froid', 
    'Coût_ECS_énergie_n°2', 'Surface_ventilée', 'Emission_GES_ECS_dépensier', 
    'Conso_5_usages_é_finale_énergie_n°1', 'Configuration_installation_chauffage_n°2', 'Adresse_(BAN)', 
    'N°étage_appartement', 'Coût_chauffage_énergie_n°1', 'Qualité_isolation_enveloppe', 
    'Usage_générateur_n°2_installation_n°2', 'Catégorie_ENR', 'Usage_générateur_n°1_installation_n°2', 
    'Emission_GES_refroidissement_dépensier', 'Déperditions_renouvellement_air', 
    'Conso_refroidissement_dépensier_é_finale', 'Description_générateur_ECS_n°2', 
    'Conso_é_finale_générateur_ECS_n°1', 'Surface_habitable_logement', 'Conso_éclairage_é_primaire', 
    'Type_énergie_n°2', 'Date_visite_diagnostiqueur', 'Coût_auxiliaires', 'Type_installation_chauffage_n°1', 
    'Conso_5_usages_par_m²_é_primaire', 'Conso_refroidissement_é_primaire', 
    'Surface_totale_capteurs_photovoltaïque', 'Code_INSEE(BAN)', 'Nombre_module', 'N°DPE', 
    'Emission_GES_ECS', 'Coût_chauffage_énergie_n°3', 'Zone_climatique_', 'Type_installation_solaire', 
    'Conso_chauffage_dépensier_é_finale', 'Conso_chauffage_é_finale', 'Emission_GES_chauffage', 
    'Type_installation_chauffage', 'Conso_chauffage_dépensier_é_primaire', 'logement', 
    'Conso_5_usages/m²_é_finale', 'Coût_refroidissement', 'Emission_GES_5_usages_par_m²', 
    'Qualité_isolation_plancher_bas', 'Conso_chauffage_dépensier_générateur_n°2_installation_n°1', 
    'Conso_chauffage_générateur_n°1_installation_n°1', 'Type_énergie_générateur_n°2_installation_n°2', 
    'Coût_ECS_dépensier', 'Deperditions_baies_vitrées', 'Date_fin_validité_DPE', 'Deperditions_planchers_hauts', 
    'Type_ventilation', 'Conso_chauffage_dépensier_générateur_n°1_installation_n°2', 'Type_énergie_n°1', 
    'N°_RPLS_logement', 'Type_énergie_principale_chauffage', "Complément_d'adresse_bâtiment", 'Coût_ECS', 
    'Déperditions_murs', 'Coût_total_5_usages', 'Conso_chauffage_é_primaire', 
    'Nombre_logements_desservis_par_installation_ECS', 'Conso_chauffage_installation_chauffage_n°2', 
    'Invariant_fiscal_logement', 'Coût_éclairage', 'Coût_ECS_énergie_n°3', 
    'Type_émetteur_installation_chauffage_n°2', 'Conso_chauffage_générateur_n°1_installation_n°2', 
    'Type_énergie_générateur_n°2_installation_n°1', 'Conso_é_finale_générateur_ECS_n°2', 
    'Type_énergie_principale_ECS', 'Déperditions_portes'
]

# Extract code cells
code_cells = [cell['source'] for cell in notebook_content['cells'] if cell['cell_type'] == 'code']

# Flatten the list of code cells
code_content = "\n".join(["".join(cell) for cell in code_cells])

# Find used variables
used_variables = [var for var in variable_list if var in code_content]

print(used_variables)