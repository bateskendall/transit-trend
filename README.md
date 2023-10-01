# MTA Real-time Data Pipeline

This project is designed to fetch, transform, and load real-time data from the Metropolitan Transit Authority's GTFS-rt data feeds into a PostgreSQL database. It provides a robust data pipeline for managing and analyzing transit data.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites
- Python 3.7 or later
- PostgreSQL

### Database Setup and API Key
Before running the pipeline, you'll need to set up a PostgreSQL database and obtain an API key from MTA.

1. **Database Setup**:
   - Install [PostgreSQL](https://www.postgresql.org/download/) if you haven't already.
   - Create a new database for this project.

2. **API Key**:
   - Visit the [MTA Real-Time Data Feeds page](https://api.mta.info/#/signup) to sign up for an API key.
   - Once you have the key, add it to your environment variables as `MTA_API_KEY`.

3. **Environment Variables**:
   - It's a good practice to store sensitive information such as your database credentials and API key as environment variables.
   - Place them in a .env file and the config.py file will pull them to authenticate.

### Steps

1. Clone the repository:
```bash
git clone https://github.com/bateskendall/transit-trend.git
cd transit-trend
```

2. Create a virtual environment and install dependencies:
```bash
python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
pip install -r requirements.txt
```

3. Set up your PostgreSQL database and update the config.py file with your database credentials.

4. Run the main.py script to initiate the data pipeline:
```bash
python main.py
```

## Usage

- Once installed, the data pipeline will fetch data from the MTA's real-time data feeds every 30 seconds by default.

- The fetched binary data is transformed into a structured format and loaded into the PostgreSQL database for further analysis.

## Architecture

- extractor.py: Module for fetching real-time binary data from MTA's API.
- loader.py: Module for loading the binary data into the PostgreSQL database.
- transformer.py: Module for transforming the binary data into a structured format.
- tf_loader.py: Module for loading the structured data into the PostgreSQL database.
- scheduler.py: Module for scheduling the data fetching, transformation, and loading processes.
- load_static_gtfs.py: Module for loading static gtfs data from .txt files in /data folder.

