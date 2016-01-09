from PySide import QtCore


def singleInstance():
    from PySide import QtGui

    mw = FreeCADGui.getMainWindow()
    if mw:
        for i in mw.findChildren(QtGui.QDockWidget):
            if i.objectName() == "TabBar":
                i.deleteLater()

singleInstance()


def dockWidget():
    from PySide import QtGui
    from PySide import QtCore

    widget = QtGui.QDockWidget()
    widget.setWindowTitle("TabBar")
    widget.setObjectName("TabBar")
    mw = FreeCADGui.getMainWindow()
    if mw:
        mw.addDockWidget(QtCore.Qt.TopDockWidgetArea, widget)
    return widget

dockWidget()


def guiUp():
    from PySide import QtCore
    from PySide import QtGui
    from PySide.QtCore import QSize

    noneIcon = ['16 16 3 1',
                ' 	c None',
                '.	c #CC0000',
                '+	c #204A87',
                '                ',
                ' ............   ',
                ' .              ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                ' .            + ',
                '              + ',
                '   ++++++++++++ ',
                '                ']

    def xpmParse(i):
        icon = []
        for a in ((((i
                  .split('{', 1)[1])
                  .rsplit('}', 1)[0])
                  .strip())
                  .split("\n")):
            icon.append((a
                        .split('"', 1)[1])
                        .rsplit('"', 1)[0])
        return icon

    def findDockWidget():
        mw = FreeCADGui.getMainWindow()

        for i in mw.findChildren(QtGui.QDockWidget):
            if i.objectName() == "TabBar":
                dockWidget = i
        return dockWidget

    tbDock = findDockWidget()

    def tabWidget():
        widget = QtGui.QTabWidget()
        return widget

    tbTabs = tabWidget()
    tbDock.setWidget(tbTabs)

    def addTabs():
        wbList = FreeCADGui.listWorkbenches()

        for i in wbList:
            widget = QtGui.QWidget()

            try:
                icon = wbList[i].Icon

                if str(icon.find("XPM")) != "-1":
                    icon = QtGui.QIcon(QtGui.QPixmap(xpmParse(icon)))
                else:
                    icon = QtGui.QIcon(QtGui.QPixmap(icon))

                if icon.pixmap(QSize(16, 16)).isNull():
                    icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))
                else:
                    pass

                tbTabs.addTab(widget, icon, wbList[i].MenuText)

            except:
                icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))
                tbTabs.addTab(widget, icon, wbList[i].MenuText)

            tbTabs.setTabToolTip(tbTabs.indexOf(widget), wbList[i].ToolTip)

    addTabs()

timer = QtCore.QTimer()
timer.setSingleShot(True)
timer.timeout.connect(guiUp)
timer.start(1000)
FreeCAD.timer = timer
