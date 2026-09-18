-- Staging Tablosu (Ham verinin Python'dan indiði geçici alan)
IF OBJECT_ID('dbo.stg_products', 'U') IS NOT NULL DROP TABLE dbo.stg_products
CREATE TABLE dbo.stg_products (
    source_product_id INT,
    product_title NVARCHAR(255),
    category NVARCHAR(100),
    brand NVARCHAR(100),
    base_price DECIMAL(18, 2),
    discount_percentage DECIMAL(5, 2),
    final_price DECIMAL(18, 2),
    stock_quantity INT,
    rating DECIMAL(3, 2),
    extracted_at DATETIME DEFAULT GETDATE()
)

-- Dimension Tablosu (Ürün Kataloðu - Tekil Ürün Bilgisi)
IF OBJECT_ID('dbo.dim_products', 'U') IS NOT NULL DROP TABLE dbo.dim_products
CREATE TABLE dbo.dim_products (
    product_sk INT IDENTITY(1,1) PRIMARY KEY,
    source_product_id INT UNIQUE NOT NULL,
    product_title NVARCHAR(255) NOT NULL,
    category NVARCHAR(100),
    brand NVARCHAR(100),
    is_active BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
)

-- Fact Tablosu (Fiyat & Stok Zaman Serisi - Her Fiyat Hareketini Tutar)
IF OBJECT_ID('dbo.fact_product_price_history', 'U') IS NOT NULL DROP TABLE dbo.fact_product_price_history
CREATE TABLE dbo.fact_product_price_history (
    price_history_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    product_sk INT FOREIGN KEY REFERENCES dbo.dim_products(product_sk),
    base_price DECIMAL(18, 2) NOT NULL,
    discount_percentage DECIMAL(5, 2),
    final_price DECIMAL(18, 2) NOT NULL,
    stock_quantity INT,
    rating DECIMAL(3, 2),
    recorded_at DATETIME DEFAULT GETDATE()
)