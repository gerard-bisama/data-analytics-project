import random
import pandas as pd


PRODUCT_GROUPS = [
    "PYRA",
    "ACT",
    "ART",
    "DIAG",
    "PREV",
    "SP"
]

FACILITY_TYPES = [
    "HEALTH CENTER",
    "HOSPITAL"
]

REPORTING_MONTHS = [
    "May",
    "February",
    "August",
    "November"
]

ZONE_TYPES = [
    "URBAN",
    "RURAL"
]


def determine_stock_status(months_of_stock):
    """
    Determine stock status from Months of Stock (MoS).

    Business rules:
        MoS = 0        -> Stockout
        0 < MoS <= 1   -> Critical
        1 < MoS < 3    -> Low
        3 <= MoS <= 5  -> Adequate
        MoS > 5        -> Overstock
        Missing MoS    -> Unknown
    """

    if months_of_stock is None:
        return "Unknown"

    if months_of_stock == 0:
        return "Stockout"

    if 0 < months_of_stock <= 1:
        return "Critical"

    if 1 < months_of_stock < 3:
        return "Low"

    if 3 <= months_of_stock <= 5:
        return "Adequate"

    if months_of_stock > 5:
        return "Overstock"

    return "Unknown"


def generate_sample_data(
    number_of_records=20,
    seed=42
):
    """
    Generate synthetic malaria supply-chain prediction data.

    The seed makes the generated dataset reproducible.
    """

    random.seed(seed)

    data = []

    for i in range(1, number_of_records + 1):

        product_group = random.choice(PRODUCT_GROUPS)
        facility_type = random.choice(FACILITY_TYPES)
        reporting_month = random.choice(REPORTING_MONTHS)
        zone_type = random.choice(ZONE_TYPES)

        # May and August correspond to preparation
        # for high-transmission periods in our model.
        if reporting_month in ["May", "August"]:
            high_transmission_preparation = "YES"
        else:
            high_transmission_preparation = "NO"

        # -----------------------------------------
        # Generate realistic consumption
        # -----------------------------------------

        amc = random.randint(20, 500)

        # Dispensing is related to AMC, but can vary.
        quantity_dispensed = round(
            amc * random.uniform(0.7, 1.3)
        )

        # -----------------------------------------
        # Generate Months of Stock
        # -----------------------------------------

        stock_scenario = random.choice([
            "Stockout",
            "Critical",
            "Low",
            "Adequate",
            "Overstock"
        ])

        if stock_scenario == "Stockout":
            months_of_stock = 0.0

        elif stock_scenario == "Critical":
            months_of_stock = round(
                random.uniform(0.1, 1.0),
                1
            )

        elif stock_scenario == "Low":
            months_of_stock = round(
                random.uniform(1.1, 2.9),
                1
            )

        elif stock_scenario == "Adequate":
            months_of_stock = round(
                random.uniform(3.0, 5.0),
                1
            )

        elif stock_scenario == "Overstock":
            months_of_stock = round(
                random.uniform(5.1, 8.0),
                1
            )

        else:
            months_of_stock = None

        # -----------------------------------------
        # Calculate stock in hand
        #
        # MoS = Stock in Hand / AMC
        # therefore:
        # Stock in Hand = MoS * AMC
        # -----------------------------------------

        if months_of_stock is None:
            stock_in_hand = None
        else:
            stock_in_hand = round(
                months_of_stock * amc
            )

        stock_status = determine_stock_status(
            months_of_stock
        )

        # -----------------------------------------
        # Losses and adjustments
        # -----------------------------------------

        total_losses_and_adjustments = round(
            random.uniform(-0.05, 0.05)
            * quantity_dispensed
        )

        # -----------------------------------------
        # Synthetic predicted order
        #
        # For testing only.
        # Higher need tends to occur when stock
        # coverage is low.
        # -----------------------------------------

        target_stock_months = 5

        if months_of_stock is None:
            estimated_gap = amc * 2
        else:
            estimated_gap = (
                max(
                    target_stock_months
                    - months_of_stock,
                    0
                )
                * amc
            )

        predicted_ordered_quantity = round(
            max(
                0,
                estimated_gap
                * random.uniform(0.85, 12.15)
            ),
            2
        )

        record = {
            "index": f"{product_group}-{i}",
            "product_group": product_group,
            "facility_type": facility_type,
            "reporting_month": reporting_month,
            "zone_type": zone_type,
            "High_Transmission_Preparation":
                high_transmission_preparation,
            "stock_status": stock_status,
            "quantity_dispensed":
                quantity_dispensed,
            "total_losses_and_adjustments":
                total_losses_and_adjustments,
            "stock_in_hand":
                stock_in_hand,
            "months_of_stock":
                months_of_stock,
            "amc":
                amc,
            "predicted_ordered_quantity":
                predicted_ordered_quantity
        }

        data.append(record)

    return data


def generate_sample_dataframe(
    number_of_records=20,
    seed=42
):
    """
    Return generated sample data as a pandas DataFrame.
    """

    data = generate_sample_data(
        number_of_records=number_of_records,
        seed=seed
    )
    #print(data)
    return pd.DataFrame(data)