"""Application entry point."""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from .main_window import MainWindow


def main():
    """Run the text editor application."""
    app = QApplication(sys.argv)
    app.setApplicationName("TextEdit")
    app.setApplicationVersion("0.1.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
