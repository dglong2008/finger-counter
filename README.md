# Finger Counter - MediaPipe Hands

Ứng dụng **Finger Counter** dùng webcam, MediaPipe Hands và OpenCV để phát hiện tối đa 2 bàn tay và đếm tổng số ngón tay đang duỗi (0-10).

## 1. Chức năng

- Đọc hình ảnh trực tiếp từ webcam.
- Dùng MediaPipe Hands để lấy 21 landmark của mỗi bàn tay.
- Tự xây dựng logic xác định ngón tay đang duỗi hay co.
- Hiển thị số ngón của từng tay và tổng số ngón trên màn hình.
- Nhấn `Q` để thoát.

## 2. Thuật toán

Chương trình dùng **góc giữa các landmark** thay vì chỉ so sánh trái/phải hoặc trên/dưới của đầu ngón tay.

- Ngón trỏ, giữa, áp út và út: tính góc tại khớp PIP bằng 3 landmark MCP - PIP - TIP. Nếu góc lớn hơn `160°`, ngón được xem là đang duỗi.
- Ngón cái: tính góc bằng landmark `2 - 3 - 4`. Nếu góc lớn hơn `150°` và đầu ngón cái nằm xa vùng lòng bàn tay hơn khớp trước nó, ngón cái được xem là đang duỗi.
- Kết quả của tối đa 2 bàn tay được cộng lại để tạo `TOTAL` từ 0 đến 10.

Cách này ổn định hơn khi lòng bàn tay hướng về camera và không phụ thuộc vào nhãn Left/Right để quyết định trạng thái ngón cái.

## 3. Yêu cầu môi trường

Khuyến nghị:

- Python **3.11**
- Webcam hoạt động bình thường
- Windows / macOS / Linux

## 4. Cài đặt

### Windows PowerShell

Nếu máy có nhiều phiên bản Python, tạo môi trường ảo bằng Python 3.11:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Kiểm tra:

```powershell
python --version
```

Kết quả nên là `Python 3.11.x`.

### Windows Command Prompt

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS / Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 5. Chạy chương trình

```bash
python main.py
```

Đưa một hoặc hai bàn tay vào khung hình. Ứng dụng sẽ vẽ landmark và hiển thị số ngón tay. Nhấn `Q` để thoát.

## 6. Xử lý lỗi thường gặp

### Không mở được camera

- Đóng Zoom, Teams, Discord hoặc ứng dụng khác đang dùng webcam.
- Cấp quyền Camera cho Terminal/Python trong hệ điều hành.
- Nếu máy có nhiều camera, thử đổi `cv2.VideoCapture(0)` thành `cv2.VideoCapture(1)`.

### Không cài được MediaPipe

Đảm bảo môi trường ảo đang dùng Python 3.11:

```powershell
python --version
```

Nếu `.venv` cũ được tạo bằng Python khác, xóa `.venv` rồi tạo lại bằng `py -3.11 -m venv .venv`.

### MediaPipe báo thiếu file `.binarypb`

Thử cài lại MediaPipe sạch:

```powershell
python -m pip uninstall mediapipe -y
python -m pip cache purge
python -m pip install --no-cache-dir mediapipe==0.10.21
```

Nếu vẫn lỗi và đường dẫn project có ký tự đặc biệt, thử copy project sang đường dẫn ngắn như `D:\FingerCounter` rồi tạo lại `.venv`.

### Kết quả đếm chưa ổn định

- Để toàn bộ bàn tay trong khung hình.
- Giữ khoảng cách vừa phải với camera.
- Tránh các ngón che nhau.
- Dùng ánh sáng đủ tốt.
- Góc 2D giúp ổn định hơn cách so sánh x/y đơn giản nhưng khi xoay bàn tay quá mạnh vẫn có thể sai.

## 7. Cấu trúc repository

```text
source/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 8. Video demo

**Demo video:** `CHUA_CO_LINK_DEMO`