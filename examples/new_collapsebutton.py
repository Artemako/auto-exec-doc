from PySide2.QtWidgets import QToolButton, QApplication, QMainWindow
from PySide2.QtCore import QSize, Qt, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QAbstractAnimation
import sys

class CollapseButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.content_ = None
        self.setCheckable(True)
        self.setStyleSheet("background:none")
        self.setIconSize(QSize(8, 8))
        self.setFont(QApplication.font())
        self.toggled.connect(self.on_toggled)

    def setText(self, text):
        QToolButton.setText(self, " " + text)

    def setContent(self, content):
        assert(content is not None)
        self.content_ = content
        animation = QPropertyAnimation(content, b"maximumHeight")
        animation.setStartValue(0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.setDuration(300)
        animation.setEndValue(content.geometry().height() + 10)
        self.animator_.addAnimation(animation)
        if not self.isChecked():
            content.setMaximumHeight(0)

    def hideContent(self):
        self.animator_.setDirection(QAbstractAnimation.Backward)
        self.animator_.start()

    def showContent(self):
        self.animator_.setDirection(QAbstractAnimation.Forward)
        self.animator_.start()

    def on_toggled(self, checked):
        self.setArrowType(Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow)
        if checked and self.content_ is not None:
            self.showContent()
        else:
            self.hideContent()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.animator_ = QParallelAnimationGroup(self)


if __name__ == "__main__":
    app = QApplication([])
    window = CollapseButton()
    window.show()
    sys.exit(app.exec())