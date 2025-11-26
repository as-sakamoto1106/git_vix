import os
import time
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def download_vix_chart():
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    # Bot対策：User-Agentを普通のChromeに見せる
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    download_dir = os.getcwd()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    print("Launching Chrome...")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        url = "http://vixcentral.com/"
        print(f"Opening {url} ...")
        driver.get(url)

        # 念のため読み込み待ち
        time.sleep(5)
        
        # デバッグ：トップページのスクショを撮る
        driver.save_screenshot("debug_01_homepage.png")
        print("Screenshot saved: homepage")

        # コンテナ待ち
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-container")))
        
        # --- 対策: JavaScriptで無理やりクリックする ---
        # メニューボタン
        export_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".highcharts-contextbutton")))
        driver.execute_script("arguments[0].click();", export_button)
        print("Clicked export menu (via JS).")
        time.sleep(1)

        driver.save_screenshot("debug_02_menu_open.png")

        # ダウンロードボタン
        download_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Download PNG image')]")))
        driver.execute_script("arguments[0].click();", download_item)
        print("Clicked Download PNG (via JS).")

        # 待機ループ
        max_wait = 30
        elapsed = 0
        target_file = "vix_chart.png"
        
        while elapsed < max_wait:
            files = glob.glob("*.png")
            # debug_から始まるファイルは除外して探す
            downloaded = [f for f in files if not f.startswith("debug_") and f != target_file]
            
            if downloaded:
                print(f"File found: {downloaded[0]}")
                if os.path.exists(target_file):
                    os.remove(target_file)
                os.rename(downloaded[0], target_file)
                print("Success! Image renamed.")
                return # 成功終了
            
            time.sleep(2)
            elapsed += 1
            print(f"Waiting... {elapsed}s")

        # タイムアウトした場合
        print("Error: Timeout loop finished.")
        # 失敗時の画面を撮る
        driver.save_screenshot("debug_03_timeout.png")
        # フォルダの中身を表示してみる
        print(f"Files in dir: {os.listdir('.')}")
        exit(1) # エラーとして終了

    except Exception as e:
        print(f"Exception: {e}")
        driver.save_screenshot("debug_99_exception.png")
        exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    download_vix_chart()