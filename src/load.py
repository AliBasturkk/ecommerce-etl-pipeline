import pandas as pd
import logging
from sqlalchemy import text
from config.db_config import get_db_engine

def load_staging_and_merge(df: pd.DataFrame) -> None:
    """
    Veriyi stg_products tablosuna yükler ve sp_merge_product_data prosedürünü tetikler.
    """
    if df.empty:
        logging.warning("Yüklenecek veri bulunamadı.")
        return

    engine = get_db_engine()
    
    with engine.begin() as conn:
        # 1. Staging tablosunu temizle
        logging.info("stg_products tablosu truncate ediliyor...")
        conn.execute(text("TRUNCATE TABLE dbo.stg_products;"))

        # 2. Temizlenen veriyi staging tablosuna yaz
        logging.info("Veri stg_products tablosuna basılıyor...")
        df.to_sql("stg_products", con=conn, if_exists="append", index=False)

        # 3. T-SQL MERGE Stored Procedure'ünü çalıştır
        logging.info("sp_merge_product_data tetikleniyor...")
        conn.execute(text("EXEC dbo.sp_merge_product_data;"))

    logging.info("Load ve MERGE işlemi başarıyla tamamlandı.")