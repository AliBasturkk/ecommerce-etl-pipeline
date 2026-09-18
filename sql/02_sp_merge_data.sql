CREATE OR ALTER PROCEDURE dbo.sp_merge_product_data
AS
BEGIN
    SET NOCOUNT ON
    BEGIN TRANSACTION

    BEGIN TRY
        -- 1. ADIM: dim_products Tablosunu Staging ile Eþitle (UPSERT / MERGE)
        MERGE dbo.dim_products AS TARGET
        USING dbo.stg_products AS SOURCE
        ON TARGET.source_product_id = SOURCE.source_product_id
        
        -- Eþleþen kayýt varsa ve bilgi deðiþtiyse güncelle
        WHEN MATCHED AND (
            TARGET.product_title <> SOURCE.product_title OR
            ISNULL(TARGET.brand, '') <> ISNULL(SOURCE.brand, '') OR
            ISNULL(TARGET.category, '') <> ISNULL(SOURCE.category, '')
        )
        THEN UPDATE SET 
            TARGET.product_title = SOURCE.product_title,
            TARGET.category = SOURCE.category,
            TARGET.brand = SOURCE.brand,
            TARGET.updated_at = GETDATE()
            
        -- Yeni ürünse ekle
        WHEN NOT MATCHED BY TARGET
        THEN INSERT (source_product_id, product_title, category, brand)
             VALUES (SOURCE.source_product_id, SOURCE.product_title, SOURCE.category, SOURCE.brand);

        -- 2. ADIM: Fiyat, Stok ve Puan Deðiþimlerini Fact Tablosuna Kaydet
        INSERT INTO dbo.fact_product_price_history (
            product_sk,
            base_price,
            discount_percentage,
            final_price,
            stock_quantity,
            rating,
            recorded_at
        )
        SELECT 
            dp.product_sk,
            stg.base_price,
            stg.discount_percentage,
            stg.final_price,
            stg.stock_quantity,
            stg.rating,
            GETDATE()
        FROM dbo.stg_products stg
        INNER JOIN dbo.dim_products dp 
            ON stg.source_product_id = dp.source_product_id

        COMMIT TRANSACTION
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION
        THROW
    END CATCH
END