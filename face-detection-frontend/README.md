# 🎯 Hướng dẫn chạy Face Detection Frontend

## 📋 **Cách 1: Sử dụng Live Server (Khuyến nghị)**

### Bước 1: Cài đặt Live Server Extension
- Extension Live Server đã được cài đặt sẵn trong VS Code

### Bước 2: Khởi chạy Frontend
1. **Mở file `index.html`** trong VS Code
2. **Click chuột phải** vào file `index.html`
3. **Chọn "Open with Live Server"**
4. Trình duyệt sẽ tự động mở tại: `http://127.0.0.1:5500/index.html`

---

## 📋 **Cách 2: Sử dụng Python HTTP Server**

```bash
# Mở terminal trong thư mục face-detection-frontend
cd "d:\NguyenTuanKhanh\Python_project\face-detection-frontend"

# Chạy Python HTTP server
python -m http.server 3000

# Hoặc nếu có Python 2
python -m SimpleHTTPServer 3000
```

Sau đó mở trình duyệt: `http://localhost:3000`

---

## 📋 **Cách 3: Mở trực tiếp file HTML**

**⚠️ Không khuyến nghị** - có thể gặp lỗi CORS

1. Mở file `index.html` trực tiếp trong trình duyệt
2. Có thể cần disable CORS trong browser để test API

---

## 🚀 **Kiểm tra hoạt động**

### 1. **Kiểm tra API Status**
- Phải thấy badge **"API đang hoạt động"** màu xanh ở góc phải header
- Nếu hiện đỏ, kiểm tra backend có đang chạy trên port 8080 không

### 2. **Test Upload ảnh**
- Click vào vùng upload hoặc kéo thả ảnh
- Ảnh phải hiển thị preview
- Nút "Nhận diện khuôn mặt" phải được enable (màu xanh)

### 3. **Test ảnh mẫu**
- Click vào các icon ảnh mẫu (Portrait, Group, Family)
- Sẽ tự động tạo ảnh test với khuôn mặt giả

### 4. **Test API Call**
- Nhấn nút "Nhận diện khuôn mặt"
- Phải thấy loading spinner
- Sau vài giây sẽ hiển thị kết quả và khoanh vùng khuôn mặt

---

## 🔧 **Troubleshooting**

### ❌ **API không hoạt động**
```bash
# Kiểm tra backend có chạy không
curl http://localhost:8080/api/face-detection/detect
```

### ❌ **CORS Error**
- Đảm bảo backend đã cấu hình CORS
- Hoặc dùng Live Server thay vì mở file trực tiếp

### ❌ **Không hiển thị kết quả**
- Mở Developer Tools (F12)
- Kiểm tra Console tab có lỗi gì không
- Kiểm tra Network tab xem API call có thành công không

### ❌ **Không khoanh được vùng mặt**
- Kiểm tra kết quả API có trả về đúng format không
- Kiểm tra coordinates của faces có hợp lệ không

---

## 📱 **Giao diện hoạt động**

### **Panel trái:**
- ✅ Upload area với drag & drop
- ✅ 3 ảnh mẫu test (Portrait, Group, Family)  
- ✅ Sliders điều chỉnh thông số (minSize, scaleFactor, minNeighbors)
- ✅ 3 preset buttons (Chính xác, Cân bằng, Nhanh)
- ✅ Button "Nhận diện khuôn mặt"

### **Panel phải:**
- ✅ Image preview với overlay canvas
- ✅ Stats cards (số mặt, thời gian, kích thước, dung lượng)
- ✅ Bảng chi tiết tọa độ từng khuôn mặt
- ✅ Loading state với spinner

### **Hiệu ứng:**
- ✅ Face boxes màu đỏ với animation dash
- ✅ Labels "Face 1", "Face 2"... 
- ✅ Corner indicators
- ✅ Glow effects
- ✅ Hover animations

---

## 🎯 **Test Cases**

1. **Portrait image**: Expect 1 face
2. **Group image**: Expect 3+ faces  
3. **Family image**: Expect 2-4 faces
4. **Adjust parameters**: Thay đổi sliders và xem kết quả khác nhau
5. **Preset modes**: Test 3 chế độ Chính xác/Cân bằng/Nhanh

---

## 📞 **Liên hệ hỗ trợ**

Nếu gặp vấn đề, kiểm tra:
1. Backend có chạy trên port 8080?
2. Python virtual environment đã activate?
3. OpenCV đã cài đặt trong venv?
4. File ảnh có đúng format (jpg, png, bmp)?
5. Developer Console có báo lỗi gì?
