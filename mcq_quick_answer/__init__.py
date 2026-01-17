"""
MCQ Quick Answer - Trả lời nhanh MCQ bằng phím số 1-5
"""

from aqt import mw, gui_hooks
from aqt.reviewer import Reviewer
from aqt.utils import showInfo
from aqt.qt import QAction, QDialog, QVBoxLayout, QCheckBox, QPushButton, QLabel
from anki.hooks import wrap
import json

# Config mặc định
DEFAULT_CONFIG = {
    "enabled": True,
    "show_tip": True
}

class ConfigDialog(QDialog):
    """Dialog cài đặt addon"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cài đặt MCQ Quick Answer")
        self.setMinimumWidth(400)
        self.setup_ui()
        self.load_config()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        layout = QVBoxLayout()
        
        # Tiêu đề
        title = QLabel("<h2>Cài đặt MCQ Quick Answer</h2>")
        layout.addWidget(title)
        
        # Checkbox bật/tắt tính năng
        self.enabled_checkbox = QCheckBox("Bật tính năng trả lời nhanh bằng phím số 1-5")
        self.enabled_checkbox.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.enabled_checkbox)
        
        # Mô tả
        desc1 = QLabel("Khi bật: Nhấn phím 1-5 sẽ chọn đáp án MCQ thay vì đánh giá thẻ")
        desc1.setStyleSheet("color: gray; padding-left: 25px;")
        layout.addWidget(desc1)
        
        layout.addSpacing(10)
        
        # Checkbox hiển thị tip
        self.show_tip_checkbox = QCheckBox("Hiển thị dòng gợi ý sử dụng phím tắt")
        self.show_tip_checkbox.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.show_tip_checkbox)
        
        # Mô tả
        desc2 = QLabel("Hiển thị: 'Mẹo: Dùng phím 1-4 để trả lời nhanh' trên thẻ")
        desc2.setStyleSheet("color: gray; padding-left: 25px;")
        layout.addWidget(desc2)
        
        layout.addSpacing(20)
        
        # Buttons
        save_btn = QPushButton("Lưu và Đóng")
        save_btn.clicked.connect(self.save_and_close)
        save_btn.setStyleSheet("font-size: 14px; padding: 8px;")
        layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("font-size: 14px; padding: 8px;")
        layout.addWidget(cancel_btn)
        
        self.setLayout(layout)
    
    def load_config(self):
        """Load cấu hình"""
        config = get_config()
        self.enabled_checkbox.setChecked(config["enabled"])
        self.show_tip_checkbox.setChecked(config["show_tip"])
    
    def save_and_close(self):
        """Lưu cấu hình và đóng"""
        config = {
            "enabled": self.enabled_checkbox.isChecked(),
            "show_tip": self.show_tip_checkbox.isChecked()
        }
        save_config(config)
        showInfo("Đã lưu cài đặt!\n\nCài đặt sẽ có hiệu lực với các thẻ tiếp theo.")
        self.accept()

def get_config():
    """Lấy cấu hình"""
    config = mw.addonManager.getConfig(__name__)
    if config is None:
        config = DEFAULT_CONFIG.copy()
        save_config(config)
    return config

def save_config(config):
    """Lưu cấu hình"""
    mw.addonManager.writeConfig(__name__, config)

def _answerCard_wrapper(self, ease, _old):
    """Wrapper cho _answerCard - chặn khi có MCQ"""
    
    # Kiểm tra xem tính năng có được bật không
    config = get_config()
    if not config["enabled"]:
        # Tính năng tắt - hoạt động bình thường
        return _old(self, ease)
    
    # Kiểm tra xem có đang ở question state không
    if self.state != "question":
        return _old(self, ease)
    
    # Kiểm tra có thẻ Quiz không
    if not self.card:
        return _old(self, ease)
    
    note = self.card.note()
    if "Quiz" not in note:
        # Không phải thẻ Quiz - cho phép answer bình thường
        return _old(self, ease)
    
    # ĐÂY LÀ THẺ QUIZ Ở QUESTION STATE - CHẶN VÀ CLICK MCQ
    
    print(f"MCQ: Chặn _answerCard(ease={ease}), chuyển sang click button {ease}")
    
    # Gửi JavaScript để click button tương ứng
    js_code = f"""
    (function() {{
        var buttons = document.querySelectorAll('.mcq-option-button');
        if (buttons.length >= {ease} && !buttons[{ease-1}].classList.contains('disabled')) {{
            buttons[{ease-1}].click();
            console.log('MCQ Quick Answer: Đã click button ' + {ease});
        }} else {{
            console.log('MCQ Quick Answer: Không tìm thấy button ' + {ease} + ' hoặc đã disabled');
        }}
    }})();
    """
    
    self.web.eval(js_code)
    
    # Chặn hoàn toàn việc answer
    return None

def inject_tip_on_show_question(card):
    """Inject dòng tip khi hiển thị câu hỏi"""
    
    # Kiểm tra cấu hình
    config = get_config()
    if not config["enabled"] or not config["show_tip"]:
        return
    
    # Kiểm tra có phải thẻ Quiz không
    if not card:
        return
    
    note = card.note()
    if "Quiz" not in note:
        return
    
    # Kiểm tra reviewer state
    if not mw.reviewer or mw.reviewer.state != "question":
        return
    
    # Inject tip vào trang
    tip_js = """
    (function() {
        // Kiểm tra xem đã có tip chưa
        if (document.getElementById('mcq-quick-answer-tip')) {
            return;
        }
        
        // Tạo tip element
        var tip = document.createElement('div');
        tip.id = 'mcq-quick-answer-tip';
        tip.innerHTML = '💡 <strong>Mẹo:</strong> Dùng phím <kbd>1</kbd> <kbd>2</kbd> <kbd>3</kbd> <kbd>4</kbd> <kbd>5</kbd> để trả lời nhanh';
        tip.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 99999;
            animation: slideInUp 0.3s ease-out;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        `;
        
        // Style cho kbd tags
        var style = document.createElement('style');
        style.textContent = `
            @keyframes slideInUp {
                from {
                    transform: translateY(20px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
            #mcq-quick-answer-tip kbd {
                background: rgba(255,255,255,0.2);
                padding: 3px 8px;
                border-radius: 4px;
                font-family: monospace;
                font-size: 13px;
                font-weight: bold;
                margin: 0 2px;
                border: 1px solid rgba(255,255,255,0.3);
            }
        `;
        document.head.appendChild(style);
        
        // Thêm vào body
        document.body.appendChild(tip);
        
        // Tự động ẩn sau 5 giây
        setTimeout(function() {
            tip.style.transition = 'opacity 0.3s ease-out, transform 0.3s ease-out';
            tip.style.opacity = '0';
            tip.style.transform = 'translateY(20px)';
            setTimeout(function() {
                tip.remove();
            }, 300);
        }, 5000);
        
        console.log('MCQ Quick Answer: Đã hiển thị tip');
    })();
    """
    
    mw.reviewer.web.eval(tip_js)

def show_config_dialog():
    """Hiển thị dialog cài đặt"""
    dialog = ConfigDialog(mw)
    dialog.exec()

def show_about():
    """Hiển thị thông tin addon"""
    about_text = """
    <h2>MCQ Quick Answer</h2>
    <p><strong>Phiên bản:</strong> 1.0.0</p>
    
    <h3>Tính năng:</h3>
    <ul>
        <li>✅ Trả lời nhanh MCQ bằng phím số 1-5</li>
        <li>✅ Chỉ hoạt động với thẻ có trường Quiz</li>
        <li>✅ Bật/tắt tính năng dễ dàng</li>
        <li>✅ Hiển thị tip hướng dẫn</li>
    </ul>
    
    <h3>Cách dùng:</h3>
    <p>Khi học thẻ MCQ, nhấn phím <strong>1, 2, 3, 4, 5</strong> để chọn đáp án tương ứng.</p>
    
    <h3>Cài đặt:</h3>
    <p>Vào <strong>Tools → MCQ Quick Answer → Cài đặt</strong> để bật/tắt tính năng.</p>
    """
    showInfo(about_text, title="Về MCQ Quick Answer")

def setup_menu():
    """Thiết lập menu"""
    # Tạo menu chính
    menu = mw.form.menuTools.addMenu("MCQ Quick Answer")
    
    # Action cài đặt
    config_action = QAction("⚙️ Cài đặt...", mw)
    config_action.triggered.connect(show_config_dialog)
    menu.addAction(config_action)
    
    menu.addSeparator()
    
    # Action về addon
    about_action = QAction("ℹ️ Về addon", mw)
    about_action.triggered.connect(show_about)
    menu.addAction(about_action)

# Wrap _answerCard
Reviewer._answerCard = wrap(Reviewer._answerCard, _answerCard_wrapper, "around")

# Hook để inject tip
gui_hooks.reviewer_did_show_question.append(inject_tip_on_show_question)

# Setup menu
gui_hooks.main_window_did_init.append(setup_menu)

print("=" * 60)
print("MCQ Quick Answer addon đã được tải!")
print("Vào Tools → MCQ Quick Answer → Cài đặt để cấu hình")
print("=" * 60)
