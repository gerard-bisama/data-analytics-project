# Data Analytics Projects – Public Health Supply Chain

This repository contains data analytics and machine learning projects focused on improving **supply chain decision-making for health commodities**.

The projects are inspired by real-world challenges faced in **health logistics systems**, particularly the need to improve **order quantity planning and stock availability at health facilities**.

## Two analytical projects are currently included in this repository.

## Repository Structure

data_analytic_project/
│
├── README.md
├── order_prediction/
└── max_stock_test/
Each subdirectory contains a complete analytical project including code, methodology, and results.

---

# Project 1 – Order Quantity Prediction

📁 Directory: **order_prediction/**

## Objective

The objective of this project is to **build a predictive model that estimates the quantity of health products facilities should order**, based on historical consumption data.

Accurate order predictions help reduce:

- stock-outs
- overstocking
- emergency orders
  It provides also clues to use by supply chain analysis to detect potential non regular orders.

➡️ See full project:  
`[this](order_prediction/README.md)`

---

# Project 2 – Maximum Stock Level Hypothesis Test

📁 Directory: **max_stock_test/**

## Objective

This project evaluates a key supply chain policy question:

**If facilities receive quantities that raise their stock level to a maximum of 5 months of stock, are they less likely to experience stock-outs during the order cycle?**

The goal is to statistically test whether maintaining a **maximum stock level of 5 months** significantly reduces stock-out risk.

## Analytical Question

Hypothesis tested:

**H₀ (Null Hypothesis)**  
Facilities supplied up to 5 months of stock are **not less likely** to experience stock-outs.

**H₁ (Alternative Hypothesis)**  
Facilities supplied up to 5 months of stock are **less likely** to experience stock-outs.

➡️ See full project:  
`/max_stock_test`

---

# Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Statsmodels
- Matplotlib / Seaborn
- Jupyter Notebook

---

# Author

This repository contains applied analytics projects inspired by real-world **health supply chain data systems and logistics operations**.
