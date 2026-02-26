from PyQt5 import QtGui, QtWidgets


def undo_button_press(buttonObj, released_text='Released',
                      pressed_text='Pressed'):
    """
    recover checkable pushButton status when error occurs

    :param buttonObj: pyqt4 pushButton object
    :param released_text: text label of the button when released
    :param pressed_text: text label of the button when pressed
    """
    if buttonObj.isChecked():
        buttonObj.setChecked(False)
        buttonObj.setText(released_text)
    else:
        buttonObj.setChecked(True)
        buttonObj.setText(pressed_text)
    return


class SpinBoxFixStyle(QtWidgets.QProxyStyle):
    """
    Copied from https://stackoverflow.com/questions/40746350/why-qspinbox-jumps-twice-the-step-value
    To fix the SpinBox button problem.  This fixes SpinBoxes issuing events
    twice.
    """

    def styleHint(self, hint, option=None, widget=None, returnData=None):
        if hint == QtWidgets.QStyle.SH_SpinBox_KeyPressAutoRepeatRate:
            return 5**10
        elif hint == QtWidgets.QStyle.SH_SpinBox_ClickAutoRepeatRate:
            return 5**10
        elif hint == QtWidgets.QStyle.SH_SpinBox_ClickAutoRepeatThreshold:
            # You can use only this condition to avoid the auto-repeat,
            # but better safe than sorry ;-)
            return 5**10
        else:
            return super().styleHint(hint, option, widget, returnData)


def apply_dark_palette(app):
    """
    Apply a native Qt dark palette for PyQt5 apps.
    """
    app.setStyle("Fusion")
    dark_palette = QtGui.QPalette()
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
    dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(35, 35, 35))
    dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(255, 255, 255))
    dark_palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(255, 255, 255))
    dark_palette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
    dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))
    dark_palette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255, 0, 0))
    dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 0, 0))
    dark_palette.setColor(
        QtGui.QPalette.Disabled,
        QtGui.QPalette.ButtonText,
        QtGui.QColor(127, 127, 127),
    )
    dark_palette.setColor(
        QtGui.QPalette.Disabled,
        QtGui.QPalette.WindowText,
        QtGui.QColor(127, 127, 127),
    )
    dark_palette.setColor(
        QtGui.QPalette.Disabled,
        QtGui.QPalette.Text,
        QtGui.QColor(127, 127, 127),
    )
    dark_palette.setColor(
        QtGui.QPalette.Disabled,
        QtGui.QPalette.Light,
        QtGui.QColor(53, 53, 53),
    )

    app.setPalette(dark_palette)
