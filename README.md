# MCQ Quick Answer - Addon Hoàn Chỉnh

Addon cho phép trả lời nhanh câu hỏi MCQ bằng phím số 1-5 trong Anki.

## ✨ Tính năng

- ✅ **Trả lời nhanh bằng phím số 1-5** thay vì click chuột
- ✅ **Chỉ hoạt động với thẻ Quiz** - không ảnh hưởng thẻ khác
- ✅ **Bật/tắt tính năng** dễ dàng qua menu
- ✅ **Hiển thị tip hướng dẫn** đẹp mắt khi học thẻ
- ✅ **Tự động ẩn tip** sau 5 giây

## 📦 Cài đặt

### Cách 1: Từ file .ankiaddon
1. Tải file `mcq_quick_answer_final.ankiaddon`
2. Kéo thả vào Anki
3. Khởi động lại Anki

### Cách 2: Cài đặt thủ công
1. **Tools** → **Add-ons** → **View Files**
2. Tạo thư mục `mcq_quick_answer`
3. Tạo 3 files như dưới đây

## 📄 Code các files (Cài đặt thủ công)

### File 1: `__init__.py`
```python
[Xem code bên dưới]
```

### File 2: `manifest.json`
```json
{
    "name": "MCQ Quick Answer",
    "package": "mcq_quick_answer",
    "author": "MCQ Team",
    "version": "1.0.0",
    "description": "Trả lời nhanh câu hỏi MCQ bằng phím số 1-5. Chỉ hoạt động với thẻ có trường Quiz. Có thể bật/tắt và hiển thị tip hướng dẫn.",
    "homepage": "",
    "min_point_version": 45,
    "max_point_version": 0,
    "conflicts": []
}
```

### File 3: `config.json`
```json
{
    "enabled": true,
    "show_tip": true
}
```

## ⚙️ Cài đặt Addon

Sau khi cài đặt, vào **Tools** → **MCQ Quick Answer** → **Cài đặt**

### Tùy chọn 1: Bật tính năng trả lời nhanh
- ✅ **Bật:** Phím 1-5 sẽ chọn đáp án MCQ
- ❌ **Tắt:** Phím 1-5 hoạt động bình thường (đánh giá thẻ)

### Tùy chọn 2: Hiển thị dòng gợi ý
- ✅ **Bật:** Hiển thị tip "Mẹo: Dùng phím 1-4 để trả lời nhanh"
- ❌ **Tắt:** Không hiển thị tip

## 🎯 Cách sử dụng

1. Học thẻ có trường **Quiz**
2. Nhấn phím **1, 2, 3, 4, 5** để chọn đáp án
3. Addon tự động click vào button tương ứng
4. Thẻ lật sang mặt sau như bình thường

## 💡 Gợi ý Tip

Khi học thẻ Quiz (nếu bật tính năng hiển thị tip), bạn sẽ thấy:

```
💡 Mẹo: Dùng phím 1 2 3 4 5 để trả lời nhanh
```

- Tip hiển thị ở góc dưới bên phải
- Màu gradient đẹp mắt (tím - xanh)
- Tự động ẩn sau 5 giây
- Animation mượt mà

## 🔧 Yêu cầu

- Anki 2.1.45 trở lên
- Thẻ phải có trường **Quiz**
- Front template phải có các button với class `.mcq-option-button`

## 📋 Front Template

Đảm bảo front template của bạn có các button MCQ như này:

```html
<div class="mcq-option-button">Đáp án 1</div>
<div class="mcq-option-button">Đáp án 2</div>
<div class="mcq-option-button">Đáp án 3</div>
<div class="mcq-option-button">Đáp án 4</div>
<div class="mcq-option-button">Đáp án 5</div>
```

## ❓ FAQ

**Q: Phím số không hoạt động?**
A: Kiểm tra xem tính năng có được bật trong cài đặt không (Tools → MCQ Quick Answer → Cài đặt)

**Q: Phím số hoạt động trên thẻ không phải Quiz?**
A: Không, addon chỉ hoạt động khi thẻ có trường "Quiz". Thẻ khác hoạt động bình thường.

**Q: Tôi muốn tắt tip?**
A: Vào Tools → MCQ Quick Answer → Cài đặt → Bỏ tick "Hiển thị dòng gợi ý"

**Q: Có thể dùng phím khác thay vì 1-5?**
A: Hiện tại chỉ hỗ trợ phím 1-5. Nếu cần phím khác, có thể sửa code.

## 🎨 Tùy chỉnh Tip

Muốn thay đổi màu sắc hoặc vị trí tip? Sửa đoạn code này trong `__init__.py`:

```javascript
tip.style.cssText = `
    position: fixed;
    bottom: 20px;        // Vị trí từ dưới
    right: 20px;         // Vị trí từ phải
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); // Màu gradient
    ...
`;
```

## 🐛 Gỡ lỗi

Nếu gặp vấn đề:
1. Mở Console: **Tools** → **Add-ons** → Chọn addon → **View Files**
2. Xem logs khi nhấn phím
3. Kiểm tra xem có thông báo lỗi không

## 📝 Changelog

### Version 1.0.0
- ✅ Chức năng trả lời nhanh bằng phím 1-5
- ✅ Menu cài đặt bật/tắt
- ✅ Hiển thị tip hướng dẫn
- ✅ Chỉ hoạt động với thẻ Quiz

## 👏 Đóng góp

Nếu có ý tưởng cải tiến hoặc phát hiện lỗi, vui lòng báo cáo!

## 📜 License

MIT License
