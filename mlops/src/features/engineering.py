import numpy as np
import pandas as pd

from sklearn.base import (
    BaseEstimator,
    TransformerMixin,
)

PRODUCT_GROUP_MAPPING = {
    "ACT-INF": "ACT",
    "ACT-SC": "ACT",
    "ACT-GC": "ACT",
    "ACT-AD": "ACT",
    "PYRA-COMP": "PYRA",
    "PYRA-SAC": "PYRA",
    "ART-INJ": "ART",
    "ART-SUP": "ART",
    "QUIN": "SP",
    "SP": "SP",
    "ITN": "PREV",
    "RDT": "DIAG",
}


FACILITY_TYPE_MAPPING = {
    "DISTRICT HOSPITAL": "HOSPITAL",
    "REGIONAL HOSPITAL": "HOSPITAL",
    "NATIONAL HOSPITAL": "HOSPITAL",
    "HEALTH CENTER": "HEALTH CENTER",
}

ZONE_TYPE_MAPPING = {
    'DISTRICT1': 'RURAL',
    'DISTRICT2': 'RURAL',
    'DISTRICT3': 'URBAN',
    'DISTRICT4': 'RURAL',
    'DISTRICT5': 'RURAL',
    'DISTRICT6': 'RURAL',
    'DISTRICT7': 'URBAN',
    'DISTRICT8': 'RURAL',
    'DISTRICT9': 'RURAL',
    'DISTRICT10': 'RURAL',
    'DISTRICT11': 'RURAL',
    'DISTRICT12': 'RURAL',
    'DISTRICT13': 'RURAL',
    'DISTRICT14': 'RURAL',
    'DISTRICT15': 'URBAN',
    'DISTRICT16': 'RURAL',
    'DISTRICT17': 'RURAL',
    'DISTRICT18': 'RURAL',
    'DISTRICT19': 'RURAL',
    'DISTRICT20': 'URBAN',
    'DISTRICT21': 'RURAL',
    'DISTRICT22': 'RURAL',
    'DISTRICT23': 'RURAL',
    'DISTRICT24': 'RURAL',
    'DISTRICT25': 'URBAN',
    'DISTRICT26': 'RURAL',
    'DISTRICT27': 'URBAN',
    'DISTRICT28': 'URBAN',
    'DISTRICT29': 'URBAN',
    'DISTRICT30': 'RURAL',
    'DISTRICT31': 'URBAN',
    'DISTRICT32': 'RURAL',
    'DISTRICT33': 'RURAL',
    'DISTRICT34': 'RURAL',
    'DISTRICT35': 'RURAL',
    'DISTRICT36': 'RURAL',
    'DISTRICT37': 'URBAN',
    'DISTRICT38': 'RURAL'
}

#FILTER_MONTHS = ['February','May','August','November']

MODEL_FEATURES = [
    "product_group",
    "facility_type",
    "reporting_month",
    "zone_type",
    "High_Transmission_Preparation",
    "stock_status",
    "beginning_balance",
    "quantity_received",
    "quantity_dispensed",
    "total_losses_and_adjustments",
    "stock_in_hand",
    "months_of_stock",
    "amc",
]


class SupplyChainFeatureEngineer (BaseEstimator,TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        X = X.copy()

        # ---------------------------
        # Reporting period | Moved to cleaning.py 
        # ---------------------------

        X["processing_periods_name"] = pd.to_datetime(
            X["processing_periods_name"],format="mixed",errors="coerce"
        )

        X["reporting_month"] = (
            X["processing_periods_name"]
            .dt
           .month_name()
        )
        #X = X[X['reporting_month'].isin(FILTER_MONTHS)]

        # ---------------------------
        # Transmission preparation
        # ---------------------------

        X["High_Transmission_Preparation"] = np.where(
            X["reporting_month"].isin(
                ["May", "August"]
            ),
            "YES",
            "NO",
        )

        # ---------------------------
        # Facility grouping
        # ---------------------------

        X["facility_type"] = (
            X["facility_type_name"]
            .map(FACILITY_TYPE_MAPPING)
        )
        # ---------------------------
        # Zone_type grouping
        # ---------------------------

        X["zone_type"] = (
            X["zone"]
            .map(ZONE_TYPE_MAPPING)
        )

        # ---------------------------
        # Product grouping
        # ---------------------------

        X["product_group"] = (
            X["product_primary_name"]
            .map(PRODUCT_GROUP_MAPPING)
        )

        # ---------------------------
        # Months of Stock
        # ---------------------------

        X["months_of_stock"] = np.divide(
            X["stock_in_hand"],
            X["amc"],
            out=np.full(
                len(X),
                np.nan,
                dtype=float
            ),
            where=X["amc"].ne(0)
        ).round(1)

        # ---------------------------
        # Stock status
        # ---------------------------

        mos = X["months_of_stock"]

        conditions = [
            mos.eq(0),
            mos.gt(0) & mos.le(1),
            mos.gt(1) & mos.lt(3),
            mos.ge(3) & mos.le(5),
            mos.gt(5),
        ]

        choices = [
            "Stockout",
            "Critical",
            "Low",
            "Adequate",
            "Overstock",
        ]

        X["stock_status"] = np.select(
            conditions,
            choices,
            default="Unknown"
        )

        return X

class ModelFeatureSelector (BaseEstimator,TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):

        return X[
            MODEL_FEATURES
        ].copy()
    
