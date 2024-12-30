# Simple Chord System Made by Python

![Python Version](https://img.shields.io/badge/python-3.x-blue)  
Một chương trình Python đơn giản để mô phỏng thuật toán Chord Distributed Hash Table (DHT), được sử dụng rộng rãi trong các hệ thống phân tán để quản lý định danh và lưu trữ dữ liệu hiệu quả.

---

## 🗋 Mô tả

Chord DHT là một thuật toán phổ biến để quản lý định danh trong các hệ thống phân tán. Nó xác định nhanh chóng vị trí của một "key" trong một mạng vòng với chi phí thấp.

Chương trình này triển khai:
1. **Finger Table Creation**: Cung cấp tuyến đường nhanh đến các nút khác.
2. **Key Location (Successor)**: Xác định nút chịu trách nhiệm lưu trữ một key cụ thể.
3. **Query Path**: Xây dựng đường dẫn tìm kiếm từ bất kỳ nút nào đến nút lưu trữ key.

---

## 🚀 Tính năng chính

- Tạo Finger Table cho các nút trong mạng vòng.
- Tìm successor của một key.
- Tìm đường dẫn truy vấn từ bất kỳ nút nào đến key mong muốn.

---

## 📙 Giải thích thuật toán và ứng dụng

### **Thuật toán Chord DHT**
- Chord DHT sử dụng một không gian định danh dạng vòng (m-bit). Mỗi nút và key được ánh xạ vào không gian [0, 2^m - 1].
- **Finger Table**: Mỗi nút duy trì một bảng định tuyến gồm m mục, giúp xác định nút tiếp theo trên đường dẫn đến successor của key.  
- **Ứng dụng**: Chord lý tưởng cho các hệ thống lưu trữ dữ liệu phân tán như BitTorrent, các ứng dụng ngang hàng, và blockchain.

---

## 📂 Cấu trúc dự án

```plaintext
.
├── chord.py                    # Code chính
├── README.md                   # README.md
├── DS_Lec 4 - Dinh danh.pdf    # Tài liệu
└── img/
    └── image.png               # Minh họa kết quả
```

---

## 📊 Quá trình tạo kết quả

### Input
- **Nodes**: `[143, 90, 80, 15, 31, 46]`  
  Danh sách các nút trong hệ thống phân tán, được ánh xạ vào không gian định danh (m = 7).  
- **Key to Locate**: `44`

### Output
1. **Finger Table**  
   Mỗi nút có một bảng định tuyến đến các nút gần nhất dựa trên khoảng cách 2^i (i = 0, ..., m-1).  
   **Ví dụ**:  
   - Nút `15` có bảng finger `[31, 31, 31, 31, 31, 80, 80]`, chỉ đến các nút gần nhất trong không gian định danh.

2. **Key Location**  
   - Key `44` được lưu tại nút `46`, vì đây là successor gần nhất của `44`.

---

## 📊 Giải thích chi tiết từng hàm

### 1. `binarySearch(arr, item)`
**Chức năng:** Thực hiện tìm kiếm nhị phân để tìm một phần tử trong danh sách đã sắp xếp.  
**Mục đích:** Giúp xác định vị trí gần đúng của một giá trị, hỗ trợ trong việc tìm successor.

### 2. `successor(L, n)`
**Chức năng:** Tìm successor (nút tiếp theo) cho giá trị `n` trong danh sách các nút.  
**Mục đích:** Trong Chord, successor của một nút là nút nhỏ nhất lớn hơn hoặc bằng `n`.

### 3. `get_fingers(nodes, m)`
**Chức năng:** Tạo **Finger Table** cho mỗi nút.  
**Mục đích:** Tối ưu hóa tìm kiếm trong mạng vòng bằng cách tiền xử lý thông tin định tuyến.

### 4. `get_key_loc(nodes, k, m)`
**Chức năng:** Xác định nút chịu trách nhiệm lưu trữ một key `k`.  
**Mục đích:** Xác định chính xác nút mà key được ánh xạ.

### 5. `get_query_path(nodes, k, n, m)`
**Chức năng:** Xây dựng đường dẫn từ một nút cụ thể đến nút lưu trữ key `k`.  
**Mục đích:** Mô phỏng cách Chord sử dụng Finger Table để định vị key hiệu quả.

---

## 📊 Kết quả minh họa

### Input
```python
nodes = [143, 90, 80, 15, 31, 46]  # Danh sách các nút
m = 7  # Kích thước không gian định danh
key = 44  # Key cần tìm
```

### Output
```
Chord DHT:  [143, 90, 80, 15, 31, 46] m =  7

Finger Table:
{15: [31, 31, 31, 31, 31, 80, 80],
 31: [46, 46, 46, 46, 80, 80, 15],
 46: [80, 80, 80, 80, 80, 80, 15],
 80: [90, 90, 90, 90, 15, 15, 31],
 90: [15, 15, 15, 15, 15, 15, 31],
 143: [31, 31, 31, 31, 31, 80, 80]}

Key location for key =  44 is at node:  46
```

---

## 📝 Cách chạy chương trình

1. Clone repository về máy:  
   ```bash
   https://github.com/NguyenHieu-class/ung_dung_phan_tan.git
   cd DS_Lec_4_Dinh_Danh
   ```

2. Chạy chương trình:  
   ```bash
   python chord.py
   ```

---

## 📺 Minh họa trực quan

![Result](https://github.com/NguyenHieu-class/ung_dung_phan_tan/blob/262b337c29e208a2020d4c57b744e80b5fc034a1/DS_Lec_4_Dinh_Danh/img/image.png)

---


