# 🚲 Toulouse Bike Analytics

**An End-to-End Data Engineering Pipeline for Toulouse Bike-Sharing Data**

An automated data engineering project that collects, validates, stores, transforms, and analyzes bike-sharing availability data from Toulouse's VélÔToulouse network.

The pipeline uses **Python, PostgreSQL, Docker, Apache Airflow, dbt, pytest, and GitHub Actions** to implement a reproducible data processing workflow.

## Project Overview

The objective of this project is to build an end-to-end data pipeline capable of collecting historical bike-sharing availability data and transforming it into structured datasets ready for analytics.

The system collects station information and bike availability snapshots from the GBFS (General Bikeshare Feed Specification) API.

It enables analysis of:

- Bike availability across stations.
- Station occupancy and empty-station frequency.
- Availability patterns by hour and day of the week.
- Mechanical versus electric bike availability.
- Historical availability trends.

The project focuses on data ingestion, orchestration, data quality, and analytical data modeling rather than dashboard development.

## Architecture

```text
               VélÔToulouse GBFS API
                        |
                        v
                  Python ETL
              Extract → Validate
              → Transform → Load
                        |
                        v
                    PostgreSQL
                  Raw Data Tables
                station_infos
                station_status
                        |
                        v
                       dbt
                 Staging Models
                        |
                        v
                Analytical Models
              Dimensions + Fact Table
                        |
                        v
                  KPI Aggregations

        Apache Airflow orchestrates the pipeline
              every 15 minutes

        Docker Compose manages the services
        GitHub Actions runs CI checks
```

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data extraction, validation, transformation, and loading |
| PostgreSQL | Relational data storage and historical snapshots |
| Docker | Containerized environments |
| Docker Compose | Multi-service configuration |
| Apache Airflow | Workflow orchestration and scheduling |
| dbt Core | SQL transformations and analytical modeling |
| pytest | Python unit testing |
| GitHub Actions | Continuous integration |
| Git | Version control |

## Data Sources

The pipeline uses two GBFS data feeds from Toulouse's bike-sharing network.

**Station Information**

Contains relatively static station attributes, including station identifiers, names, geographic coordinates, addresses, and capacities.

**Station Status**

Contains operational information, including available bikes, available docks, mechanical and electric bike counts, and station operating status.

The pipeline periodically collects these feeds to build a historical record of station availability.

## Python ETL Pipeline

The ETL pipeline is organized into separate Python modules.

### Extract

`src/extract.py`

Retrieves data from the GBFS endpoints using HTTP requests. Includes request timeouts and error handling.

### Validate

`src/validate.py`

Checks incoming data for validity before loading it into PostgreSQL.

### Transform

`src/transform.py`

Prepares data for storage, including column mappings, field normalization, and transformations required by the database schema.

### Load

`src/load.py`

Loads validated and transformed data into PostgreSQL.

The loading process supports conflict handling to avoid duplicate records and maintain station information.

### Database

`src/database.py`

Manages PostgreSQL connections and database operations.

### Pipeline Entry Point

`src/main.py`

Coordinates the execution of the ETL pipeline.

## PostgreSQL Data Model

The ingestion database contains two main tables.

| Table | Description |
|---|---|
| `station_infos` | Station identifiers and descriptive attributes |
| `station_status` | Historical station availability observations |

The `station_status` table uses the composite primary key:

```sql
PRIMARY KEY (station_id, collected_at)
```

This allows a station to have multiple historical observations while preventing duplicate records for the same station and collection timestamp.

Foreign-key constraints ensure that station availability observations reference existing stations.

Database definitions are maintained in `sql/schema.sql`.

## Workflow Orchestration — Apache Airflow

Apache Airflow orchestrates the pipeline using the DAG:

` toulouse_bikes_pipeline `

**Schedule:** Every 15 minutes.

The workflow consists of four tasks:

```text
run_etl
   |
   v
quality_check
   |
   v
dbt_run
   |
   v
dbt_test
```

**run_etl** extracts and processes the GBFS data, then loads it into PostgreSQL.

**quality_check** verifies that the expected number of station observations was loaded for the current logical execution date.

**dbt_run** builds the SQL transformation models.

**dbt_test** validates the analytical models using dbt tests.

The DAG includes retry handling for transient failures and restricts overlapping DAG runs.

The Airflow logical date is used to identify collection batches consistently across task retries.

## dbt — Data Transformation

dbt transforms the ingestion tables into analytical datasets within PostgreSQL.

The project follows a layered modeling approach.

### Staging Layer

- `stg_station_infos`
- `stg_station_status`

These models standardize the source data and prepare it for downstream transformations.

### Analytical Layer

**Dimension tables**

- `dim_station` — Station attributes.
- `dim_time` — Date and time attributes derived from collection timestamps.

**Fact table**

- `fct_station_availability` — Bike availability observations by station and collection timestamp.

### KPI Aggregations

| Model | Purpose |
|---|---|
| `agg_station_availability` | Average bike availability and empty-station frequency |
| `agg_hourly_availability` | Availability patterns by hour |
| `agg_weekday_availability` | Availability patterns by day of the week |
| `agg_bike_types` | Electric bike availability and proportion |

These models provide analytics-ready datasets for SQL queries and potential BI dashboards.

## Data Quality and Testing

The project includes multiple layers of validation.

**Python tests — pytest**

Unit tests cover extraction, transformation, and validation logic.

**PostgreSQL constraints**

Database constraints provide primary-key, foreign-key, and other data integrity checks.

**Airflow quality check**

Verifies the number of loaded station observations for each pipeline execution.

**dbt tests**

Tests validate properties including:

- Uniqueness and non-null requirements.
- Referential integrity.
- Non-negative availability values.
- Valid time dimensions.
- KPI values within expected ranges.
- Uniqueness of station and timestamp combinations.

## Continuous Integration — GitHub Actions

The repository includes a GitHub Actions workflow:

`.github/workflows/ci.yml`

The workflow runs on pushes and pull requests targeting `main`.

It contains two jobs.

**Python tests**

Installs Python dependencies and runs automated unit tests using pytest.

Manual database integration tests are excluded from this CI job.

**dbt validation**

Installs dbt Core and the PostgreSQL adapter, then runs `dbt parse` to validate the project configuration and model definitions.

Full dbt SQL execution and data tests are performed within the Airflow pipeline, rather than by this CI workflow.

## Repository Structure

```text
toulouse-bike-analytics/
|
├── .github/
│   └── workflows/
│       └── ci.yml
|
├── airflow/
│   ├── docker-compose.yaml
│   └── dbt-profiles/
│       └── profiles.yml
|
├── dags/
│   └── bike_pipeline_dag.py
|
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   ├── tests/
│   └── dbt_project.yml
|
├── sql/
│   ├── schema.sql
│   └── test_schema.sql
|
├── src/
│   ├── config.py
│   ├── database.py
│   ├── extract.py
│   ├── validate.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
|
├── tests/
├── Dockerfile
├── Dockerfile.airflow
├── compose.yaml
├── requirements.txt
├── requirements-dbt.txt
└── README.md
```

## Getting Started

### Prerequisites

- Docker Desktop with Docker Compose
- Git
- Sufficient memory and storage for the local Airflow environment

Python and dbt can be run locally for development, but the project is designed around Docker containers.

### 1. Clone the Repository

```bash
git clone <https://github.com/Jalilo-C/toulouse-bike-analytics.git>
cd toulouse-bike-analytics
```

Replace the placeholder with the actual GitHub repository URL.

### 2. Configure Environment Variables

Create a `.env` file at the project root.

Configure the PostgreSQL connection settings and the Airflow environment variables required by the Compose files.

Example variable names:

```dotenv
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=toulouse_bike_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=replace_with_a_secure_password
AIRFLOW_UID=50000
```

This is an illustrative configuration. Adjust it to match the Compose services and your local environment.

**Never commit real credentials or the `.env` file to Git.**

### 3. Build Docker Images

```bash
docker compose --env-file .env \
  -f compose.yaml \
  -f airflow/docker-compose.yaml \
  build
```

### 4. Start PostgreSQL

```bash
docker compose --env-file .env \
  -f compose.yaml \
  -f airflow/docker-compose.yaml \
  up -d db
```

Initialize the application database using the SQL definitions in `sql/schema.sql` if the tables have not already been created.

### 5. Initialize and Start Airflow

The Airflow environment uses the initialization service provided by its Docker Compose configuration.

On a fresh environment, initialize Airflow before starting its services:

```bash
docker compose --env-file .env \
  -f compose.yaml \
  -f airflow/docker-compose.yaml \
  up airflow-init
```

Then start the configured services:

```bash
docker compose --env-file .env \
  -f compose.yaml \
  -f airflow/docker-compose.yaml \
  up -d
```

Airflow is configured locally to use:

`http://localhost:8081`

Open the Airflow interface and locate:

`toulouse_bikes_pipeline`

Enable the DAG to run on its schedule, or manually trigger an execution for testing.

### 6. Check the dbt Configuration

The dbt environment is available inside the custom Airflow image.

An example validation command is:

```bash
docker compose --env-file .env \
  -f compose.yaml \
  -f airflow/docker-compose.yaml \
  run --rm --no-deps \
  --entrypoint /home/airflow/dbt-venv/bin/dbt \
  airflow-worker debug \
  --project-dir /opt/airflow/dbt \
  --profiles-dir /opt/airflow/dbt-profiles
```

The dbt container connects to PostgreSQL using the internal Docker service name `db` and port `5432`.

For execution from the host machine, the PostgreSQL service uses its published host port, configured as `5433` in this project's local setup.

### 7. Run Python Unit Tests

Install the Python requirements and pytest:

```bash
python -m pip install -r requirements.txt
python -m pip install pytest
```

Then run:

```bash
python -m pytest tests/ --ignore=tests/test_load_manual.py
```

Database integration tests require a configured PostgreSQL instance.

## Reliability Considerations

The pipeline includes several mechanisms to improve reliability:

- HTTP request timeouts and exception handling.
- PostgreSQL constraints and conflict handling.
- Task retries in Airflow.
- Consistent logical timestamps for scheduled executions.
- Data quality checks after ingestion.
- dbt model tests.
- Automated CI checks.

These mechanisms reduce common pipeline failures but do not eliminate the need for monitoring or operational maintenance.

## Possible Future Improvements

Potential extensions include:

- Incremental dbt materializations for growing historical datasets.
- Expanded integration testing with a temporary PostgreSQL database.
- Improved monitoring and alerting.
- Performance benchmarking.
- A BI dashboard for exploring historical station availability.

## Project Purpose

This project was developed as a hands-on Data Engineering portfolio project to gain practical experience with data ingestion, relational databases, workflow orchestration, containerization, SQL transformations, automated testing, and continuous integration.

Its main objective is to demonstrate the design and implementation of a maintainable end-to-end data pipeline.
