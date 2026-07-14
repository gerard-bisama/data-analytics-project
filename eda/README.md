# Exploratory Data Analysis

## 📌 Overview

This section presents an exploratory data analysis (EDA) of the malaria supply chain dataset, focusing on inventory patterns across multiple variables of the dataset. The analysis highlights key statistical characteristics such as distribution, variability, and outlier behavior, and links them to underlying supply chain dynamics.
These insights provide a critical foundation for subsequent work, including A/B testing of supply policies and the development of machine learning models aimed at improving demand forecasting, stock optimization, and decision-making within the health supply chain system.
The EDA are organized by project to properly meet every project objective. Thus, 3 EDA will be conducted:

- EDA for Allocation Hypothesis Testing: focus on paired variables, allocation gaps, distributional assumptions, and preparation for the hypotheses test.
- EDA for Demand Forecasting: focus on temporal patterns, seasonality, feature relationships, and predictor selection
- EDA for Stock Policy Evaluation: focus on Months of Stock, stock-out patterns, threshold analysis, and variables needed for evaluating the five-month stock policy

## EDA for Allocation Hypothesis Testing

[EDA_Allocation Hypothesis Testing](eda_test_qty.ipynb)
It focuses on paired variables, allocation gaps, distributional assumptions, and preparation for paired tests.
Here is the exploratory data analysis worklflow for the Hypothesis Testing.
![](../images/EDA_HypoTesting_qtyreqvsapp.png)

### Executive Summary overview

This Exploratory Data Analysis (EDA) was conducted to prepare the dataset for project 1, which aims to determine whether the quantities of malaria commodities requested by health facilities differ significantly from the quantities approved by the national Medical Store.
The EDA focused on understanding the statistical characteristics of the key study variables, identifying potential data quality issues, evaluating the distribution of allocation differences, and assessing whether the assumptions required for hypothesis testing are reasonably satisfied.

Details of the Executive summary can be found on the link [Details Qty requested vs Qty approved ](README_AllocTesting.md)

---
