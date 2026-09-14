import os
import shutil
import urllib.request
from PKDevTools.classes.Archiver import afterMarketStockDataExists, get_user_data_dir

data_dir = get_user_data_dir()
os.makedirs(data_dir, exist_ok=True)
print(f"[+] User data directory: {data_dir}")

url = "https://raw.githubusercontent.com/pkjmesra/PKScreener/actions-data-download/actions-data-download/daily_candles.pkl"
target_raw = os.path.join(data_dir, "daily_candles.pkl")
if not os.path.exists(target_raw):
    print(f"[+] Downloading historical stock data (2,300+ Indian stocks)...")
    urllib.request.urlretrieve(url, target_raw)
print(f"[+] Data file ready: {os.path.getsize(target_raw)} bytes")

# Copy to expected daily and intraday cache filenames
_, daily_expected = afterMarketStockDataExists(intraday=False)
shutil.copy(target_raw, os.path.join(data_dir, daily_expected))
print(f"[+] Prepared daily cache: {daily_expected}")

_, intra_expected = afterMarketStockDataExists(intraday=True)
shutil.copy(target_raw, os.path.join(data_dir, intra_expected))
print(f"[+] Prepared intraday cache: {intra_expected}")

shutil.copy(target_raw, os.path.join(data_dir, "stock_data.pkl"))
print("[+] All cache targets successfully primed!")
