from PyQt5.QtWidgets import QApplication

from logic import *


def main() -> None:
    """
    Sets up Gui
    :return: NONE
    """
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()


if __name__ == '__main__':
    main()
