from PySide6.QtWidgets import QApplication
from utils import *
from windows import *

import sys


if __name__ == "__main__":
    app = QApplication()

    form = Form()
    form.show()

    sys.exit(app.exec())
