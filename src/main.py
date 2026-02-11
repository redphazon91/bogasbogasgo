import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QTabWidget,
    QToolButton,
    QMessageBox,
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
import defaults
from sua_banda import SuaBandaWidget
from settings import SettingsWidget
import themes
import json
import os


class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "config.json"
        )
        self.load_settings()
        self.setWindowTitle(defaults.BROWSER_NAME)
        self.resize(1200, 800)

        # 1. Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.tab_changed)

        # 2. Navigation Bar
        nav_bar = QHBoxLayout()

        self.back_btn = QPushButton("←")
        self.back_btn.clicked.connect(self.back_clicked)

        self.forward_btn = QPushButton("→")
        self.forward_btn.clicked.connect(self.forward_clicked)

        self.reload_btn = QPushButton("↻")
        self.reload_btn.clicked.connect(self.reload_clicked)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.new_tab_btn = QToolButton()
        self.new_tab_btn.setText("+")
        self.new_tab_btn.clicked.connect(lambda: self.add_new_tab())

        self.sua_banda_btn = QPushButton("SuaBanda")
        self.sua_banda_btn.clicked.connect(self.add_sua_banda_tab)
        self.sua_banda_btn.setStyleSheet("font-weight: bold; color: #d63384;")

        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.clicked.connect(self.add_settings_tab)
        self.settings_btn.setToolTip("Configurações")

        nav_bar.addWidget(self.back_btn)
        nav_bar.addWidget(self.forward_btn)
        nav_bar.addWidget(self.reload_btn)
        nav_bar.addWidget(self.url_bar)
        nav_bar.addWidget(self.new_tab_btn)
        nav_bar.addWidget(self.sua_banda_btn)
        nav_bar.addWidget(self.settings_btn)

        # 3. Favorites Bar
        favorites_bar = QHBoxLayout()

        self.favorites = [
            {
                "name": "X",
                "url": r"https://x.com/aied_online",
            },
            {
                "name": "GitHub",
                "url": r"https://github.com/naoimportaweb",
            },
            {
                "name": "Angadosu (YouTube)",
                "url": r"https://www.youtube.com/@angado_su/featured",
            },
        ]

        for favorite in self.favorites:
            btn = QPushButton(favorite["name"])
            btn.clicked.connect(lambda _, url=favorite["url"]: self.open_url(QUrl(url)))
            btn.setToolTip(f'Ir para {favorite["name"]}\nem "{favorite["url"]}"')
            favorites_bar.addWidget(btn)

        # 4. Layout Setup
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Container for bars to have some padding
        bars_container = QVBoxLayout()
        bars_container.setContentsMargins(5, 5, 5, 5)
        bars_container.addLayout(nav_bar)
        bars_container.addLayout(favorites_bar)

        layout.addLayout(bars_container)
        layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Add initial tab
        self.add_new_tab(QUrl(defaults.BROWSER_HOMEPAGE), "Home")
        self.apply_theme()

    def back_clicked(self):
        browser = self.current_browser()
        if isinstance(browser, QWebEngineView):
            browser.back()

    def forward_clicked(self):
        browser = self.current_browser()
        if isinstance(browser, QWebEngineView):
            browser.forward()

    def reload_clicked(self):
        browser = self.current_browser()
        if isinstance(browser, QWebEngineView):
            browser.reload()

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl(defaults.BROWSER_HOMEPAGE)

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # Update local UI when this browser's URL or Title changes
        browser.urlChanged.connect(
            lambda qurl, browser=browser: self.update_url_bar(qurl, browser)
        )
        browser.loadFinished.connect(
            lambda _, i=i, browser=browser: self.tabs.setTabText(
                i, browser.page().title()
            )
        )

    def change_theme(self, theme_name):
        new_theme = themes.THEMES.get(theme_name)
        if new_theme:
            self.current_theme = new_theme
            self.apply_theme()
            self.save_settings()

    def change_font_setting(self, use_theme_font):
        self.use_theme_font = use_theme_font
        self.apply_theme()
        self.save_settings()

    def apply_theme(self):
        # Update all tabs
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if isinstance(widget, (SuaBandaWidget, SettingsWidget)):
                widget.update_theme(
                    self.current_theme, use_theme_font=self.use_theme_font
                )

        # Update main window and bar styles
        self.update_styles()

    def load_settings(self):
        theme_name = "Claro"
        self.use_theme_font = True
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    data = json.load(f)
                    theme_name = data.get("theme", "Claro")
                    self.use_theme_font = data.get("use_theme_font", True)
            except Exception as e:
                print(f"Error loading settings: {e}")

        self.current_theme = themes.THEMES.get(theme_name, themes.LIGHT)

    def save_settings(self):
        data = {"theme": self.current_theme.name, "use_theme_font": self.use_theme_font}
        try:
            with open(self.settings_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def add_settings_tab(self):
        # Check if settings tab already exists
        for i in range(self.tabs.count()):
            if isinstance(self.tabs.widget(i), SettingsWidget):
                self.tabs.setCurrentIndex(i)
                return

        settings = SettingsWidget(
            current_theme_name=self.current_theme.name,
            theme=self.current_theme,
            use_theme_font=self.use_theme_font,
        )
        settings.theme_changed.connect(self.change_theme)
        settings.font_setting_changed.connect(self.change_font_setting)
        i = self.tabs.addTab(settings, "Configurações")
        self.tabs.setCurrentIndex(i)

    def update_styles(self):
        t = self.current_theme
        font_family = t.font_family if self.use_theme_font else "inherit"
        self.setStyleSheet(f"""
            * {{
                font-family: {font_family};
            }}
            QMainWindow {{
                background-color: {t.bg};
            }}
            QTabWidget::pane {{
                border-top: 1px solid {t.button_border};
                background-color: {t.bg};
            }}
            QTabBar::tab {{
                background-color: {t.tab_inactive_bg};
                color: {t.tab_inactive_text};
                padding: 10px;
                border: 1px solid {t.button_border};
                border-bottom: none;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }}
            QTabBar::tab:selected {{
                background-color: {t.tab_active_bg};
                color: {t.tab_active_text};
                border-bottom: 2px solid {t.tab_active_bg};
            }}
            QTabBar::tab:hover {{
                background-color: {t.tab_hover_bg};
                color: {t.tab_hover_text};
            }}
            QLineEdit {{
                background-color: {t.input_bg};
                color: {t.input_text};
                border: 1px solid {t.button_border};
                padding: 5px;
                border-radius: 4px;
            }}
            QPushButton {{
                background-color: {t.button_bg};
                color: {t.text};
                border: 1px solid {t.button_border};
                padding: 5px 10px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {t.button_hover};
                color: {t.button_text_hover};
            }}
            QComboBox {{
                background-color: {t.button_bg};
                color: {t.text};
                border: 1px solid {t.button_border};
                padding: 2px 5px;
            }}
        """)
        # Specific overrides
        self.sua_banda_btn.setStyleSheet(
            f"font-weight: bold; color: #d63384; background-color: {t.button_bg}; border: 1px solid {t.button_border};"
        )
        self.settings_btn.setStyleSheet(
            f"background-color: {t.button_bg}; border: 1px solid {t.button_border}; color: {t.text};"
        )

    def add_sua_banda_tab(self):
        # Check if SuaBanda tab already exists
        for i in range(self.tabs.count()):
            if isinstance(self.tabs.widget(i), SuaBandaWidget):
                self.tabs.setCurrentIndex(i)
                return

        sua_banda = SuaBandaWidget(
            theme=self.current_theme, use_theme_font=self.use_theme_font
        )
        i = self.tabs.addTab(sua_banda, "SuaBanda")
        self.tabs.setCurrentIndex(i)

    def current_browser(self):
        return self.tabs.currentWidget()

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            reply = QMessageBox.question(
                self,
                "Close Browser?",
                "This is the last tab. Do you want to close the application?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                QApplication.quit()
            return
        self.tabs.removeTab(i)

    def tab_changed(self, i):
        widget = self.tabs.widget(i)
        if isinstance(widget, QWebEngineView):
            qurl = widget.url()
            self.update_url_bar(qurl, widget)
            self.update_title(widget)
        else:
            self.url_bar.setText("")
            self.update_title(widget)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url:
            return
        if not url.startswith("http"):
            url = "https://" + url
        self.open_url(QUrl(url))

    def open_url(self, qurl):
        browser = self.current_browser()
        if isinstance(browser, QWebEngineView):
            browser.setUrl(qurl)
        else:
            self.add_new_tab(qurl)

    def update_url_bar(self, q, browser=None):
        if browser != self.current_browser():
            return
        if q:
            self.url_bar.setText(q.toString())

    def update_title(self, browser):
        if browser != self.current_browser():
            return
        if hasattr(browser, "page"):
            title = browser.page().title()
            self.setWindowTitle(f"{title} - {defaults.BROWSER_NAME}")
        else:
            self.setWindowTitle(f"SuaBanda - {defaults.BROWSER_NAME}")


app = QApplication(sys.argv)
window = SimpleBrowser()
window.show()
sys.exit(app.exec())
