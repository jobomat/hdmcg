from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QBuffer, QUrl
from PySide6.QtGui import QMovie
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

_URL = 'https://cataas.com/cat/gif'


class CatWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.WindowType.Window)
        self.setWindowTitle('Cat')

        self._nam = QNetworkAccessManager(self)
        self._reply = None
        self._movie = None
        self._buf = None

        self._label = QLabel('Loading...')
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._next_btn = QPushButton('I need one more cat')
        self._next_btn.clicked.connect(self._fetch)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self._label)
        layout.addWidget(self._next_btn)
        self.setCentralWidget(central)

        self._fetch()

    def _fetch(self):
        self._label.setText('Please wait. Yout cat is being prepared...')
        if self._movie:
            self._movie.stop()
        if self._reply is not None:
            self._reply.abort()
            self._reply = None
        self._reply = self._nam.get(QNetworkRequest(QUrl(_URL)))
        self._reply.finished.connect(self._on_reply)

    def _on_reply(self):
        reply, self._reply = self._reply, None
        if reply.error() == QNetworkReply.NetworkError.NoError:
            data = reply.readAll()
            self._buf = QBuffer()
            self._buf.setData(data)
            self._buf.open(QBuffer.OpenModeFlag.ReadOnly)
            self._movie = QMovie()
            self._movie.setDevice(self._buf)
            self._label.setMovie(self._movie)
            self._movie.frameChanged.connect(self._fit_to_movie)
            self._movie.start()
        else:
            self._label.setText(f'Error: {reply.errorString()}')
        reply.deleteLater()

    def _fit_to_movie(self):
        self._movie.frameChanged.disconnect(self._fit_to_movie)
        gif = self._movie.currentPixmap().size()
        self._label.setFixedSize(gif)
        layout = self.centralWidget().layout()
        m = layout.contentsMargins()
        w = gif.width() + m.left() + m.right()
        h = gif.height() + self._next_btn.sizeHint().height() + layout.spacing() + m.top() + m.bottom()
        self.setMinimumSize(0, 0)
        self.resize(w, h)
