# Data Analytics Projects – PMalaria Supply Chain Data Analysis Project

This repository contains data analytics and machine learning projects focused on improving **supply chain decision-making for health commodities**.

The projects are inspired by real-world challenges faced in **health logistics systems**, particularly the need to improve **order quantity planning and stock availability at health facilities**.

Two analytical projects are currently included in this repository.

## Study Context and Operational Scenario

The analysis in this project is based on routine logistics data reported by health facilities as part of a malaria commodity supply chain management system.

Health facilities submit monthly inventory and consumption reports describing the use and stock status of malaria-related commodities. These reports must be submitted **no later than the 10th day of the following month**. Reports submitted after this deadline are considered late submissions, which may affect the timeliness and quality of supply chain monitoring.

Each report, also referred to as a requisition, contains product-level inventory information for malaria commodities managed by the facility. The report includes several key inventory variables such as the beginning balance, quantity received during the reporting period, quantity dispensed to patients, stock on hand at the end of the month, and the quantity requested for resupply. A requisition contains one record per product, meaning that the same product cannot appear multiple times in a report. In addition, each facility can submit only one requisition per reporting period, ensuring the uniqueness of facility–month observations in the dataset.

The commodities reported in the system correspond to three main categories of malaria interventions. Medicines are used for the **treatment** of malaria cases, rapid diagnostic tests (RDTs) are used for **diagnosis**, and insecticide-treated nets (ITNs) are used for **prevention**. Together, these products represent the core commodities required for malaria case management and prevention programs.

Although facilities submit reports every month, regular resupply orders are only expected during four specific months of the year: February, May, August, and November. These months correspond to the quarterly ordering cycle used by the supply chain system. During the other months, facilities continue submitting consumption reports but do not necessarily place a routine order.

When placing an order, facilities are expected to request quantities that will raise their inventory to a maximum stock level equivalent to five months of consumption. This maximum level is defined as three months of expected consumption for the upcoming quarter plus two additional months of buffer stock intended to protect against supply disruptions.

The recommended order quantity is calculated using the following formula:

```
Order Quantity = (Average Monthly Consumption × 5) − Stock on Hand
```

The **Average Monthly Consumption (AMC)** is computed as the average quantity dispensed during the three most recent consecutive months, including the current reporting month.

However, adjustments are made during two specific ordering periods: May and November. These months correspond to periods preceding the high malaria transmission season, when commodity consumption typically increases. To account for this seasonal variation, order quantities may be adjusted based on historical consumption patterns observed during the same period in the previous year. This seasonal adjustment helps ensure that facilities are adequately stocked to meet the expected increase in demand.
This operational context explains the structure of the dataset used in this study and provides the foundation for the analytical work performed in this repository, including **order quantity prediction and evaluation of stock adequacy policies**.

## Repository Structure

```
data_analytic_project/
│
├── README.md
│
├── data_extraction/
|
├── order_prediction/
│
├── max_stock_test/
```

Each subdirectory contains a complete analytical project including code, methodology, and results.

> [!NOTE]
> In the real case scenario, before conducting the analytical and modeling work, the required data must be extracted from the operational database or system. The [data_extraction](data_extraction/README.md) sub-repository show the process of data extraction.
>
> ---
>
> For every type of analysis there is a need a preliminary inspection of the data in order to understand key data variable descriptions and ensure the information provided is suitable for generating clear and meaningfull insights [data_cleaning](data_cleaning/README.md) sub-repository show the process of data extraction.

---

# Project 1 – Requested vs Approved Quantity Analysis

📁 Directory: **approval_quantity_test/**

## Objective

This project analyzes whether the **quantities of malaria commodities requested by health facilities differ significantly from the quantities approved at the national level**.

In many public health supply chains, facilities submit requisitions based on their reported consumption and stock status. However, the quantities approved during the national validation process differ due to factors such as stock availability and lack of respect of directive shared to the facilities.

The goal is to statistically test whether maintaining a **the quantity requested by facilities** significantly reduce the amount of time taken by the national level to review and approve the orders.

## Analytical Question

Hypothesis tested:

**H₀ (Null Hypothesis)**  
There is **no significant difference** between the quantities requested by facilities and the quantities approved at the national level.

**H₁ (Alternative Hypothesis)**  
There **is a significant difference** between the quantities requested by facilities and the quantities approved at the national level.

➡️ See full project:  
[approval_quantity_test](approval_quantity_test/README.md)

# Project 2 – Order Quantity Prediction

📁 Directory: **order_prediction/**

## Objective

The objective of this project is to **build a predictive model that estimates the quantity of health products facilities should order**, based on historical consumption data.

Accurate order predictions help reduce:

- stock-outs
- overstocking
- emergency orders
- Reduce the time in orders approval
  It provides also clues to use by supply chain analysis to detect potential non regular orders.

➡️ See full project:  
[order_prediction](order_prediction/README.md)

---

# Project 3 – Maximum Stock Level Hypothesis Test

📁 Directory: **max_stock_test/**

## Objective

This project evaluates a key supply chain operation performance question:

**If facilities receive quantities that raise their stock level to a maximum of 5 months of stock, are they less likely to experience stock-outs during the order cycle?**

The goal is to statistically test whether maintaining a **maximum stock level of 5 months** significantly reduces stock-out risk.

## Analytical Question

Hypothesis tested:

**H₀ (Null Hypothesis)**  
Facilities supplied up to 5 months of stock are **not less likely** to experience stock-outs.

**H₁ (Alternative Hypothesis)**  
Facilities supplied up to 5 months of stock are **less likely** to experience stock-outs.

➡️ See full project:  
[max_stock_test](max_stock_test/README.md)

---

# Data dictionnary

The dataset used in this repository is a synthetic dataset generated using a statistical generative model trained on the structure of the original operational data. The synthetic dataset preserves the statistical properties and relationships of the original data while ensuring that no real facility or operational record can be reconstructed.

The dataset contains:
x rows – each row represents a different requisition
xx columns

| Table                           | Description                                                                          |
| ------------------------------- | ------------------------------------------------------------------------------------ |
| `product_code`                  | Product code                                                                         |
| `product_primaryname`           | Product name                                                                         |
| `processing_periods_id`         | ID of the reporting period                                                           |
| `processing_periods_name`       | Name of the reporting period: mm-yyyy                                                |
| `processing_periods_start_date` | Start of the reporting period. Begining of the month                                 |
| `processing_periods_end_date`   | End of the reporting period                                                          |
| `facility_type_name`            | Type of the reporting facility                                                       |
| `facility_code`                 | Code of the reporting facility                                                       |
| `beginningbalance`              | stock of the product at the beginning of the month or reporting period               |
| `quantityreceived`              | Quantity received during the resupply or it should be equal to the quantity approved |
| `quantitydispensed`             | Quantity of product used in the facilities or to the patient                         |
| `stockinhand`                   | Usable stock available at the facility                                               |
| `quantityrequested`             | Quantity of product requested by the facility based on their need and the directive  |
| `reasonforrequestedquantity`    | Raison for requesting a quantity different the directive                             |
| `quantityapproved`              | Quantity of product approved at the national level                                   |
| `remarks`                       | Comment on quantity approved if major change that require justification              |
| `totallossesandadjustments`     | Movement of product other than dispensation: losses and adjustments                  |
| `amc`                           | Average Monthly consumption                                                          |
| `packsize`                      | Number of items (dispense unit) in a pack                                            |
| `skipped`                       | If true the requisition line should be ignore. Not submitted                         |
| `req_id`                        | id of the requisition                                                                |
| `req_status`                    | Status of the requisition. Submitted and Approved are requisition to process         |
| `req_line_id`                   | ID of each item of the requisition (each product)                                    |
| `zone_id`                       | ID of the district where the facility is located                                     |
| `zone`                          | District where the facility is located                                               |
| `dispensingunit`                | Smallest unit give to patient in the prescription                                    |

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
