# Exploratory Data Analysis

## 📌 Overview

This section presents an exploratory data analysis (EDA) of the malaria supply chain dataset, focusing on inventory patterns across multiple variables of the dataset. The analysis highlights key statistical characteristics such as distribution, variability, and outlier behavior, and links them to underlying supply chain dynamics.
These insights provide a critical foundation for subsequent work, including A/B testing of supply policies and the development of machine learning models aimed at improving demand forecasting, stock optimization, and decision-making within the health supply chain system.

## Data quality and outliers detection

The analysis covers multiple product groups:

- **ACT** – First-line malaria treatment
- **PYRA** – Alternative treatment
- **ART** – Severe malaria treatment
- **SP** – Treatment and prevention
- **PREV** – Diagnostic (RDT) and preventive (ITN) products

---

## Key Findings

### 1. Systemic Stock Imbalances Across Product Groups

The analysis reveals that stock imbalances are **systemic rather than product-specific**.

- The proportion of outliers remains relatively consistent across product groups, typically ranging between **5% and 7%**
- Peaks of **8% to 13%** are observed in higher-level facilities, particularly for **ART products**

These results indicate that:

> Inventory inefficiencies are driven by structural supply chain issues rather than the characteristics of individual products.

---

### 2. Facility-Level Patterns of Inefficiency

#### Health Centers

- Show **consistent and concentrated outliers** across all product groups
- Indicate **uniform but suboptimal supply practices**

This suggests:

> Standardized resupply mechanisms are applied but do not adequately reflect real consumption patterns, leading to systematic overstocking.

---

#### District Hospitals

- Exhibit **moderate but inconsistent performance**
- Suggest uneven implementation of inventory management practices

---

#### Regional Hospitals

- Display **variable performance depending on product group**
  - More stable for **PREV products**
  - Less stable for **PYRA and ART**

This indicates:

> Sensitivity to both demand variability and supply fluctuations.

---

#### National Hospitals

- Show the **highest variability and dispersion of outliers**
- In some cases, the **highest proportion of outliers**

This suggests:

> System inefficiencies are amplified at higher levels of care, where complexity increases.

---

### 3. Product Group Comparison

#### Treatment Products (ACT, PYRA, SP)

- Show **consistent inefficiencies across all facility types**
- Reflect **misalignment between supply quantities and actual consumption**

---

#### Severe Malaria Products (ART)

- Exhibit **greater instability**, especially in higher-level facilities
- Likely driven by **unpredictable and irregular demand patterns**

---

#### Diagnostic and Preventive Products (PREV)

- Show relatively **better control at some levels** (e.g., regional hospitals)
- Still exhibit **system-wide inefficiencies**, particularly at:
  - Health centers
  - National hospitals

---

## Overall Conclusion

Across all product groups and facility levels, the analysis highlights **system-wide inefficiencies in inventory management**.

Key systemic issues include:

- Persistent overstocking patterns
- Weak alignment between supply and consumption
- Increasing variability with system complexity
- Limited responsiveness of supply mechanisms to real demand signals

> These findings suggest that improving supply chain performance will require **system-level interventions**, including better forecasting models, adaptive resupply policies, and enhanced data-driven decision-making.

---

## Implications for Further Analysis

These results provide a strong foundation for the analytical projects in this repository:

- **Order Quantity Prediction** → Improve alignment between supply and consumption
- **Maximum Stock Policy Testing** → Evaluate optimal stock levels
- **Requested vs Approved Analysis** → Assess supply allocation efficiency
