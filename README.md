# 🛒 E-Commerce Dynamic Price & Catalog ETL Pipeline

Canlı bir REST API kaynağından ürün, kategori, stok ve fiyat verilerini otomatik olarak çeken; veriyi temizleyip dönüştürdükten sonra MS SQL Server üzerinde kurumsal **Staging $\rightarrow$ Data Warehouse (DWH)** mimarisinde modelleyen uçtan uca veri mühendisliği ve ETL boru hattıdır.

---

## 📌 Proje Kapsamı ve Yapılan İşlemler

Bu projede, analitik sistemlerin ihtiyaç duyduğu canlı veri akışını sağlamak amacıyla dış dünyadan dinamik olarak beslenen 3 katmanlı bir veri ambarı altyapısı inşa edilmiştir:

1. **Extract (API Veri Çekme & Sayfalama):**
   * REST API üzerinden ürün verileri `limit` ve `skip` parametreleriyle dinamik olarak sayfalara bölünerek (pagination) çekilmiştir.
   * API oturum yönetimi (`requests.Session`) ve hata kontrolü (`raise_for_status`) uygulanarak veri akışının kesintisizliği sağlanmıştır.

2. **Transform (Veri Temizleme & İş Mantığı):**
   * Ham JSON verisi Pandas kütüphanesiyle düzleştirilerek ilişkisel tablo formatına getirilmiştir.
   * Eksik ve `NULL` değerler iş mantığına uygun varsayılan etiketlerle yönetilmiştir.
   * Liste fiyatı ve yüzde indirim oranı üzerinden nihai satış fiyatı hesaplanarak yeni bir metrik sütun oluşturulmuştur:  
     $$\text{final\_price} = \text{base\_price} \times \left(1 - \frac{\text{discount\_percentage}}{100}\right)$$
   * SQL Server veri tiplerine uyum için tip zorlama (type casting) adımları uygulanmıştır.

3. **Load & Orchestration (Staging Katmanı):**
   * Temizlenen veri seti, SQLAlchemy motoru kullanılarak `stg_products` geçici tablosuna dökülmüştür.
   * Boru hattı her çalıştığında önce staging tablosunu temizleyip (TRUNCATE) ardından yeni yüklemeyi yaparak veri kirliliğini önleyecek şekilde kurgulanmıştır.

4. **T-SQL Artımlı Yükleme (MERGE & UPSERT):**
   * Staging tablosundaki verileri kalıcı ambar tablolarına aktarmak için T-SQL tabanlı bir Stored Procedure (`sp_merge_product_data`) yazılmıştır.
   * **Boyut Tablosu (`dim_products`):** Sistemde olmayan yeni ürünler eklenmiş; başlık, marka veya kategori bilgisi değişen mevcut ürünler ise güncellenmiştir (SCD Type 1). Böylece ürün kataloğunda mükerrer kayıt oluşması engellenmiştir.
   * **Hareket Tablosu (`fact_product_price_history`):** Ürünün o anki fiyatı, stok miktarı ve puanı zaman damgasıyla (`recorded_at`) kaydedilerek zaman serisi fiyat takibine hazır hale getirilmiştir.

---

## 🏗️ Mimari Akış Şeması

```text
[REST API Kaynağı]
        │ (HTTP GET / Pagination)
        ▼
[Python ETL Katmanı]
  ├── extract.py   --> API'den sayfalı ham JSON çekme
  ├── transform.py --> Null yönetimi, tip dönüşümü ve nihai fiyat hesabı
  └── load.py      --> SQLAlchemy ile Staging tablosuna aktarım
        │
        ▼
[MS SQL Server (ECommerce_DWH)]
  ├── stg_products (Geçici ara tablo / Her işlemde truncate edilir)
  └── sp_merge_product_data (Stored Procedure)
        ├── dim_products (Tekil ürün kataloğu - UPSERT)
        └── fact_product_price_history (Tarihsel fiyat ve stok hareketleri)