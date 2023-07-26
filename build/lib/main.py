from PySide6.QtWidgets import QApplication
from windows.MainWindow import Form

import sys

app = QApplication()

form = Form()
form.show()

sys.exit(app.exec())
