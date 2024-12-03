from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from conversation import conversation_script_1

chrome_driver_path = r"D:\Workspace\Python\chromedriver.exe"

# Cấu hình tài khoản
accounts = {
    "A": {
        "name": "Diễm Hằng Xinh Đẹp",
        "chrome_path": "C:\\Others\\Tele Accounts\\84929895980\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "C:\\Others\\Tele Accounts\\84929895980\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9222  # Cổng Remote Debugging riêng
    },
    "B": {
        "name": "Hải Bình Ngu Ngốc",
        "chrome_path": "C:\\Others\\Tele Accounts\\84826519744\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "C:\\Others\\Tele Accounts\\84826519744\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9223  # Cổng Remote Debugging riêng
    },
    "C": {
        "name": "Bình Minh Lên Rồi",
        "chrome_path": "C:\\Others\\Tele Accounts\\84925599903\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "C:\\Others\\Tele Accounts\\84925599903\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9224  # Cổng Remote Debugging riêng
    },
    "D": {
        "name": "Đình Diệu Diệu Kỳ",
        "chrome_path": "C:\\Others\\Tele Accounts\\84567845408\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "C:\\Others\\Tele Accounts\\84567845408\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9225  # Cổng Remote Debugging riêng
    },
}

# Hàm khởi tạo Selenium
def init_driver(account):
    options = webdriver.ChromeOptions()
    options.binary_location = account["chrome_path"]
    options.add_argument(f"--user-data-dir={account['user_data_dir']}")  # Thư mục dữ liệu riêng
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")  # Mở trình duyệt ở chế độ tối đa
    options.add_argument(f"--remote-debugging-port={account['debug_port']}")  # Cổng Debug riêng

    # Sử dụng webdriver-manager để tự động tải ChromeDriver
    service = Service(chrome_driver_path)
    return webdriver.Chrome(service=service, options=options)

def send_message(driver,  message):
    try:
        # Chờ cho nhóm chat tải xong
        # WebDriverWait(driver, 15).until(
        #     EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "peer-title")]'))
        # )

        # Chờ ô nhập liệu tin nhắn sẵn sàng (chọn div contenteditable thứ 2)
        message_box = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '(//div[@contenteditable="true"])[2]'))
        )

         # Chờ thời gian ngẫu nhiên từ 30 đến 60 giây
        wait_time = random.randint(2)
        print(f"Chờ {wait_time} giây trước khi gửi tin nhắn...")
        time.sleep(wait_time)

        # Gửi tin nhắn
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
        print(f"Đã gửi: {message}")

    except Exception as e:
        print(f"Lỗi khi gửi tin nhắn: {e}")

# Hàm chờ và nhận tin nhắn từ nhóm
def wait_for_new_message(driver, expected_message):
    try:
        # Lấy tất cả các thẻ <div> có lớp 'markup_f8f345 messageContent_f9f2ca'
        message_divs = WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.XPATH, '//div[contains(@class, "markup_f8f345") and contains(@class, "messageContent_f9f2ca")]')
        )

        # Duyệt qua từng <div> và lấy tất cả các thẻ <span> bên trong
        for div in message_divs:
            spans = div.find_elements(By.XPATH, './/span')  # Lấy tất cả các thẻ <span> trong <div>
            full_message = ''.join([span.text for span in spans]).strip()  # Nối nội dung các thẻ <span> lại thành chuỗi

            # Kiểm tra nội dung tin nhắn
            if full_message == expected_message:
                print(f"Nhận được tin nhắn khớp: {full_message}")
                return True

        print("Không tìm thấy tin nhắn khớp.")
        return False
    except Exception as e:
        print(f"Lỗi khi nhận tin nhắn: {e}")
        return False


# Hàm chính
def main():
    # Khởi tạo trình duyệt cho cả hai tài khoản
    drivers = {key: init_driver(account) for key, account in accounts.items()}

    try:
        # Mở Telegram Web
        for driver in drivers.values():
            driver.get("https://discord.com/channels/1310409244058587156/1310409287947784305")
        time.sleep(5)

        # Duyệt qua kịch bản hội thoại
        for step in conversation_script_1:
            sender = step["sender"]
            receiver = step["response"]

            # Gửi tin nhắn từ người gửi
            send_message(drivers[sender], step["message"])

            time.sleep(5)

            # Kiểm tra tin nhắn mới
            received = wait_for_new_message(drivers[receiver], step["message"])
            if received:
                send_message(drivers[receiver], step["reply"])

    except Exception as e:
        print(f"Lỗi xảy ra trong quá trình chạy: {e}")

    finally:
        # Đóng tất cả trình duyệt
        for driver in drivers.values():
            driver.quit()

if __name__ == "__main__":
    main()