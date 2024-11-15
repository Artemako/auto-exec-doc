from PySide6 import QtCore
from PySide6.QtWidgets import (
    QWidget,
    QScrollArea,
    QFrame,
    QToolButton,
    QGridLayout,
    QSizePolicy,
)
from PySide6 import QtGui


class Section(QWidget):
    def __init__(self, osbm, section_id, section_name, sections_checked, is_checked):
        """
        References:
            # Adapted from c++ version
            http://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt
        """
        self.__osbm = osbm
        self.__section_id = section_id
        self.__section_name = section_name
        self.__sections_checked = sections_checked
        self.__is_checked = is_checked
        super(Section, self).__init__(None)

        self.__osbm.obj_style.set_style_for(self)

        self.animationDuration = 50
        self.toggleAnimation = QtCore.QParallelAnimationGroup()
        self.contentArea = QScrollArea()
        self.headerLine = QFrame()
        self.toggleButton = QToolButton()
        self.mainLayout = QGridLayout()

        toggleButton = self.toggleButton
        toggleButton.setStyleSheet("QToolButton { border: none; }")
        toggleButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        toggleButton.setArrowType(QtCore.Qt.RightArrow)

        metrics = QtGui.QFontMetrics(self.toggleButton.font())
        toggleButton.setText(
            metrics.elidedText(self.__section_name, QtCore.Qt.ElideRight, 300)
        )
        toggleButton.setCheckable(True)
        toggleButton.setChecked(self.__is_checked)

        headerLine = self.headerLine
        headerLine.setFrameShape(QFrame.HLine)
        headerLine.setFrameShadow(QFrame.Sunken)
        headerLine.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        headerLine.setStyleSheet("QFrame { background-color: #3F3F46; }")

        self.contentArea.setStyleSheet("QScrollArea { border: none; }")
        self.contentArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # start out collapsed
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)
        # let the entire widget grow and shrink with its content
        toggleAnimation = self.toggleAnimation
        toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self, b"minimumHeight"))
        toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self, b"maximumHeight"))
        toggleAnimation.addAnimation(
            QtCore.QPropertyAnimation(self.contentArea, b"maximumHeight")
        )
        # don't waste space
        mainLayout = self.mainLayout
        mainLayout.setVerticalSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        row = 0
        mainLayout.addWidget(self.toggleButton, row, 0, 1, 1, QtCore.Qt.AlignLeft)
        mainLayout.addWidget(self.headerLine, row, 2, 1, 1)
        row += 1
        mainLayout.addWidget(self.contentArea, row, 0, 1, 3)
        self.setLayout(self.mainLayout)

        def start_animation(checked):
            print(f"checked = {checked}")
            arrow_type = QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow
            direction = (
                QtCore.QAbstractAnimation.Forward
                if checked
                else QtCore.QAbstractAnimation.Backward
            )
            toggleButton.setArrowType(arrow_type)
            self.toggleAnimation.setDirection(direction)
            self.toggleAnimation.start()
            self.__sections_checked[self.__section_id] = checked

        self.toggleButton.clicked.connect(start_animation)

        if self.__is_checked:
            start_animation(self.__is_checked)

    def setContentLayout(self, contentLayout):
        # Not sure if this is equivalent to self.contentArea.destroy()
        self.contentArea.destroy()
        self.contentArea.setLayout(contentLayout)
        collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
        contentHeight = contentLayout.sizeHint().height()
        for i in range(self.toggleAnimation.animationCount() - 1):
            SectionAnimation = self.toggleAnimation.animationAt(i)
            SectionAnimation.setDuration(self.animationDuration)
            SectionAnimation.setStartValue(collapsedHeight)
            SectionAnimation.setEndValue(collapsedHeight + contentHeight)
        contentAnimation = self.toggleAnimation.animationAt(
            self.toggleAnimation.animationCount() - 1
        )
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)
