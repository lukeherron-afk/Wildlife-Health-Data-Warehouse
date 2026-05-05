# Wildlife Health Data Warehouse
Project Lead: Luke Herron | Institution: University of Technology Sydney

## Project Overview
This repository contains the architecture and ETL pipeline for a specialised wildlife health data warehouse that specifically adheres to the FAIR (Findable, Accessible, Interoperable, Reusable) and CARE (Collective Benefit, Authority to Control, Responsibility, Ethics) Guiding Principles. Guided by the One Health approach, that recognises the interconnections between human, animal, and environmental health, the project addresses critical gaps in veterinary data standards. The goal is to provide a secure, scalable, and ethical solution for multi-agency data integration and ensuring Indigenous Data Sovereignty is maintained alongside scientific utility.

## Core Features
- Integrated Star Schema: Optimised for high-performance querying of clinical observations.
- Sovereign Data Mapping: Automated GPS-to-Country enrichment in the `dim_location` table.
- Validated ETL Pipeline: Python-driven cleaning and biological validation of raw veterinary field data.
- Interactive Analytics: A Streamlit dashboard for real-time health trend analysis.
- Dockerized Architecture: One-click deployment.

## Docker Deployment

### 1. Clone the Repository
```bash
git clone <https://github.com/lukeherron-afk/Wildlife-Health-Data-Warehouse.git>
cd WILDLIFE_HEALTH_DATA_WAREHOUSE
```

### 2. Launch with Docker
```bash
docker-compose up --build
```
*This command initialises the PostgreSQL database, runs the full ETL pipeline, and starts the Streamlit UI.*

### 3. Launch Analytics
Navigate to *http://localhost:8501/* in a browser to experience the Interactive Analytics.

---

## Manual Local Setup (Alternative)

### Prerequisites
* **Python 3.11+** installed on your system.
* **PostgreSQL** installed and running locally.

### 1. Clone the Repository
```bash
git clone <https://github.com/lukeherron-afk/Wildlife-Health-Data-Warehouse.git>
cd WILDLIFE_HEALTH_DATA_WAREHOUSE
```

### 2. Create and Activate a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.

#### Windows: 
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a file named .env in the root directory of the project and add your PostgreSQL database connection string:
```plaintext
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/wildlife_health
```
*Before proceeding, ensure your local PostgreSQL instance has a database created named wildlife_health.*

### 5. Initialize the Data Warehouse
Run the ETL pipeline scripts in the following order to build the schema and populate the mock data:
```bash
python -m src.database.initialise_warehouse
python -m src.database.populate_dates
python -m src.database.populate_environment
python -m src.database.generate_mock_data
```

### 6. Launch Analytics
```bash
# Run the Interactive Dashboard
streamlit run src/dashboard.py

# OR Generate Static PNG Reports
python -m src.analysis.generate_health_report
```

## Research Context
This prototype was developed using the Design Science Research (DSR) methodology as part of an Engineering Capstone project. It serves as a proof-of-concept for bridging the gap between scientific biodiversity repositories and ethical data governance frameworks.