# Ordered Quantity Prediction Model

## Overview

This project focuses on building a **model capable of predicting the quantity of malaria commodities that will be approved by the central supply chain**, based on facility inventory status, historical consumption, product characteristics, facility characteristics, and seasonal factors.

Rather than directly applying a complex machine-learning algorithm, the project follows a progressive modeling approach, starting with Multiple Linear Regression (MLR) as an interpretable baseline model and subsequently moving toward more advanced machine-learning approaches, including Decision Tree and Random Forest Regression

This approach makes it possible to determine whether increasingly flexible models provide meaningful improvements in predictive performance by capturing non-linear relationships, interactions, and threshold effects that may not be adequately represented by a linear model.

![ML Analysis framework](../images/ML_Analysis_Framework.png)

Accurate and reliable prediction of order quantities can support supply-chain operations by helping to:

- reduce the risk of stock-outs and overstocking;
- reduce the need for emergency orders;
- support faster and more evidence-based order review and approval;
- identify potentially unusual or irregular order quantities requiring additional review;
- provide supply-chain analysts with a quantitative decision-support tool for commodity planning.

## Ordered quantity prediction using the Linear Regresssion

[MLR based model for order prediction](mlr_model.ipynb)
Following the Exploratory Data Analysis and feature-engineering phase, a Multiple Linear Regression (MLR) model was developed as the first predictive model for estimating the quantity of malaria commodities approved by the central supply chain.

### Executive Summary overview

This Multiple Linear Regression (MLR) analysis was conducted as the first modeling stage of Project 2, which aims to develop and evaluate predictive models for estimating malaria commodity quantities approved by the central supply chain.
The analysis uses MLR as an interpretable baseline model to assess the combined linear contribution of inventory, product, facility, geographic, and temporal predictors to quantity_approved. The resulting performance provides a reference benchmark for evaluating whether more flexible models, particularly Decision Tree and Random Forest Regression, can better capture the non-linear relationships and interactions observed in the data.

Details of the Executive summary can be found on the link [Multiple Linear Regression Predictive Model ](README_MLR_model.md)

---

## Ordered Quantity Prediction using Decision Tree and Random Forest Regression

[Decision Tree and Random Forest based model for order prediction](decision_tree_model.ipynb)

Following the Multiple Linear Regression (MLR) baseline model, Decision Tree and Random Forest Regression were developed to assess whether non-linear relationships, interactions, and threshold effects among logistics predictors could improve the prediction of malaria commodity quantities approved by the central supply chain.

### Executive Summary overview

This analysis represents the advanced machine-learning stage of the order prediction project. Decision Tree Regression was first used to identify non-linear and threshold-based relationships between approved quantities and inventory and consumption characteristics. Random Forest Regression was subsequently developed to determine whether combining multiple trees could improve predictive accuracy and generalization. Both models were evaluated against the **MLR baseline using the same test dataset and the same performance metrics: R², MAE, and RMSE**. The analysis also compares predictor importance across the tree-based models to identify the logistics factors providing the strongest predictive information.

Details of the analysis can be found in the [Decision Tree and Random Forest Predictive Model Executive Summary](README_DT_RF_model.md).
