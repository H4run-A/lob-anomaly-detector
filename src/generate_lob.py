import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Python dökümantasyon standartlarına uygun tip belirteçleri (Type Hinting) kullanıyoruz
def generate_synthetic_lob(num_rows: int = 500000, output_file: str = "data/raw_lob_data.csv") -> None:
    print(f"Büyüklüğü {num_rows} satır olan LOB verisi üretiliyor...")

    # 1. Zaman Damgası (Timestamp) Üretimi: Her işlem arası 10 milisaniye
    start_time = datetime(2026, 1, 1, 9, 30, 0)
    timestamps = [start_time + timedelta(milliseconds=10 * i) for i in range(num_rows)]

    # 2. Fiyatların Rastgele Yürüyüşü (Random Walk)
    # Matematiksel model: P_t = P_{t-1} + epsilon_t
    np.random.seed(42) # Sonuçların her seferinde aynı çıkması için
    price_changes = np.random.normal(loc=0, scale=0.01, size=num_rows)
    base_price = 100.0 + np.cumsum(price_changes)

    # 3. Bid (Alış) ve Ask (Satış) Fiyatlarını Oluşturma
    # Normal şartlarda Spread her zaman > 0 olmalıdır.
    bids = base_price - np.random.uniform(0.01, 0.05, num_rows)
    asks = base_price + np.random.uniform(0.01, 0.05, num_rows)

    # Hacimleri (Size) rastgele belirle
    bid_sizes = np.random.randint(10, 500, num_rows)
    ask_sizes = np.random.randint(10, 500, num_rows)

    # 4. Veriyi Pandas DataFrame'ine Çevirme
    df = pd.DataFrame({
        'timestamp': timestamps,
        'bid_price': bids,
        'ask_price': asks,
        'bid_size': bid_sizes,
        'ask_size': ask_sizes
    })

    # 5. ANOMALİ ENJEKSİYONU (İleride bunları tespit edeceğiz)
    print("Anomaliler enjekte ediliyor (Crossed Markets ve NaN değerler)...")
    
    # Anomali 1: Rastgele 500 satırda Ask fiyatını Bid fiyatının altına çek (Crossed Market)
    anomaly_indices = np.random.choice(df.index, size=500, replace=False)
    df.loc[anomaly_indices, 'ask_price'] = df.loc[anomaly_indices, 'bid_price'] - 0.10

    # Anomali 2: Rastgele 1000 satırda bid_size değerini NaN yap
    nan_indices = np.random.choice(df.index, size=1000, replace=False)
    df.loc[nan_indices, 'bid_size'] = np.nan

    # 6. CSV olarak kaydet
    df.to_csv(output_file, index=False)
    print(f"Veri başarıyla kaydedildi: {output_file}")

if __name__ == "__main__":
    generate_synthetic_lob()