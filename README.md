# Security Lab: Giám sát bàn phím & ghi ảnh màn hình

## Tổng quan

Đây là một dự án lab nghiên cứu bảo mật, mô phỏng các kỹ thuật phổ biến mà attacker sử dụng để thu thập dữ liệu, bao gồm:

- Ghi lại thao tác bàn phím (keylogging) → Lưu vào syslog.txt trong thư mục hệ thống
- Chụp màn hình định kỳ → Lưu ảnh vào thư mục screenshots
- Ghi lại lịch sử duyệt web → Đọc dữ liệu từ Google Chrome
- Gửi log qua email → Cấu hình thời gian gửi log bàn phím và ảnh màn hình về mail → Có thể biết được victim đang làm gì



## Mục tiêu dự án

Hiểu cách hoạt động của kỹ thuật ghi phím ở mức ứng dụng

Mô phỏng hành vi attacker trong thực tế

Phân tích cách các hoạt động này bị phát hiện bởi Antivirus/EDR

Rèn luyện kỹ năng Python trong lĩnh vực an toàn thông tin

Giúp hiểu rõ cách attacker hoạt động và từ đó cải thiện khả năng phát hiện và phòng thủ

## Công nghệ sử dụng
Python 3
- pynput – lắng nghe bàn phím
- Pillow – chụp màn hình
- smtplib – gửi email
- threading – xử lý đa luồng
