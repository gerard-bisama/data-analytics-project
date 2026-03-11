# Data Extraction from the source (System)

## Data Source

The data used in this analysis is stored in a **PostgreSQL relational database** from the openLMIS V2 System.

The database contains operational data from a logistics management information system (LMIS), including information on:

- health facilities
- health products
- requisitions and resupply orders
- reporting periods
- stock levels and consumption
- program classifications
  The analysis is based on transactional data related to **requisition submissions and stock management at health facilities**.

---

## Database Structure Overview

The relevant data is distributed across multiple tables, including:
| Table | Description |
|------|-------------|
| `requisitions` | Header table for facility resupply reports |
| `requisition_line_items` | Detailed product-level information for each requisition |
| `products` | Product master data |
| `programs` | Health program classification |
| `program_products` | Mapping between products and programs |
| `facilities` | Health facility registry |
| `facility_types` | Facility classification |
| `geographic_zones` | Regional or administrative zones |
| `processing_periods` | Reporting periods |
| `processing_schedules` | Reporting schedules |
| `product_forms` | Pharmaceutical form classification |
| `dosage_units` | Product dosage unit classification |

Because the analysis requires information from multiple tables, a **database view** was created to simplify data extraction.
To view the ERD diagram for more details here is the ![schema](images/database_diag.png)

```SQL
CREATE OR REPLACE VIEW public.vw_requisition_detail_with_raison AS
SELECT programs.id AS program_id,
  programs.name AS program_name,
  products.id AS product_id,
  products.code AS product_code,
  products.primaryname AS product_primaryname,
  products.description AS product_description,
  products.tracer AS indicator_product,
  processing_periods.id AS processing_periods_id,
  processing_periods.name AS processing_periods_name,
  processing_periods.startdate AS processing_periods_start_date,
  processing_periods.enddate AS processing_periods_end_date,
  processing_periods.scheduleid AS processing_schedules_id,
  facility_types.id AS facility_type_id,
  facility_types.name AS facility_type_name,
  facilities.code AS facility_code,
  facilities.name AS facility_name,
  requisition_line_items.productcode,
  requisition_line_items.product,
  requisition_line_items.beginningbalance,
  requisition_line_items.quantityreceived,
  requisition_line_items.quantitydispensed,
  requisition_line_items.stockinhand,
  requisition_line_items.quantityrequested,
  requisition_line_items.reasonforrequestedquantity,
  requisition_line_items.calculatedorderquantity,
  requisition_line_items.quantityapproved,
  requisition_line_items.totallossesandadjustments,
  requisition_line_items.newpatientcount,
  requisition_line_items.stockoutdays,
  requisition_line_items.normalizedconsumption,
  requisition_line_items.amc,
  requisition_line_items.maxmonthsofstock,
  requisition_line_items.maxstockquantity,
  requisition_line_items.packstoship,
  requisition_line_items.packsize,
  requisition_line_items.fullsupply,
  requisition_line_items.skipped,
  facilities.id AS facility_id,
  requisitions.id AS req_id,
  requisitions.status AS req_status,
  requisition_line_items.id AS req_line_id,
  geographic_zones.id AS zone_id,
  geographic_zones.name AS region,
  facility_types.nominalmaxmonth,
  facility_types.nominaleop,
  dosage_units.code AS du_code,
  product_forms.code AS pf_code,
  products.dispensingunit,
  program_products.productcategoryid AS categoryid,
  products.productgroupid,
  processing_periods.scheduleid,
  requisitions.emergency
FROM ((((((((((((requisition_line_items
  JOIN requisitions ON ((requisition_line_items.rnrid = requisitions.id)))
  JOIN products ON (((requisition_line_items.productcode)
::text =
(products.code)::text)))
     JOIN programs ON
((requisitions.programid = programs.id)))
     JOIN program_products ON
(((products.id = program_products.productid) AND
(program_products.programid = programs.id))))
     JOIN processing_periods ON
((requisitions.periodid = processing_periods.id)))
     JOIN product_categories ON
((program_products.productcategoryid = product_categories.id)))
     JOIN processing_schedules ON
((processing_periods.scheduleid = processing_schedules.id)))
     JOIN facilities ON
((requisitions.facilityid = facilities.id)))
     JOIN facility_types ON
((facilities.typeid = facility_types.id)))
     JOIN geographic_zones ON
((facilities.geographiczoneid = geographic_zones.id)))
     JOIN product_forms ON
((products.formid = product_forms.id)))
     JOIN dosage_units ON
((products.dosageunitid = dosage_units.id)));
```

public.vw_requisition_detail_with_raison was created.
This view consolidates requisition data across multiple relational tables into a single dataset suitable for analytical processing.

The view includes information such as:

- program identifiers
- facility identifiers
- product attributes
- reporting period information
- stock levels
- quantities requested and approved
- consumption indicators
- stock-out indicators
- product classification

## This approach simplifies data extraction by avoiding repeated complex joins during analysis.

## Batch Data Extraction Strategy

Because the database contains a large volume of operational data, extraction is performed **in batches** to avoid excessive load on the production database.

The extraction strategy is based on **reporting periods**.

Each extraction retrieves data corresponding to **four months of reporting periods**.

Batch size = 4 months
The number of extraction batches is calculated as:
Number of batches = Total number of months / 4

Example:
If the dataset contains **22 months** of reporting periods:
22 / 4 = 5.5 → 6 batches
Therefore, data will be extracted in **6 batches of 4 months each**.

---

## Extraction Query

The following SQL query is used to extract data from the analytical view for a given batch.

Example query:

```sql
SELECT *
FROM vw_requisition_detail_with_raison
WHERE processing_periods_id IN (
    SELECT id
    FROM processing_periods
    WHERE startdate::date >= '2023-12-01'
    ORDER BY startdate
    LIMIT 4 OFFSET 0
);
```

### Query Logic

The query works as follows:

- Select the first 4 reporting periods starting from a given start date.
- Use LIMIT 4 to restrict the extraction to four reporting periods.
- Use OFFSET to move to the next batch of reporting periods.

Example for batch 3: `SQL LIMIT 4 OFFSET 8`

### Advantages of Batch Extraction

This approach provides several advantages:

- Prevents heavy load on the production database
- Reduces query execution time
- Allows controlled extraction of large datasets
- Improves reproducibility of data pipelines

## Data Export

Each batch can be exported to a file format suitable for analysis, such as CSV

These datasets are then used in downstream analytical workflows :

- exploratory data analysis
- predictive modeling
- statistical hypothesis testing
