Words with a * next to it is explained in the Deeper Explanations section.

# Wildlife Health Data Warehouse
Project Lead: Luke Herron | Institution: University of Technology Sydney

# Project Overview
This repository contains the architecture and ETL pipeline for a specialised wildlife health data warehouse that specifically adheres to the FAIR and CARE Guiding Principles. Guided by the One Health* approach, the project addresses critical gaps in veterinary data standards. The goal is to provide a secure, scalable, and ethical solution for multi-agency data integration and ensuring Indigenous Data Sovereignty is maintained alongside scientific utility.

# Core Features
- Optimised Star Schema Dimensional Model for high-performance querying of clinical observations.
- Standarised indexing and metadata structures within a PostgreSQL environment to ensure easy indexing and discovery. 
- Automated mapping of GPS coordinates (longitude/latitude) to Indigenous Country names within the _dim_location_ table.
- Built to allow for cross-database integration with other global health and biodiversity repositories.
- A Python-driven Automated ETL Pipeline for cleaning and validation of raw veterinary field data into a central repository.
- Centralised Security Model to enforce robust access rules and data-sharing agreements between multiple agencies.
- Scalable Analytics with a focus on supporting longitudinal health trend analysis across diverse Australian species.


# Deeper Explanations
- FAIR* = Findable, Accessible, Interoperable, Reusable. Focuses on the technical utility of scientific data.
- CARE* = Collective Benefit, Authority to Control, Responsibility, Ethics. Focuses on Indigenous Data Sovereignty and ethical governance.
- One Health* = An integrated approach that recognises the interconnections between human, animal, and environmental health.`