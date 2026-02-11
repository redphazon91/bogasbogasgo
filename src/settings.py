from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QScrollArea,
    QFrame,
)
from PyQt6.QtCore import pyqtSignal
import themes


class SettingsWidget(QWidget):
    theme_changed = pyqtSignal(str)

    def __init__(self, current_theme_name="Claro", theme=None):
        super().__init__()
        self.current_theme_name = current_theme_name
        self.theme = theme
        self.init_ui()
        self.apply_styles()

    def update_theme(self, theme):
        self.theme = theme
        # Update combo box without triggering signals
        self.theme_combo.blockSignals(True)
        self.theme_combo.setCurrentText(theme.name)
        self.theme_combo.blockSignals(False)
        self.apply_styles()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.container = QWidget()
        self.scroll.setWidget(self.container)

        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(30)

        # Header
        self.header = QLabel("Configurações")
        self.header.setStyleSheet("font-size: 32px; font-weight: bold;")
        self.main_layout.addWidget(self.header)

        # Appearance Section
        self.appearance_label = QLabel("Aparência")
        self.appearance_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; border-bottom: 2px solid #ddd; padding-bottom: 5px;"
        )
        self.main_layout.addWidget(self.appearance_label)

        # Theme Selector
        theme_layout = QHBoxLayout()
        self.theme_label = QLabel("Tema do Aplicativo")
        self.theme_label.setStyleSheet("font-size: 14px;")

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(themes.THEMES.keys()))
        self.theme_combo.setCurrentText(self.current_theme_name)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)

        theme_layout.addWidget(self.theme_label)
        theme_layout.addStretch()
        theme_layout.addWidget(self.theme_combo)
        self.main_layout.addLayout(theme_layout)

        # About Section
        self.about_label = QLabel("Sobre")
        self.about_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; border-bottom: 2px solid #ddd; padding-bottom: 5px;"
        )
        self.main_layout.addWidget(self.about_label)

        self.about_text = QLabel(
            "Bogas Bogas GO - Seu navegador e assistente pessoal.\nVersão 0.1.0"
        )
        self.main_layout.addWidget(self.about_text)

        self.main_layout.addStretch()

        layout.addWidget(self.scroll)
        self.setLayout(layout)

    def apply_styles(self):
        t = self.theme
        if not t:
            return

        text_color = t.text
        bg_color = t.bg
        secondary_text = t.secondary_text
        border_color = t.button_border

        self.setStyleSheet(f"background-color: {bg_color};")
        self.container.setStyleSheet(f"background-color: {bg_color};")

        self.header.setStyleSheet(
            f"font-size: 32px; font-weight: bold; color: {text_color};"
        )
        self.appearance_label.setStyleSheet(
            f"font-size: 18px; font-weight: bold; color: {text_color}; border-bottom: 2px solid {border_color}; padding-bottom: 5px;"
        )
        self.theme_label.setStyleSheet(f"font-size: 14px; color: {text_color};")

        self.theme_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {t.button_bg};
                color: {text_color};
                border: 1px solid {border_color};
                padding: 5px;
                min-width: 200px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {t.button_bg};
                color: {text_color};
                selection-background-color: {t.button_hover};
            }}
        """)

        self.about_label.setStyleSheet(
            f"font-size: 18px; font-weight: bold; color: {text_color}; border-bottom: 2px solid {border_color}; padding-bottom: 5px;"
        )
        self.about_text.setStyleSheet(f"color: {secondary_text}; line-height: 1.5;")

    def on_theme_changed(self, theme_name):
        self.current_theme_name = theme_name
        self.theme_changed.emit(theme_name)
