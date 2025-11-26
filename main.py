import os
import time
from datetime import datetime, timedelta
# ▼▼▼ 追加：画像処理ライブラリ ▼▼▼
from PIL import Image, ImageDraw, ImageFont
# ▲▲▲ 追加ここまで ▲▲▲
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
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    print("Launching Chrome...")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        url = "http://vixcentral.com/"
        print(f"Opening {url} ...")
        driver.get(url)

        # チャート読み込み待ち
        chart_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "highcharts-container")))
        print("Chart loaded.")
        
        # アニメーション待ち
        time.sleep(5)
        
        # ポップアップ消し
        try:
            driver.find_element(By.TAG_NAME, "body").click()
        except:
            pass

        target_file = "vix_chart.png"
        
        # 要素までスクロールして撮影
        driver.execute_script("arguments[0].scrollIntoView();", chart_element)
        time.sleep(1)
        chart_element.screenshot(target_file)
        print(f"Screenshot saved: {target_file}")

        # ▼▼▼ 追加：日付を書き込む処理 ▼▼▼
        if os.path.exists(target_file):
            # 1. 日本時間の計算 (UTC + 9時間)
            jst_now = datetime.utcnow() + timedelta(hours=9)
            date_str = jst_now.strftime("%Y-%m-%d %H:%M JST")
            
            # 2. 画像を開く
            img = Image.open(target_file)
            draw = ImageDraw.Draw(img)
            
            # 3. フォント設定 (サーバー上のフォントを探す)
            # Ubuntu(GitHub Actions)にはDejaVuSansが入っていることが多い
            try:
                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                font = ImageFont.truetype(font_path, 24) # サイズ24
            except:
                # なければデフォルト（小さいかもしれないがエラーにはならない）
                font = ImageFont.load_default()
            
            # 4. 文字を描く (左上 座標10,10 に赤色で)
            draw.text((15, 15), date_str, fill="red", font=font)
            
            # 5. 上書き保存
            img.save(target_file)
            print(f"Timestamp added: {date_str}")
        # ▲▲▲ 追加ここまで ▲▲▲

    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("debug_error.png")
        exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    download_vix_chart()