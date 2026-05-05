# Wildlife Health Data Warehouse
Project Lead: Luke Herron | Institution: University of Technology Sydney

## Project Overview
This repository contains the architecture and ETL pipeline for a specialised wildlife health data warehouse that specifically adheres to the FAIR (Findable, Accessible, Interoperable, Reusable) and CARE (Collective Benefit, Authority to Control, Responsibility, Ethics) Guiding Principles. Guided by the One Health approach, that recognises the interconnections between human, animal, and environmental health, the project addresses critical gaps in veterinary data standards. The goal is to provide a secure, scalable, and ethical solution for multi-agency data integration and ensuring Indigenous Data Sovereignty is maintained alongside scientific utility.

## Core Features
- Optimised Star Schema Dimensional Model for high-performance querying of clinical observations.
- Standarised indexing and metadata structures within a PostgreSQL environment to ensure easy indexing and discovery. 
- Automated mapping of GPS coordinates (longitude/latitude) to Indigenous Country names within the _dim_location_ table.
- Built to allow for cross-database integration with other global health and biodiversity repositories.
- A Python-driven Automated ETL Pipeline for cleaning and validation of raw veterinary field data into a central repository.
- Centralised Security Model to enforce robust access rules and data-sharing agreements between multiple agencies.
- Scalable Analytics with a focus on supporting longitudinal health trend analysis across diverse Australian species.

## Local Setup & Installation
Follow these steps to set up the Wildlife Health Data Warehouse environment on a new machine.

### Prerequisites
* **Python 3.10+** installed on your system.
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

Before proceeding, ensure your local PostgreSQL instance has a database created named wildlife_health.

### 5. Initialize the Data Warehouse
Run the ETL pipeline scripts in the following order to build the schema and populate the mock data:
```bash
python src/database/initialise_warehouse.py
python src/database/populate_dates.py
python src/database/populate_environment.py
python src/database/generate_mock_data.py
```
