# Gold Price Forecasting Project

This project predicts future gold prices using Prophet. It pulls data from Alphavantages, trains a model, stores results in PostgreSQL, and visualizes everything in Grafana.  
The goal is to build a simple end-to-end forecasting pipeline that runs inside Docker.

## What It Does

- Downloads gold price data (GLD) from Alphavantages
- Uses Prophet to forecast future prices  
- Saves both historical and predicted data into PostgreSQL  
- Displays the data in Grafana dashboards  
- Runs the full stack (Django, PostgreSQL, Grafana) with Docker Compose  

## Stack

- Python (Prophet, Alphavantages, pandas)
- PostgreSQL
- Grafana
- Docker / Docker Compose

## Project Structure

```bash
django-docker/
├── gold_app/
│   ├── code/
│   │   └── gold_prediction.py      # Main forecasting script
│   ├── views.py                    # Django view for displaying results
│   ├── urls.py
│   └── templates/
├── Dockerfile                      # Django Docker image
├── docker-compose.yml              # Runs all services
├── requirements.txt
└── README.md
```

## How to Run

1. Make sure Docker and Docker Compose are installed.  
2. Clone the project:

```bash
git clone https://github.com/yourusername/gold-forecasting.git
cd gold-forecasting
```

3. Build and run:

```bash
docker compose up --build -d
```

4. Once it’s up:  
   - Django: [http://localhost:8000](http://localhost:8000)  
   - Grafana: [http://localhost:3000](http://localhost:3000)  
     - user: `admin`  
     - password: `admin`  
   - PostgreSQL: `localhost:5432` (user: `postgres`, password: `postgres`)

## How It Works

- The Python script (`gold_prediction.py`) downloads gold prices from Alpha vantages.  
- It trains a Prophet model with yearly and monthly seasonality.  
- It generates forecasts for the next 365 days.  
- The results are stored in the PostgreSQL database.  
- Grafana connects to the same database to visualize trends and forecasts.

## Common Issues

- If you see “waiting for db...”, Django is waiting for PostgreSQL to start — this is normal.  
- “Importing plotly failed” just means interactive plots are disabled — the forecast still works fine.  
- Make sure your internet connection is stable; Yahoo Finance data requires it.

## Future Improvements

- Add a REST API to fetch forecasts directly.  
- Automate daily retraining using Celery.  
- Add more visualizations to Grafana (e.g. confidence intervals, historical trends).

## About

This project was built to practice integrating data science tools (Prophet, pandas) with web and visualization tools (Django, Grafana).  
It demonstrates a complete data flow — from fetching and forecasting to storing and visualizing.

— Kasra

