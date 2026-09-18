import requests
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_URL = "https://dummyjson.com/products"

def fetch_all_products(batch_size: int = 50) -> List[Dict[str, Any]]:
    """
    DummyJSON API üzerinden tüm ürün kayıtlarını sayfalı (pagination) olarak çeker.
    """
    all_products = []
    skip = 0
    
    with requests.Session() as session:
        while True:
            url = f"{BASE_URL}?limit={batch_size}&skip={skip}"
            try:
                logging.info(f"API isteği atılıyor: limit={batch_size}, skip={skip}")
                response = session.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                products = data.get("products", [])
                if not products:
                    break
                
                all_products.extend(products)
                total = data.get("total", 0)
                skip += batch_size
                
                if skip >= total:
                    break
                    
            except requests.exceptions.RequestException as error:
                logging.error(f"API isteği sırasında hata oluştu: {error}")
                raise
                
    logging.info(f"Extract tamamlandı. Toplam çekilen kayıt: {len(all_products)}")
    return all_products