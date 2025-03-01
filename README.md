# Nest-Nomics: Edinburgh Property Market Analysis

This repository contains an analysis of the Edinburgh property market using data scraped from Rightmove. The project aims to provide insights into property trends, pricing patterns, and market dynamics in Edinburgh, Scotland.

> [!NOTE]
> This is a one-off analysis project and not intended for ongoing data collection. The data scraped is for personal analysis purposes only, and users should be aware of and respect Rightmove's terms of service when working with their data.

## Project Overview

The analysis consists of two main components:
1. Data collection from Rightmove
2. Analysis of the collected property data

## Repository Structure

- `rightmove_scrape.ipynb`: Jupyter notebook for scraping property data from Rightmove
- `edinburgh_analysis.ipynb`: Jupyter notebook containing the analysis of Edinburgh property market
- `src/`: Source code modules used by the notebooks
  - `postcodes.py`: Module for handling postcode operations
  - `rightmove/`: Modules for interacting with Rightmove data
- `data/`: Directory containing raw and processed datasets

## Data Collection

The data collection process uses the `rightmove_scrape.ipynb` notebook, which:
- Uses postcode data to identify representative areas across Edinburgh
- Searches for properties in these areas using the Rightmove API
- Collects detailed information including property prices, features, and sales history
- Handles rate limiting and pagination to gather comprehensive data
- Exports the raw data to CSV format for subsequent analysis

## Analysis

The `edinburgh_analysis.ipynb` notebook provides:
- Exploratory data analysis of the Edinburgh property market
- Price analysis by location, property type, and features
- Historical price trends
- Visualizations of key market indicators
- Insights into property market patterns across different areas of Edinburgh

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/antoinedao/nest-nomics.git
   cd nest-nomics
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the notebooks:
   - Open and run `rightmove_scrape.ipynb` to gather fresh data
   - Open and run `edinburgh_analysis.ipynb` to perform the analysis

## Requirements

- Python 3.8+
- Jupyter Notebook
- Required Python packages listed in `requirements.txt`

