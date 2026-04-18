# 📊 Malaria Supply Chain Data Analysis Project - Data Preparation

## 📌 Overview

This project analyzes routine logistics data from a malaria commodity supply chain system. The dataset reflects real-world operations where health facilities report monthly stock and consumption data, and place orders on a quarterly basis.

The objective of this project is to:

- Assess reporting performance
- Evaluate inventory management practices
- Analyze demand vs supply gaps
- Build a foundation for advanced analytics and predictive modeling

➡️ See full analysis details on notebook file:  
[Data Preparation](Data%20Preparation.ipynb)

---

## 🚧 Project Status

This step focus on the Data Understanding & Preparation Phase.

## 🔍 Key Insights

### Structured Dataset

- The dataset follows a structured pattern of facility × product × month, indicating a standardized reporting system.
- Dataset structure analysis (~170,676 records, 14 variables).
- Uniform product occurrences across all commodities

---

### Reporting Trend

Reporting completeness improved over time:

- 2024-01: 1221 observations
- 2025-02: 1388 observations

Progressive improvement in reporting compliance.
Peak performance in early 2025.
Slight variability in later periods.

---

## Missing Data

- Core inventory variables: ~28% missing → missing reports
- quantityrequested: ~72% missing → non-order months
- quantityapproved: ~19% missing → supply variability

Missing data is due to the operational logic, not data quality issue.

---

### Consumption Patterns

- Median dispensed: 183
- Strong variability across facilities
- Presence of high-demand facilities
  Consumption is Highly Heterogeneous.

---

### Inventory Levels

- Stockinhand shows indicates that facilities generally maintain positive stock levels, with no evidence of widespread stockouts within the year.The wider variability (1549-200) shows that facilities hold very diffrent stock level.
- AMC shows smooth distribution with no zeros at the quartiles but with high variability 28 to 4,862.

---

### Demand vs Supply

Quantityapproved is oftem lower then requested median=42 vs 652,show that facilities request much more than what they received.
