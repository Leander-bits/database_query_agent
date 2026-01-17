from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Set

class Settings(BaseSettings):
    # supabase
    supabase_url:str = Field(..., env="SUPABASE_URL")
    supabase_anon_key:str = Field(..., env="SUPABASE_ANON_KEY")
    # deepseek
    deepseek_api_key:str = Field(..., env="DEEPSEEK_API_KEY")
    deepseek_model:str = Field(..., env="DEEPSEEK_MODEL")
    # prompt
    allowed_columns: Set[str] = {
        "delivery_note_number", "tracking_number", "delivery_note_status", "pod_document",
        "invoice_number", "customer_parent_name", "customer_branch_name", "customer_number",
        "order_type", "destination_country", "country_code", "destination_city",
        "postal_code", "address_street", "consignee_company_name", "consignee_person_name",
        "contact_number", "contact_email", "unique_lines", "total_delivery_note_qty",
        "total_picklist_qty", "total_net_amount", "total_vat_amount", "total_amount_including_tax",
        "total_net_weight_actual", "total_gross_weight_actual", "total_cbm_actual", "incoterm",
        "shipped_time_actual", "delivered_time_actual", "invoice_issued_time", "picklist_time",
        "notified_time", "created_time", "last_updated_time"
    }

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
        
settings = Settings()