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


class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.back_btn.clicked.connect(lambda: self.current_browser().back())

        self.forward_btn = QPushButton("→")
        self.forward_btn.clicked.connect(lambda: self.current_browser().forward())

        self.reload_btn = QPushButton("↻")
        self.reload_btn.clicked.connect(lambda: self.current_browser().reload())

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.new_tab_btn = QToolButton()
        self.new_tab_btn.setText("+")
        self.new_tab_btn.clicked.connect(lambda: self.add_new_tab())

        nav_bar.addWidget(self.back_btn)
        nav_bar.addWidget(self.forward_btn)
        nav_bar.addWidget(self.reload_btn)
        nav_bar.addWidget(self.url_bar)
        nav_bar.addWidget(self.new_tab_btn)

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
            btn.clicked.connect(
                lambda _, url=favorite["url"]: self.current_browser().setUrl(QUrl(url))
            )
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
        qurl = self.current_browser().url()
        self.update_url_bar(qurl, self.current_browser())
        self.update_title(self.current_browser())

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.current_browser().setUrl(QUrl(url))

    def update_url_bar(self, q, browser=None):
        if browser != self.current_browser():
            return
        self.url_bar.setText(q.toString())

    def update_title(self, browser):
        if browser != self.current_browser():
            return
        title = self.current_browser().page().title()
        self.setWindowTitle(f"{title} - {defaults.BROWSER_NAME}")


app = QApplication(sys.argv)
window = SimpleBrowser()
window.show()
sys.exit(app.exec())
