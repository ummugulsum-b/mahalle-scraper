import time
import os
import pdfplumber
import csv
import json
import re
import schedule

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

download_dir = os.path.join(os.getcwd(), "data")

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    },
)


def download_pdf():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    driver.get("https://www.e-icisleri.gov.tr/Anasayfa/MulkiIdariBolumleri.aspx")

    time.sleep(3)

    button = driver.find_element(
        By.ID, "ctl00_cph1_CografiBirimControl_imgButtonMahalleSayisi"
    )
    button.click()

    time.sleep(5)

    driver.quit()


def get_latest_pdf_file():
    files = [f for f in os.listdir(download_dir) if f.endswith(".pdf")]

    if not files:
        print("PDF dosyası bulunamadı.")
        return None

    latest_pdf = max(
        files, key=lambda f: os.path.getctime(os.path.join(download_dir, f))
    )
    return os.path.join(download_dir, latest_pdf)


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def parse_mahalle_data(text):
    mahalle_listesi = []
    pattern = re.compile(
        r"(\d+)\s+([0-9A-Za-z\u00C0-\u017F\s\(\)-\.]+(?:-\w+)*)(?:\s+([A-ZÇŞĞÜÖİÂ]+))\s*(?:->\s*([A-ZÇŞĞÜÖİÂ\s-]+))?"
    )

    for line in text.split("\n"):
        match = pattern.match(line)
        if match:
            mahalle_listesi.append(
                {
                    "sira_no": int(match.group(1)),
                    "mahalle_adi": match.group(2).strip(),
                    "il": match.group(3).strip(),
                    "ilce": match.group(4).strip().replace(" -", ""),
                }
            )
    return mahalle_listesi


def save_to_json(data, json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"JSON dosyası oluşturuldu: {json_path}")


def save_to_csv(data, csv_path):
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sira_no", "mahalle_adi", "il", "ilce"])
        writer.writeheader()
        writer.writerows(data)
    print(f"CSV dosyası oluşturuldu: {csv_path}")


def job():
    download_pdf()

    pdf_path = get_latest_pdf_file()
    if pdf_path:
        text = extract_text_from_pdf(pdf_path)
        mahalle_listesi = parse_mahalle_data(text)
        json_path = os.path.join(download_dir, "mahalle_listesi.json")
        csv_path = os.path.join(download_dir, "mahalle_listesi.csv")
        save_to_json(mahalle_listesi, json_path)
        save_to_csv(mahalle_listesi, csv_path)
    else:
        print("PDF dosyası indirilemedi.")


schedule.every().week.do(job)

job()

while True:
    schedule.run_pending()
    time.sleep(1)
