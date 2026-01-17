# Table: serve.outbound_with_dn
  
## Business Purpose
This table provides a unified and detailed record of outbound delivery notes and their associated shipment, invoicing, customer, and status information.  
Each column contains valuable business data that can be used for a wide range of queries — not only shipment tracking or POD lookup but also analytical, financial, and operational questions such as:

- Track a shipment or delivery note by its number or customer name  
- Check when an order was shipped, invoiced, or notified  
- Retrieve customer contact details or consignee address for delivery  
- Compare planned vs actual shipping times or countries  
- Calculate aggregated metrics such as total quantities, monetary amounts, or VAT totals  
- Retrieve POD (proof-of-delivery) links for confirmation  
- Inspect the last known logistics status and timestamp for each delivery note  
- Cross-check delivery performance, country-level shipping statistics, or incoterm distributions  

In other words, **every column is queryable**, and the table is specifically designed to support rich and multidimensional data queries.

---

## Column Dictionary (detailed explanations)

### Column Name: [Delivery Note Number] 
Description: The unique identifier for each delivery note (DN). It acts as the primary reference key for outbound orders. Each DN corresponds to a unique and specific shipment. Example: `5A9125A1H1`.
### Column Name: [Tracking Number]
Description: The tracking number assigned by the courier company. Used to trace the shipment through the logistics provider’s system (e.g., DHL). Example: `JJD014600007380411876`.
### [Invoice Number]
The commercial invoice associated with the delivery note, usually indicating the financial transaction reference. Example: `6A9SMS25A012`.
### [Customer Name]
The name of the end customer or receiving company for this shipment. Example: `SAIC MOTOR ESPAÑA, S.L.`.
### [Source Customer]
The upstream sender or distributor responsible for creating the outbound order. Often an internal or regional distribution partner. Example: `Autoconsa S.L.`.
### [Order Type]
The business type of the order, describing how it was created or processed (e.g., Regular, Return, Replacement). Example: `Regular`.
### [Destination Country]
The destination country of the shipment in human-readable form. Example: `Spain`, `Portugal`.
### [Unique Lines]
The count of distinct line items contained in the delivery note (each line typically represents a product SKU). Example: `2`.
### [Total DN QTY]
The total quantity of goods in this delivery note (summed over all unique lines). Represents the shipped quantity. Example: `2`.
### [Total PKL QTY]
The total quantity recorded in the corresponding packing list (PKL). Example: `2`.
### [Total Net Amount]
The total net monetary amount (excluding VAT) associated with this delivery note. Typically expressed in the company’s accounting currency. Example: `159`.
### [Total Vat Amount] 
The total VAT amount charged on this delivery note. Example: `0`.
### [Total CBM(A)]
The total cubic meter (CBM) measurement of the goods in this DN, representing shipment volume for logistics calculations. Example: `0.01`.
### [Incoterm]
The trade term (e.g., DDP, CIF, FOB) describing shipping responsibility and cost allocation between buyer and seller. Example: `DDP,Amsterdam`.
### [Shipped Time(A)]
The timestamp when the goods were physically shipped or dispatched from the warehouse. Example: `2025-10-08 16:28:29`.
### [Invoice Time]
The timestamp when the invoice document was officially generated. Example: `2025-10-08 18:22:37`.
### [PKL Time] 
The time when the packing list (PKL) was created or finalized, representing when items were prepared for shipment. Example: `2025-10-08 13:45:35`.
### [Notified Time]
The time when the consignee or carrier was notified of the upcoming shipment. Example: `2025-10-07 14:02:39`.
### [Create Time]
The system creation timestamp for the delivery note record. It reflects when the DN was first generated in the system. Example: `2025-10-07 14:00:02`.
### [Last Update Time]
The timestamp of the most recent data update for this record (e.g., from logistics or ERP integration). Example: `2025-10-08 18:22:48`.
### [Last Status]
The current or final delivery status of the DN, reflecting its most up-to-date logistics state. Common values: `delivered`, `transit`, `failure`. Example: `delivered`.
### [Last Status Time] 
The timestamp corresponding to when the last known status was recorded. Example: `2025-10-14 14:40:00`.
### [POD Link]
The proof-of-delivery (POD) link providing official confirmation of delivery (e.g., scanned signature or photo). Example: a Google Drive or carrier URL.
### [Distributor Code]
The code identifying the distributor or reseller associated with the order. Example: `430018`.
### [Consignee Info Line 2]
Additional consignee (recipient) information line; usually holds a contact person’s name. Example: `Carlos Herrero`.
### [Consignee Info Line 1]
Primary consignee company name or contact label. Example: `Autoconsa S.L.`.
### [Address]
The street address of the consignee or delivery location. Example: `CRTA ADANERO GIJON KM 194 ZARATAN`.
### [Postal Code]
The postal or ZIP code for the consignee address. Example: `47610`.
### [City Name]
The city or locality name of the consignee’s address. Example: `Valladolid`.
### [Country Code] 
The ISO-3166 three-letter country code for the consignee address. Example: `ESP`, `PRT`.
### [Contact Phone]
The phone number of the consignee or responsible contact person. Example: `983 34 12 11`.
### [Contact Email]
The email address for the consignee contact. Example: `carlos.herrero@autocyl.es`.
### [Delivery Short Name]
A short or display name for the delivery destination, typically used in dashboards or simplified outputs. Example: `MG LEV MOTOR`.
### [Last Update At]
The system time when this entire record was last updated (audit trail timestamp). Example: `2025-10-14 12:27:32`.

### Notes
- Column names contain spaces; always use square brackets `[ ]` in SQL.
- The primary lookup key is `[Delivery Note Number]`.

---

## Example Query

### Example Query 1: Retrieve key shipment information for a specific customer within a date range

```sql
SELECT TOP (10)
  [Delivery Note Number],
  [Customer Name],
  [Destination Country],
  [Shipped Time(A)],
  [Last Status],
  [Last Status Time],
  [POD Link]
FROM [serve].[outbound_with_dn_lookup]
WHERE [Customer Name] = 'SAIC MOTOR ESPAÑA, S.L.'
  AND [Shipped Time(A)] BETWEEN '2025-10-01' AND '2025-10-10'
ORDER BY [Shipped Time(A)] DESC;
```

### Example Query 2: Retrieve the latest status and timestamp for a specific delivery note

```sql
SELECT
  [Delivery Note Number],
  [Last Status],
  [Last Status Time]
FROM [serve].[outbound_with_dn_lookup]
WHERE [Delivery Note Number] = '5A9125A1H1';
```