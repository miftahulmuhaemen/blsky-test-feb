# Pokemon API Scraper

A Python application that scrapes Pokemon data and provides a JSON:API compliant REST API. The application scrapes Pokemon data from PokeAPI and stores it in a local database, making it available through a REST API.

## Features

- Scrapes Pokemon data from PokeAPI
- Stores data in local SQLite database
- Provides REST API endpoints following JSON:API specification

## Requirements

- Python 3.8+
- Required packages (see requirements.txt)

## Installation

1. Clone the repository
```bash
git clone https://github.com/miftahulmuhaemen/pokemon-scraper.git
cd pokemon-scraper
```

2. Create and activate virtual environment
```bash
python<version> -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```
# Usage

To start the application,
```bash
python main.py
```

The application will initialize the database, scrape Pokemon data, and start the API server on http://localhost:8000

# API ENDPOINTS
1. Via Swagger, http://localhost:8000/docs
2. Via ReDoc, http://localhost:8000/redoc

# Project Structure
```
pokemon-scraper/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── scraper.py
│   ├── database.py
│   ├── api.py
│   └── models.py
└── main.py
```