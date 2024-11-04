BASE_URL = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"

columns = ['Type_générateur_n°1_installation_n°2',
 'Emission_GES_5_usages',
 'Classe_inertie_bâtiment',
 'Deperditions_enveloppe',
 'Conso_refroidissement_dépensier_é_primaire',
 'Ubat_W/m²_K',
 'Type_émetteur_installation_chauffage_n°2',
 'Besoin_ECS',
 'Type_énergie_principale_chauffage',
 'Conso_5_usages/m²_é_finale',
 'Code_INSEE_(BAN)',
 'Déperditions_portes',
 'Conso_ECS_dépensier_é_finale',
 'Nombre_appartement',
 'Déperditions_murs',
 'Surface_totale_capteurs_photovoltaïque',
 'Conso_chauffage_générateur_n°1_installation_n°2',
 'Coût_chauffage_énergie_n°2',
 'Volume_stockage_générateur_ECS_n°2',
 'Code_postal_(BAN)',
 'Type_générateur_ECS_n°2',
 'Type_générateur_n°2_installation_n°2',
 'Coût_total_5_usages',
 'Coût_ECS',
 'Conso_chauffage_installation_chauffage_n°2',
 'Type_installation_solaire',
 'Description_générateur_ECS_n°1',
 'Coût_éclairage',
 'Coût_refroidissement_dépensier',
 'Type_générateur_n°2_installation_n°1',
 'Type_énergie_n°3',
 'Coût_ECS_énergie_n°1',
 'Surface_tertiaire_immeuble',
 'Coût_refroidissement',
 'Conso_chauffage_dépensier_générateur_n°2_installation_n°1',
 'Zone_climatique_',
 'Conso_refroidissement_é_primaire',
 'Coût_chauffage_énergie_n°3',
 'Conso_5_usages_é_finale',
 'Usage_générateur_n°1_installation_n°1',
 'Nombre_module',
 'Conso_auxiliaires_é_primaire',
 'Coût_chauffage',
 'Emission_GES_éclairage',
 'Type_énergie_principale_ECS',
 'Description_installation_chauffage_n°2',
 'Appartement_non_visité_(0/1)',
 'N°_voie_(BAN)',
 'Conso_chauffage_dépensier_générateur_n°1_installation_n°1',
 'Usage_générateur_n°1_installation_n°2',
 'Conso_chauffage_é_primaire',
 'Conso_chauffage_générateur_n°1_installation_n°1',
 'Nombre_logements_desservis_par_installation_ECS',
 'N°_région_(BAN)',
 'Date_établissement_DPE',
 'Coût_chauffage_dépensier',
 'Adresse_(BAN)',
 'Emission_GES_ECS_dépensier',
 'Emission_GES_refroidissement',
 'Etiquette_GES',
 'Statut_géocodage',
 'Déperditions_renouvellement_air',
 'Usage_générateur_ECS_n°2',
 'Coût_ECS_énergie_n°3',
 'Type_générateur_ECS_n°1',
 'Conso_é_finale_installation_ECS',
 'Besoin_refroidissement',
 'Deperditions_planchers_bas',
 'Surface_chauffée_installation_chauffage_n°1',
 'N°_RPLS_logement',
 'Type_énergie_n°2',
 'Conso_ECS_é_finale',
 'Usage_générateur_n°2_installation_n°1',
 'Code_postal_(brut)',
 'Emission_GES_chauffage',
 'Inertie_lourde_(0/1)',
 'Conso_éclairage_é_finale',
 'Conso_5_usages_par_m²_é_primaire',
 'Configuration_installation_ECS',
 'Coût_ECS_énergie_n°2',
 'Type_installation_ECS',
 'Type_générateur_froid',
 'N°_DPE_immeuble_associé',
 'Date_visite_diagnostiqueur',
 'Adresse_brute',
 'Type_énergie_générateur_n°1_installation_n°2',
 'Position_logement_dans_immeuble',
 'Conso_auxiliaires_é_finale',
 'Surface_ventilée',
 "Cage_d'escalier",
 'Coût_ECS_dépensier',
 'Qualité_isolation_plancher_haut_comble_aménagé',
 'Déperditions_ponts_thermiques',
 'Emission_GES_refroidissement_dépensier',
 'Présence_brasseur_air_(0/1)',
 'Deperditions_baies_vitrées',
 'Invariant_fiscal_logement',
 'Score_BAN',
 'Production_ecs_solaire_installation',
 'Conso_éclairage_é_primaire',
 'Conso_5_usages_é_primaire',
 'Conso_chauffage_générateur_n°2_installation_n°2',
 'Type_bâtiment',
 'Conso_chauffage_é_finale',
 'Type_énergie_générateur_ECS_n°1',
 'Type_énergie_générateur_n°1_installation_n°1',
 'Hauteur_sous-plafond',
 'Conso_chauffage_dépensier_générateur_n°1_installation_n°2',
 'N°_étage_appartement',
 'N°_DPE_remplacé',
 'Type_énergie_n°1',
 'Conso_chauffage_installation_chauffage_n°1',
 'Type_générateur_n°1_installation_n°1',
 'Méthode_application_DPE',
 'Conso_chauffage_dépensier_é_finale',
 'Emission_GES_5_usages_énergie_n°1',
 'Qualité_isolation_plancher_bas',
 'Conso_chauffage_générateur_n°2_installation_n°1',
 'Ventilation_postérieure_2012_(0/1)',
 'Identifiant__BAN',
 'Type_installation_chauffage_n°1',
 'Présence_production_PV_(0/1)',
 'N°DPE',
 'Classe_altitude',
 'Nom__commune_(BAN)',
 'Deperditions_planchers_hauts',
 'Type_installation_chauffage',
 'Nom_résidence',
 'Emission_GES_chauffage_dépensier',
 'Conso_chauffage_dépensier_é_primaire',
 'Emission_GES_auxiliaires',
 'Catégorie_ENR',
 'Typologie_logement',
 'Conso_refroidissement_annuel',
 "Complément_d'adresse_logement",
 'Surface_habitable_immeuble',
 'Configuration_installation_chauffage_n°2',
 'Description_installation_chauffage_n°1',
 'COP_générateur_ECS_n°2',
 'Surface_habitable_logement',
 'Conso_é_finale_générateur_ECS_n°2',
 'Nombre_niveau_logement',
 'Etiquette_DPE',
 'Version_DPE',
 'Coût_auxiliaires',
 'Electricité_PV_autoconsommée',
 'Nom__rue_(BAN)',
 'Système_production_électricité_origine_renouvelable',
 'Qualité_isolation_enveloppe',
 'Type_ventilation',
 'Coordonnée_cartographique_X_(BAN)',
 'Description_générateur_ECS_n°2',
 'Besoin_chauffage',
 'Type_émetteur_installation_chauffage_n°1',
 'Protection_solaire_exterieure_(0/1)',
 'Qualité_isolation_menuiseries',
 'Conso_é_finale_générateur_ECS_n°1',
 'Emission_GES_5_usages_par_m²',
 'N°_département_(BAN)',
 'N°_immatriculation_copropriété',
 'COP_générateur_ECS_n°1',
 'Indicateur_confort_été',
 'Conso_ECS_dépensier_é_primaire',
 'Surface_chauffée_installation_chauffage_n°2',
 "Complément_d'adresse_bâtiment",
 'Conso_refroidissement_é_finale',
 'Coordonnée_cartographique_Y_(BAN)',
 'Type_énergie_générateur_n°2_installation_n°1',
 'Isolation_toiture_(0/1)',
 'Date_réception_DPE',
 'Modèle_DPE',
 'Logement_traversant_(0/1)',
 'Description_installation_ECS',
 'Conso_ECS_é_primaire',
 'Coût_chauffage_énergie_n°1',
 'Date_fin_validité_DPE',
 'Configuration_installation_chauffage_n°1',
 'Type_installation_ECS_(général)',
 'Volume_stockage_générateur_ECS_n°1',
 'Conso_5_usages_é_finale_énergie_n°1',
 'Type_énergie_générateur_ECS_n°2',
 'Surface_climatisée',
 'Emission_GES_5_usages_énergie_n°3',
 'Qualité_isolation_murs',
 'Conso_refroidissement_dépensier_é_finale',
 'Usage_générateur_ECS_n°1',
 'Type_installation_chauffage_n°2',
 'Usage_générateur_n°2_installation_n°2',
 'Nombre_niveau_immeuble',
 'Conso_chauffage_dépensier_générateur_n°2_installation_n°2',
 'Type_énergie_générateur_n°2_installation_n°2',
 'Surface_habitable_desservie_par_installation_ECS',
 'Emission_GES_5_usages_énergie_n°2',
 'Emission_GES_ECS',
 'passoire_energetique']