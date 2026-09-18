import logging
from src.extract import fetch_all_products
from src.transform import transform_products_data
from src.load import load_staging_and_merge

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_pipeline():
    logging.info("=== ETL Boru Hattı Başlatıldı ===")
    
    # 1. Extract
    raw_data = fetch_all_products(batch_size=50)
    
    # 2. Transform
    transformed_df = transform_products_data(raw_data)
    
    # 3. Load
    load_staging_and_merge(transformed_df)
    
    logging.info("=== ETL Boru Hattı Başarıyla Tamamlandı ===")

if __name__ == "__main__":
    run_pipeline()