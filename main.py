import os
import time
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def download_vix_chart():
    # パスは必ず「絶対パス」で指定する
    download_dir = os.getcwd()
    
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    # Bot対策User-Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    # 通常の設定（これだけでは不十分な場合がある）
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    print("Launching Chrome...")
    driver = webdriver.Chrome(options=options)
    
    # ▼▼▼ 重要：ヘッドレスでもダウンロードを強制許可する魔法のコマンド ▼▼▼
    driver.execute_cdp_cmd("Page.setDownloadBehavior", {
        "behavior": "allow",
        "downloadPath": download_dir
    })
    # ▲▲▲ 追加ここまで ▲▲▲

    wait = WebDriverWait(driver, 20)

    try:
        url = "http://vixcentral.com/"
        print(f"Opening {url} ...")
        driver.get(url)

        # 読み込み待ち
        time.sleep(5)
        
        # コンテナ待ち
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-container")))
        print("Page loaded.")

        # メニューボタンをクリック（JSで強制クリック）
        export_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".highcharts-contextbutton")))
        driver.execute_script("arguments[0].click();", export_button)
        print("Menu clicked.")
        time.sleep(1)

        # ダウンロードボタンをクリック
        download_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Download PNG image')]")))
        driver.execute_script("arguments[0].click();", download_item)
        print("Download clicked.")

        # ダウンロード待機（最大30秒）
        max_wait = 30
        elapsed = 0
        target_file = "vix_chart.png"
        
        print(f"Waiting for download in: {download_dir}")

        while elapsed < max_wait:
            # 最新のファイル状況を確認
            files = glob.glob(os.path.join(download_dir, "*.png"))
            # debug画像とターゲット画像以外を探す（＝新規ダウンロードファイル）
            candidates = [f for f in files if "debug_" not in f and target_file not in f]
            
            if candidates:
                downloaded_file = candidates[0]
                # ダウンロード中のファイル(.crdownload)でないか確認
                if not downloaded_file.endswith(".crdownload"):
                    print(f"File found: {downloaded_file}")
                    
                    # 既存ファイルがあれば削除
                    if os.path.exists(target_file):
                        os.remove(target_file)
                    
                    # リネーム
                    os.rename(downloaded_file, target_file)
                    print(f"Success! Saved as {target_file}")
                    return # 成功して終了
            
            time.sleep(1)
            elapsed += 1
            if elapsed % 5 == 0:
                print(f"Waiting... {elapsed}s")

        # タイムアウトした場合
        print("Error: Download timeout.")
        # ディレクトリの中身を表示してデバッグ
        print(f"Files in directory: {os.listdir(download_dir)}")
        driver.save_screenshot("debug_timeout.png")
        exit(1)

    except Exception as e:
        print(f"Exception occurred: {e}")
        driver.save_screenshot("debug_error.png")
        exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    download_vix_chart()