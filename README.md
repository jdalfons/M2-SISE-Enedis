# M2-Enedis

<p align="center">
    <img src="assets/logo.png" alt="M2-Enedis Logo" width="200">
</p>

## Application Status

| Status                | Description                          |
|-----------------------|--------------------------------------|
| **Current Version**   | 1.0.0                                |
| **Python Version**    | 3.11                                 |
## Overview

M2-Enedis is a dashboard application built using Dash and Plotly. It provides various functionalities including data visualization, machine learning predictions, and interactive maps. The application is designed to help users understand and analyze energy consumption data.

You can see an explanation of the application in the following video: [Watch Video](https://youtu.be/TH3bm7r2nYE)


## Before install

Ensure you have the latest data in the `dataset` folder. If the repository does not contain the latest version, you can download it from the following URL: [Download Latest Dataset](https://drive.google.com/file/d/1Y5EPyN07dRrQ9i70DckcayalByRuakpq/view?usp=sharing)


## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/greentech_dashboard.git
    cd greentech_dashboard
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the Dash application:**
    ```sh
    python app.py
    ```

2. **Open your web browser and navigate to:**
    ```
    http://127.0.0.1:8050/
    ```

## Running API

1. **Run API**
```sh
    uvicorn main:app --reload
```

## Example API Request

#### Api predict consumption

To send a request to the API, you can use the following example with `curl`:

```sh
curl -X POST "http://127.0.0.1:8000/predict_consomation" -H "Content-Type: application/json" -d '{
  "etiquette_dpe": 3.0,
  "type_batiment": 0.0,
  "annee_construction": 1921.0,
  "classe_inertie_batiment": 1.0,
  "hauteur_sous_plafond": 3.1,
  "surface_habitable_logement": 50.2,
  "type_energie_principale_chauffage": 11.0,
  "isolation_toiture": 1.0,
  "code_postal_ban": 69002.0
}'
```

#### Api predict label

```sh
curl -X POST "http://127.0.0.1:8000/predict_label" -H "Content-Type: application/json" -d '{
    "annee_construction": 1948,
    "surface_habitable_logement": 197.5,
    "cout_total_5_usages": 4415.2,
    "cout_ecs": 409,
    "cout_chauffage": 3937.8,
    "cout_eclairage": 60.4,
    "cout_auxiliaires": 5.0,
    "cout_refroidissement": 0.0
}'
```

Replace `"http://127.0.0.1:8000/predict_etiquets"` with the actual endpoint of your API.

## Usage

- **Home Page:** Provides an introduction of our solution.
- **Context Page:** Provides an introduction of data and key performance indicators (KPIs).
- **Map Page:** Shows interactive maps for data visualization.
- **Analytiques:** Allows users to visualize energy consumption data through interactive graphs for deeper insights and trend analysis.
- **Prediction Page:** Allows users to make predictions using the trained machine learning model.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

| Nom                        | GitHub Profile                     |
|----------------------------|------------------------------------|
| SOURAYA AHMED ABDEREMANE   | [Sahm269](https://github.com/Sahm269) |
| BERTRAND KLEIN             | [bertrandklein](https://github.com/bertrandklein) |
| JUAN DIEGO ALFONSO OCAMPO  | [jdalfons](https://github.com/jdalfons) |
| PIERRE BOURBON             | [pbrbn](https://github.com/pbrbn)  |

## Contact

For any questions or inquiries, please contact Juan Diego A. at [jalfonsooc@univ-lyon2.fr](mailto:jalfonsooc@univ-lyon2.fr).

