import pandas as pd
import time

def clean_lob_data(file_path: str = "data/raw_lob_data.csv") -> pd.DataFrame:
    print("Veri yükleniyor ve anomali tespiti başlıyor...\n")
    start_time = time.time()

    # 1. Veriyi RAM'e al (Pandas DataFrame)
    df = pd.read_csv(file_path)
    initial_rows = len(df)

    # 2. Vektörize Spread Hesaplaması
    # Matematiksel kural: Spread = Ask - Bid
    df['spread'] = df['ask_price'] - df['bid_price']

    # 3. Anomali Tespiti 1: Eksik Veriler (NaN)
    # isna() tüm DataFrame'i tarar, any(axis=1) ise o satırda en az bir NaN varsa True döndürür.
    nan_mask = df.isna().any(axis=1)
    nan_count = nan_mask.sum()

    # 4. Anomali Tespiti 2: Crossed Market (Negatif veya Sıfır Spread)
    # Spread'in 0'a eşit veya küçük olduğu durumlar mantıksızdır.
    crossed_mask = df['spread'] <= 0
    crossed_count = crossed_mask.sum()

    # 5. Temizleme (Filtreleme)
    # Tilda (~) işareti "DEĞİL" (NOT) anlamına gelir. Maskeleri tersine çevirir.
    # Yani: NaN OLMAYANLARI ve Crossed OLMAYANLARI getir.
    clean_df = df[~nan_mask & ~crossed_mask].copy()
    final_rows = len(clean_df)

    # Temizlenmiş veriyi kaydet
    clean_file = "data/clean_lob_data.csv"
    clean_df.to_csv(clean_file, index=False)

    # Raporlama
    print("-" * 30)
    print("VERİ KALİTE RAPORU")
    print("-" * 30)
    print(f"Başlangıç Satır Sayısı: {initial_rows}")
    print(f"Eksik (NaN) Veri İçeren Satır: {nan_count}")
    print(f"Crossed Market Satır Sayısı: {crossed_count}")
    print(f"Kalan Temiz Satır Sayısı: {final_rows}")
    
    end_time = time.time()
    print(f"\nTüm işlem {end_time - start_time:.4f} saniyede tamamlandı.")
    print(f"Temizlenmiş veri kaydedildi: {clean_file}")

    return clean_df

if __name__ == "__main__":
    clean_lob_data()