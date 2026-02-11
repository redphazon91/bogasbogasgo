from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QGridLayout,
    QMessageBox,
)
from PyQt6.QtCore import Qt


class SuaBandaWidget(QWidget):
    def __init__(self, theme=None, use_theme_font=True):
        super().__init__()
        self.theme = theme
        self.use_theme_font = use_theme_font
        self.utility_buttons = []
        self.init_ui()
        self.apply_styles()

    def update_theme(self, theme, use_theme_font=None):
        self.theme = theme
        if use_theme_font is not None:
            self.use_theme_font = use_theme_font
        self.apply_styles()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # Header
        self.header = QLabel("SuaBanda - Assistente Pessoal")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.header)

        # Description
        self.desc = QLabel(
            "Bem-vindo à sua central de utilitários. Escolha uma das ferramentas abaixo para começar."
        )
        self.desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.desc)

        # Grid for utilities
        self.grid = QGridLayout()
        self.grid.setSpacing(15)

        utilities = [
            ("Calculadora", "🧮", self.not_implemented),
            ("Gerador de Senhas", "🔑", self.not_implemented),
            ("Anotações", "📝", self.not_implemented),
            ("Cronômetro", "⏱️", self.not_implemented),
            ("Conversor de Moedas", "💱", self.not_implemented),
            ("Lista de Tarefas", "✅", self.not_implemented),
        ]

        row = 0
        col = 0
        for name, icon, callback in utilities:
            btn = self.create_utility_button(name, icon, callback)
            self.utility_buttons.append(btn)
            self.grid.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.main_layout.addLayout(self.grid)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def apply_styles(self):
        t = self.theme
        if not t:
            bg_color = "#f5f5f5"
            text_color = "#000000"
            secondary_text = "#666666"
            button_bg = "white"
            button_border = "#dddddd"
            button_hover = "#e9e9e9"
        else:
            bg_color = t.bg
            text_color = t.text
            secondary_text = t.secondary_text
            button_bg = t.button_bg
            button_border = t.button_border
            button_hover = t.button_hover

        font_family = t.font_family if self.use_theme_font else ""

        self.setStyleSheet(f"background-color: {bg_color}; font-family: {font_family};")

        self.header.setStyleSheet(
            f"font-size: 24px; font-weight: bold; margin-bottom: 10px; color: {text_color}; background: transparent;"
        )
        self.desc.setStyleSheet(
            f"font-size: 14px; color: {secondary_text}; margin-bottom: 20px; background: transparent;"
        )

        button_css = f"""
            QPushButton {{
                background-color: {button_bg};
                border: 1px solid {button_border};
                border-radius: 10px;
                padding: 20px;
                font-size: 16px;
                min-width: 150px;
                min-height: 100px;
                color: {text_color};
            }}
            QPushButton:hover {{
                background-color: {button_hover};
                color: {t.button_text_hover if t else "#000000"};
            }}
        """

        for btn in self.utility_buttons:
            btn.setStyleSheet(button_css)
            # Find labels inside the button and set transparency
            # (Note: we already set transparent background in create_utility_button,
            # but let's be sure the labels are styled correct if needed)

    def create_utility_button(self, name, icon, callback):
        btn = QPushButton()
        btn_layout = QVBoxLayout(btn)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 32px; background: transparent;")

        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("font-weight: bold; background: transparent;")

        btn_layout.addWidget(icon_label)
        btn_layout.addWidget(name_label)

        btn.clicked.connect(callback)
        return btn

    def not_implemented(self):
        QMessageBox.information(
            self,
            "Em desenvolvimento",
            "Esta funcionalidade será implementada em breve!",
        )
