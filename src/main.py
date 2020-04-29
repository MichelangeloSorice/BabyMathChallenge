from PyQt5.QtWidgets import QApplication

from fingerdetection_app import FingerDetectionApp

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    babymath_app = FingerDetectionApp()
    babymath_app.setWindowTitle('Finger Detection')
    babymath_app.show()
    sys.exit(app.exec_())
