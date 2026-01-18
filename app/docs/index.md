# Table: serve.outbound_with_dn
  
## Business Purpose
This table provides a unified and detailed record of outbound delivery notes and their associated shipment, invoicing, customer, and status information.  
Each column contains valuable business data that can be used for a wide range of queries — not only shipment tracking or POD lookup but also analytical, financial, and operational questions such as:

- Track a shipment or delivery note by its number or customer name  
- Check when an order was shipped, invoiced, or notified  
- Retrieve customer contact details or consignee address for delivery   
- Retrieve POD (proof-of-delivery) document for confirmation  

In other words, **every column is queryable**, and the table is specifically designed to support rich and multidimensional data queries.

---

## Column Dictionary (detailed explanations)

### delivery_note_number
The unique identifier for each delivery note (DN). It acts as the primary reference key for outbound orders. Each DN corresponds to a unique and specific shipment. Example: `5A9125A1H1`.
### tracking_number
The tracking number assigned by the courier company. Used to trace the shipment through the logistics provider’s system (e.g., DHL). Example: `JJD014600007380411876`.
### delivery_note_status
The current or final logistics status of the delivery note (DN). This field reflects the exact stage of the shipment within the outbound logistics process. Example: `Delivered`.
### invoice_number
The commercial invoice associated with the delivery note, usually indicating the financial transaction reference. Example: `6A9SMS25A012`.
### customer_parent_name
The name of the parent customer organization that owns or manages the business relationship for this delivery note. Example: `SAIC MOTOR ESPAÑA, S.L.`.
### customer_branch_name
The specific branch, subsidiary, or operational unit of the parent customer that is associated with this delivery note. Example: `Autoconsa S.L.`.
### customer_number
The internal customer identifier used in the ERP or order management system. This field uniquely identifies the customer entity from a system perspective. Example: `420012`
### order_type
The business type of the order, describing how it was created or processed (e.g., Regular, Return, Replacement). Example: `Regular`.
### destination_country
The destination country of the shipment in human-readable form. Example: `Spain`, `Portugal`.
### destination_city
The destination city where the shipment is delivered. Example: `Szolnok`.
### unique_lines
The count of distinct line items contained in the delivery note (each line typically represents a product SKU). Example: `2`.
### total_delivery_note_qty
The total quantity of goods in this delivery note (summed over all unique lines). Represents the shipped quantity. Example: `2`.
### total_picklist_qty
The total quantity recorded in the corresponding packing list (PKL). Example: `2`.
### total_net_amount
The total net monetary amount (excluding VAT) associated with this delivery note. Typically expressed in the company’s accounting currency. Example: `159`.
### total_vat_amount 
The total VAT amount charged on this delivery note. Example: `0`.
### total_amount_including_tax
The total monetary amount of the delivery note including all applicable taxes (e.g., VAT). This value represents the final gross amount charged to the customer for this delivery note. Example: `1620.48`.
### total_net_weight_actual
The actual total net weight of the shipped goods, excluding packaging materials. This field reflects the real measured weight of the products. Example: `0.01`.
### total_gross_weight_actual
The actual total gross weight of the shipment, including products and packaging. This value is typically used by carriers for transportation planning and cost calculation. Example: `0.01`.
### total_cbm_actual
The total cubic meter (CBM) measurement of the goods in this DN, representing shipment volume for logistics calculations. Example: `0.01`.
### incoterm
The trade term (e.g., DDP, CIF, FOB) describing shipping responsibility and cost allocation between buyer and seller. Example: `DDP,Amsterdam`.
### delivered_time_actual
The timestamp when the shipment was successfully delivered to the consignee. Example: `2025-11-05 10:51:00`.
### shipped_time_actual
The timestamp when the goods were physically shipped or dispatched from the warehouse. Example: `2025-10-08 16:28:29`.
### invoice_issued_time
The timestamp when the invoice document was officially generated. Example: `2025-10-08 18:22:37`.
### picklist_time
The time when the packing list (PKL) was created or finalized, representing when items were prepared for shipment. Example: `2025-10-08 13:45:35`.
### notified_time
The time when the consignee or carrier was notified of the upcoming shipment. Example: `2025-10-07 14:02:39`.
### created_time
The system creation timestamp for the delivery note record. It reflects when the DN was first generated in the system. Example: `2025-10-07 14:00:02`.
### last_updated_time
The timestamp of the most recent data update for this record (e.g., from logistics or ERP integration). Example: `2025-10-08 18:22:48`.
### pod_document
The proof-of-delivery (POD) link providing official confirmation of delivery (e.g., scanned signature or photo). Example: a Google Drive or carrier URL.
### [Distributor Code]
The code identifying the distributor or reseller associated with the order. Example: `430018`.
### consignee_person_name
Additional consignee information line; holds a contact person’s name. Example: `Carlos Herrero`.
### consignee_company_name
Primary consignee company name. Example: `Autoconsa S.L.`.
### address_street
The street address of the consignee or delivery location. Example: `CRTA ADANERO GIJON KM 194 ZARATAN`.
### postal_code
The postal or ZIP code for the consignee address. Example: `47610`.
### country_code 
The ISO-3166 three-letter country code for the consignee address. Example: `ESP`, `PRT`.
### contact_number
The phone number of the consignee or responsible contact person. Example: `983 34 12 11`.
### contact_email
The email address for the consignee contact. Example: `carlos.herrero@autocyl.es`.
### [Last Update At]
The system time when this entire record was last updated (audit trail timestamp). Example: `2025-10-14 12:27:32`.

## Notes

- Column names use **snake_case** and must be referenced exactly as shown.
- The primary lookup key is `delivery_note_number`.

---

## Example Queries (PostgreSQL)

### Example 1: Retrieve recent delivery notes for a specific customer
```sql
SELECT
  delivery_note_number,
  customer_parent_name,
  destination_country,
  shipped_time_actual,
  delivery_note_status,
  pod_document
FROM serve.outbound_with_dn
WHERE customer_parent_name = 'SAIC MOTOR ESPAÑA, S.L.'
ORDER BY shipped_time_actual DESC
LIMIT 20;
```