import os
import time
from datetime import datetime, timedelta
# 画像処理ライブラリ
from PIL import Image, ImageDraw, ImageFont

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def download_vix_chart():
    print("--- Start Script ---")
    
    # ブラウザ設定
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # 1. サイトを開く
        url = "http://vixcentral.com/"
        print(f"Opening {url} ...")
        driver.get(url)

        # 2. グラフが表示されるまで待つ
        chart_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-container")))
        print("Chart loaded.")
        
        # 3. アニメーション待ち（5秒）
        time.sleep(5)
        
        # 4. ポップアップ消し（念のため）
        try:
            driver.find_element(By.TAG_NAME, "body").click()
        except:
            pass

        target_file = "vix_chart.png"
        
        # 5. スクリーンショット撮影（ループは使いません！）
        driver.execute_script("arguments[0].scrollIntoView();", chart_element)
        time.sleep(1)
        chart_element.screenshot(target_file)
        print(f"Screenshot saved: {target_file}")

        # 6. 日時書き込み処理
        if os.path.exists(target_file):
            print("Adding timestamp...")
            
            # 日本時間の計算
            jst_now = datetime.utcnow() + timedelta(hours=9)
            date_str = jst_now.strftime("%Y-%m-%d %H:%M JST")
            
            # 画像を開く
            img = Image.open(target_file)
            draw = ImageDraw.Draw(img)
            
            # 【重要】フォント読み込みを一番シンプルな形にする
            # ファイルパス指定だと環境によって止まることがあるため、
            # 最初から load_default() を試みる
            try:
                # デフォルトフォント（サイズ指定はできないが一番安全）
                font = ImageFont.load_default()
                # 少し大きくしたい場合、PCならサイズ指定できるが、
                # サーバーのエラー回避のため標準を使う
            except Exception as e:
                print(f"Font warning: {e}")
                font = None

            if font:
                # 文字を描く (左上 座標10,10 に赤色で)
                # デフォルトフォントは小さいので背景に白枠をつける
                draw.rectangle((10, 10, 150, 30), fill="white")
                draw.text((15, 15), date_str, fill="red", font=font)
            
            # 上書き保存
            img.save(target_file)
            print(f"Timestamp added: {date_str}")
            
        else:
            raise Exception("File not found after screenshot.")

    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("debug_error.png")
        exit(1)
    finally:
        driver.quit()
        print("--- End Script ---")

if __name__ == "__main__":
    download_vix_chart()