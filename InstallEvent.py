# License: CC BY-SA 3.0
# https://creativecommons.org/licenses/by-sa/3.0/legalcode
# Attribution:
# http://stackoverflow.com/a/34478089

from PySide.QtGui import QApplication, QWheelEvent
from PySide.QtCore import QEvent, QObject


class InstallEvent(QObject):

    def eventFilter(self, obj, event):
        if obj and not obj.isEnabled() and event.type() == QEvent.Wheel:
            newEvent = QWheelEvent(obj.mapToParent(event.pos()), event.globalPos(),
                                   event.delta(), event.buttons(),
                                   event.modifiers(), event.orientation())
            QApplication.instance().postEvent(obj.parent(), newEvent)
            return True

        return QObject.eventFilter(self, obj, event)
