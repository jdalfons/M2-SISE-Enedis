import dash
import dash_bootstrap_components as dbc

# Constants for paths
PREDICTION_PATH = "/prediction"
MAP_PATH = "/map"
CONTEXTE_PATH = "/contexte"
ANALYTIQUES_PATH = "/analytiques"
HOME_PATH = "/"
DATA = "./data/data_output.csv"

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet"
    }, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"]

app = dash.Dash(
    __name__,
    title = "GreenTech Solutions",
    external_stylesheets=[
        external_stylesheets,
        dbc.themes.BOOTSTRAP,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'  
    ]
)
app.config.suppress_callback_exceptions = True
server = app.server



fields = ['Etiquette_DPE',
    'Type_bâtiment',
    'Coût_chauffage',
    'Année_construction',
    'Surface_habitable_immeuble',
    'Emission_GES_5_usages',
    'Coût_chauffage_dépensier',
    'Conso_5_usages_é_finale',
    'Adresse_brute',
    'Code_postal_(BAN)',
    'Identifiant__BAN',
    'Date_réception_DPE',
    'Adresse_(BAN)',
    'Qualité_isolation_enveloppe',
    'Surface_habitable_logement',
    'Coût_auxiliaires',
    'Type_installation_chauffage_n°1',
    'Type_installation_chauffage',
    'Conso_5_usages/m²_é_finale',
    'Coût_refroidissement',
    'Type_énergie_n°1',
    'Coût_ECS',
    'Coût_total_5_usages',
    'Coût_éclairage',
    'Isolation_toiture_(0/1)'
    'Classe_inertie_bâtiment',
    'Hauteur_sous-plafond',
    'Type_énergie_principale_chauffage',
    'Code_INSEE_(BAN)'
    'Conso_chauffage_dépensier_é_finale',
    'Volume_stockage_générateur_ECS_n°1',
    'Conso_ECS_é_finale_énergie_n°3',
    'Conso_é_finale_installation_ECS',
    'Nom__commune_(BAN)',
    'Emission_GES_chauffage',
    'Conso_ECS_é_finale_énergie_n°2',
    'Conso_ECS_é_finale_énergie_n°1',
    'Besoin_refroidissement',
    'Conso_chauffage_dépensier_installation_chauffage_n°1',
    'Configuration_installation_chauffage_n°1',
    'Conso_é_finale_dépensier_installation_ECS',
    'Configuration_installation_ECS',
    'Surface_chauffée_installation_chauffage_n°1',
    'Coordonnée_cartographique_X_(BAN)',
    'Nombre_niveau_logement',
    'Apports_internes_saison_froid',
    'Type_installation_ECS_(général)',
    'Déperditions_murs',
    'Conso_5_usages_par_m²_é_primaire',
    'Ubat_W/m²_K',
    'Usage_générateur_ECS_n°1',
    'Coût_ECS_dépensier',
    'Emission_GES_auxiliaires',
    'Emission_GES_5_usages_par_m²',
    'Emission_GES_éclairage',
    'Apports_solaires_saison_froid',
    'Conso_ECS_dépensier_é_finale',
    'Date_visite_diagnostiqueur',
    'N°_étage_appartement',
    'Type_énergie_générateur_ECS_n°1',
    'Présence_production_PV_(0/1)',
    "Complément_d'adresse_logement",
    'Coût_total_5_usages_énergie_n°3',
    'Date_établissement_DPE',
    'Coût_total_5_usages_énergie_n°2',
    'Type_générateur_ECS_n°1',
    'Coût_total_5_usages_énergie_n°1',
    'Description_installation_chauffage_n°1',
    'Besoin_ECS',
    'N°DPE',
    'Conso_refroidissement_é_finale',
    'Conso_chauffage_é_primaire',
    'Emission_GES_5_usages_énergie_n°3',
    'Conso_éclairage_é_primaire',
    'Qualité_isolation_menuiseries',
    'Qualité_isolation_murs',
    'Emission_GES_5_usages_énergie_n°1',
    'Type_émetteur_installation_chauffage_n°1',
    'Emission_GES_5_usages_énergie_n°2',
    'Statut_géocodage',
    'Emission_GES_ECS_énergie_n°3',
    'Emission_GES_ECS_énergie_n°2',
    'Emission_GES_ECS_énergie_n°1',
    'Nombre_appartement',
    'Modèle_DPE',
    'Description_générateur_chauffage_n°1_installation_n°1',
    'Description_générateur_ECS_n°1',
    'Production_électricité_PV_(kWhep/an)',
    'N°_département_(BAN)',
    'Conso_refroidissement_é_primaire',
    'Méthode_application_DPE',
    'N°_région_(BAN)',
    'Code_postal_(brut)',
    'Deperditions_planchers_bas',
    'Coordonnée_cartographique_Y_(BAN)',
    '_rand',
    'Période_construction',
    'Emission_GES_ECS_dépensier',
    'Emission_GES_chauffage_énergie_n°2',
    'Emission_GES_chauffage_énergie_n°1',
    'Emission_GES_chauffage_énergie_n°3',
    'Conso_é_finale_dépensier_générateur_ECS_n°1',
    'Emission_GES_refroidissement',
    'Classe_altitude',
    'Description_installation_ECS',
    'Type_énergie_n°3',
    'Emission_GES_ECS',
    'Type_énergie_n°1',
    'Type_énergie_n°2',
    'Coût_ECS_énergie_n°2',
    'Coût_ECS_énergie_n°3',
    'Coût_ECS_énergie_n°1',
    'Qualité_isolation_plancher_haut_comble_perdu',
    'Conso_éclairage_é_finale',
    'Coût_refroidissement_dépensier',
    'Date_fin_validité_DPE',
    'Deperditions_planchers_hauts',
    'Emission_GES_refroidissement_dépensier',
    'Apports_solaires_saison_chauffe',
    'Conso_chauffage_générateur_n°1_installation_n°1',
    'Déperditions_renouvellement_air',
    'Déperditions_portes',
    '_geopoint',
    'Conso_chauffage_installation_chauffage_n°1',
    'Conso_ECS_dépensier_é_primaire',
    'Zone_climatique_',
    'Conso_refroidissement_dépensier_é_finale',
    'Usage_générateur_n°1_installation_n°1',
    'Version_DPE',
    'Electricité_PV_autoconsommée',
    'Deperditions_baies_vitrées',
    'Conso_chauffage_dépensier_générateur_n°1_installation_n°1',
    'Type_énergie_générateur_n°1_installation_n°1',
    'Déperditions_ponts_thermiques',
    'Système_production_électricité_origine_renouvelable',
    'Emission_GES_chauffage_dépensier',
    'Conso_ECS_é_primaire',
    'Etiquette_GES',
    'Conso_5_usages_é_finale_énergie_n°1',
    'Conso_5_usages_é_finale_énergie_n°2',
    'Conso_5_usages_é_finale_énergie_n°3',
    'Conso_auxiliaires_é_primaire',
    'Conso_auxiliaires_é_finale',
    'Conso_é_finale_générateur_ECS_n°1',
    'Conso_chauffage_é_finale',
    'Conso_refroidissement_dépensier_é_primaire',
    'Besoin_refroidissement_dépensier',
    'Type_générateur_n°1_installation_n°1',
    'Coût_chauffage_énergie_n°1',
    '_i',
    'Coût_chauffage_énergie_n°2',
    'Qualité_isolation_plancher_bas',
    'Apports_internes_saison_chauffe_',
    'Nom__rue_(BAN)',
    'Coût_chauffage_énergie_n°3',
    'Conso_chauffage_dépensier_é_primaire',
    'Score_BAN',
    'Deperditions_enveloppe',
    'Type_énergie_principale_ECS',
    'Conso_5_usages_é_primaire',
    'Conso_chauffage_é_finale_énergie_n°3',
    'Conso_chauffage_é_finale_énergie_n°2',
    'Conso_chauffage_é_finale_énergie_n°1',
    '_score',
    '_id',
    'N°_voie_(BAN)',
    'Qualité_isolation_plancher_haut_toit_terrase',
    'Catégorie_ENR',
    'N°_DPE_remplacé',
    'Date_installation_générateur_ECS_n°1',
    'Position_logement_dans_immeuble',
    'Type_générateur_froid',
    'Surface_ventilée',
    'Nombre_niveau_immeuble',
    'Surface_tertiaire_immeuble',
    'Ventilation_postérieure_2012_(0/1)',
    'Typologie_logement',
    'Type_ventilation',
    'Type_installation_solaire',
    'Surface_climatisée',
    'Production_ecs_solaire_installation',
    'Conso_refroidissement_dépensier_annuel',
    'Conso_refroidissement_annuel',
    'Inertie_lourde_(0/1)',
    'Conso_chauffage_générateur_n°2_installation_n°1',
    'Conso_chauffage_dépensier_générateur_n°2_installation_n°1',
    'Description_générateur_chauffage_n°2_installation_n°1',
    'Type_générateur_n°2_installation_n°1',
    'Facteur_couverture_solaire_installation_chauffage_n°1',
    'Usage_générateur_n°2_installation_n°1',
    'Type_énergie_générateur_n°2_installation_n°1',
    'Conso_chauffage_dépensier_installation_chauffage_n°2',
    'Configuration_installation_chauffage_n°2',
    'Surface_chauffée_installation_chauffage_n°2',
    'Description_installation_chauffage_n°2',
    'Type_émetteur_installation_chauffage_n°2',
    'Description_générateur_chauffage_n°1_installation_n°2',
    'Conso_chauffage_générateur_n°1_installation_n°2',
    'Conso_chauffage_installation_chauffage_n°2',
    'Usage_générateur_n°1_installation_n°2',
    'Type_énergie_générateur_n°1_installation_n°2',
    'Conso_chauffage_dépensier_générateur_n°1_installation_n°2',
    'Type_générateur_n°1_installation_n°2',
    'Type_énergie_climatisation',
    'N°_immatriculation_copropriété',
    'Nom_résidence',
    'Appartement_non_visité_(0/1)',
    'Surface_totale_capteurs_photovoltaïque',
    'Nombre_module',
    'Facteur_couverture_solaire',
    'N°_DPE_immeuble_associé',
    'Facteur_couverture_solaire_saisi',
    'COP_générateur_ECS_n°1',
    'Invariant_fiscal_logement',
    'Facteur_couverture_solaire_saisi_installation_chauffage_n°1',
    'Conso_chauffage_générateur_n°2_installation_n°2',
    'Conso_chauffage_dépensier_générateur_n°2_installation_n°2',
    'Description_générateur_chauffage_n°2_installation_n°2',
    'Type_générateur_n°2_installation_n°2',
    'Usage_générateur_n°2_installation_n°2',
    'Type_énergie_générateur_n°2_installation_n°2',
    "Cage_d'escalier",
    'Facteur_couverture_solaire_installation_chauffage_n°2',
    'N°_RPLS_logement']