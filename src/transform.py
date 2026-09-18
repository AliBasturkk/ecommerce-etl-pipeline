import pandas as pd
import logging
from typing import List, Dict, Any

def transform_products_data(raw_products: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Ham JSON ürün verilerini temizler, indirimli fiyatı hesaplar ve stg_products şemasına hazırlar.
    """
    if not raw_products:
        logging.warning("Dönüştürülecek veri bulunamadı!")
        return pd.DataFrame()

    df = pd.DataFrame(raw_products)

    # 1. Gerekli sütunları seç ve yeniden adlandır
    column_mapping = {
        "id": "source_product_id",
        "title": "product_title",
        "category": "category",
        "brand": "brand",
        "price": "base_price",
        "discountPercentage": "discount_percentage",
        "stock": "stock_quantity",
        "rating": "rating"
    }
    
    df = df[list(column_mapping.keys())].rename(columns=column_mapping)

    # 2. Eksik veya Null değerleri yönet
    df["brand"] = df["brand"].fillna("Generic")
    df["category"] = df["category"].fillna("Uncategorized")
    df["stock_quantity"] = df["stock_quantity"].fillna(0).astype(int)

    # 3. İndirimli Nihai Fiyat Hesaplaması (Business Logic)
    # final_price = base_price * (1 - (discount_percentage / 100))
    df["final_price"] = (
        df["base_price"] * (1 - (df["discount_percentage"] / 100.0))
    ).round(2)

    # 4. Veri tiplerini zorla (Data Type Casting)
    df["source_product_id"] = df["source_product_id"].astype(int)
    df["base_price"] = df["base_price"].astype(float).round(2)
    df["discount_percentage"] = df["discount_percentage"].astype(float).round(2)
    df["rating"] = df["rating"].astype(float).round(2)

    logging.info(f"Transform tamamlandı. İşlenen satır sayısı: {len(df)}")
    return df