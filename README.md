# CarPrice Prediction

Predicting used car prices in Iran using data scraped from Divar.ir.

---

## About

This project collects car listings from Divar.ir through web scraping, processes the raw data, and trains machine learning models to predict used car prices based on features such as brand, year, mileage, and condition.

---

## Project Structure

```
CarPrice_Prediction/
│
├── Data/                  # Processed datasets
├── ScrapeData/            # Raw scraped data
│
├── utils.py               # Helper functions
├── 01_eda.ipynb           # Exploratory data analysis
├── ep.ipynb               # Feature engineering and modeling
│
├── requirements.txt       # Project dependencies
└── README.md
```

---

## Setup

```bash
git clone https://github.com/Behniash/CarPrice_Prediction.git
cd CarPrice_Prediction

pip install -r requirements.txt
```

Run the notebooks in order:

1. `01_eda.ipynb` — data exploration and visualization
2. `ep.ipynb` — feature engineering and model training

---

## Stack

- **Python** — core language
- **Requests / BeautifulSoup** — web scraping
- **Pandas / NumPy** — data processing
- **Matplotlib / Seaborn** — visualization
- **Scikit-learn** — modeling

---

## Pipeline

1. Scrape car listings from Divar.ir
2. Clean raw data and handle missing values
3. Exploratory analysis of price, brand, year, and mileage
4. Feature engineering and encoding
5. Train and evaluate regression models

---

## Disclaimer

This project is intended for educational and research purposes only.
Scraping was done with request rate limiting to avoid overloading the server.

---

## Author

Behniash — [GitHub](https://github.com/Behniash)
