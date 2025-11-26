import os
import time
import glob
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def download_vix_chart():
    # === 設定: GitHub Actions上で動くための設定 ===
    options = Options()
    options.add_argument("--headless=new") # ヘッドレスモード（画面を表示しない）
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # 保存先を「現在のフォルダ」に設定
    download_dir = os.getcwd()
    
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    print("Launching Headless Chrome...")
    # GitHub Actionsではドライバのパス指定は不要（Seleniumが自動管理）
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        url = "http://vixcentral.com/"
        print(f"Opening {url} ...")
        driver.get(url)

        # チャートが表示されるまで待機
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-container")))
        print("Chart container loaded.")

        # エクスポートメニュー（ハンバーガーメニュー）をクリック
        # 読み込み直後はクリックできないことがあるため少し待機
        time.sleep(2) 
        export_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".highcharts-contextbutton"))
        )
        export_button.click()
        print("Opened export menu.")

        # "Download PNG" をクリック
        download_item = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(., 'Download PNG image')]")
            )
        )
        download_item.click()
        print("Clicked Download PNG.")

        # ダウンロード待機（.pngファイルが増えるのを待つ）
        max_wait = 30
        elapsed = 0
        file_found = False
        target_file = "vix_chart.png" # 最終的なファイル名

        while elapsed < max_wait:
            # chart.png という名前で落ちてくることが多いが、念のためワイルドカードで探す
            files = glob.glob(os.path.join(download_dir, "*.png"))
            # 名前変更済みのファイル（vix_chart.png）は除外して判定
            new_files = [f for f in files if target_file not in f]
            
            if new_files:
                # ダウンロードされたファイルを見つけた
                downloaded_file = new_files[0]
                # 完全にダウンロードが終わるまで（サイズが0以上）少し待つ
                if os.path.getsize(downloaded_file) > 0:
                    print(f"File downloaded: {downloaded_file}")
                    
                    # 既存の vix_chart.png があれば削除
                    if os.path.exists(target_file):
                        os.remove(target_file)
                    
                    # 名前を固定名に変更
                    os.rename(downloaded_file, target_file)
                    print(f"Renamed to: {target_file}")
                    file_found = True
                    break
            
            time.sleep(1)
            elapsed += 1

        if not file_found:
            print("Error: Download timed out.")
            exit(1) # エラー終了

    except Exception as exc:
        print(f"Error occurred: {exc}")
        exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    download_vix_chart()