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
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
import defaults


class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(defaults.BROWSER_NAME)
        self.resize(1200, 800)

        # 1. The Web Engine View (The actual browser area)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(defaults.BROWSER_HOMEPAGE))

        # 2. Navigation Bar
        nav_bar = QHBoxLayout()

        self.back_btn = QPushButton("←")
        self.back_btn.clicked.connect(self.browser.back)

        self.forward_btn = QPushButton("→")
        self.forward_btn.clicked.connect(self.browser.forward)

        self.reload_btn = QPushButton("↻")
        self.reload_btn.clicked.connect(self.browser.reload)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        nav_bar.addWidget(self.back_btn)
        nav_bar.addWidget(self.forward_btn)
        nav_bar.addWidget(self.reload_btn)
        nav_bar.addWidget(self.url_bar)

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
                lambda _, url=favorite["url"]: self.browser.setUrl(QUrl(url))
            )
            btn.setToolTip(f'Ir para {favorite["name"]}\nem "{favorite["url"]}"')
            favorites_bar.addWidget(btn)

        # 3. Layout Setup
        layout = QVBoxLayout()
        layout.addLayout(nav_bar)
        layout.addLayout(favorites_bar)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Update URL bar when page changes
        self.browser.urlChanged.connect(self.update_url)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())


app = QApplication(sys.argv)
window = SimpleBrowser()
window.show()
sys.exit(app.exec())
