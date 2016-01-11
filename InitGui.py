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

    settingsIcon = ['16 16 2 1',
                    ' 	c None',
                    '.	c #888A85',
                    '                ',
                    '                ',
                    '  ............  ',
                    '  ............  ',
                    '                ',
                    '                ',
                    '                ',
                    '  ............  ',
                    '  ............  ',
                    '                ',
                    '                ',
                    '                ',
                    '  ............  ',
                    '  ............  ',
                    '                ',
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
    tbDockTitleBar = tbDock.titleBarWidget()

    def onControl():
        mw = FreeCADGui.getMainWindow()

        for i in mw.findChildren(QtGui.QDialog):
            if i.objectName() == "tbPreferences":
                i.deleteLater()

        tbPrefDialog = QtGui.QDialog(mw)
        tbPrefDialog.resize(600, 400)
        tbPrefDialog.setObjectName("tbPreferences")
        tbPrefDialog.setWindowTitle("TabBar")
        tbPrefDialog.show()

    def quickMenu():
        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

        menu = QtGui.QMenu()

        # TEMP
        menu.setStyleSheet("padding: 5px")
        #

        lockAction = QtGui.QAction(menu)
        lockAction.setIconText("Lock")
        lockAction.setCheckable(True)

        radioTop = QtGui.QRadioButton("Top")
        radioActionTop = QtGui.QWidgetAction(menu)
        radioActionTop.setDefaultWidget(radioTop)

        radioBottom = QtGui.QRadioButton("Bottom")
        radioActionBottom = QtGui.QWidgetAction(menu)
        radioActionBottom.setDefaultWidget(radioBottom)

        radioLeft = QtGui.QRadioButton("Left")
        radioActionLeft = QtGui.QWidgetAction(menu)
        radioActionLeft.setDefaultWidget(radioLeft)

        radioRight = QtGui.QRadioButton("Right")
        radioActionRight = QtGui.QWidgetAction(menu)
        radioActionRight.setDefaultWidget(radioRight)

        prefAction = QtGui.QAction(menu)
        prefAction.setIconText("Preferences")
        prefButton = QtGui.QToolButton()
        prefButton.setDefaultAction(prefAction)
        prefButtonAction = QtGui.QWidgetAction(menu)
        prefButtonAction.setDefaultWidget(prefButton)

        menu.addAction(lockAction)
        menu.addSeparator()
        menu.addAction(radioActionTop)
        menu.addAction(radioActionBottom)
        menu.addAction(radioActionLeft)
        menu.addAction(radioActionRight)
        menu.addSeparator()
        menu.addAction(prefButtonAction)

        menuButton = QtGui.QToolButton()
        menuButton.setMenu(menu)
        menuButton.setAutoRaise(True)
        menuButton.setIcon(QtGui.QIcon(QtGui.QPixmap(settingsIcon)))
        menuButton.setPopupMode(QtGui.QToolButton
                                .ToolButtonPopupMode.InstantPopup)

        def toTop():
            if radioTop.isChecked():
                tbTabs.setTabPosition(QtGui.QTabWidget.North)
                paramGet.SetString("Position", "North")
            else:
                pass

        radioTop.toggled.connect(toTop)

        def toBottom():
            if radioBottom.isChecked():
                tbTabs.setTabPosition(QtGui.QTabWidget.South)
                paramGet.SetString("Position", "South")
            else:
                pass

        radioBottom.toggled.connect(toBottom)

        def toLeft():
            if radioLeft.isChecked():
                tbTabs.setTabPosition(QtGui.QTabWidget.West)
                paramGet.SetString("Position", "West")
            else:
                pass

        radioLeft.toggled.connect(toLeft)

        def toRight():
            if radioRight.isChecked():
                tbTabs.setTabPosition(QtGui.QTabWidget.East)
                paramGet.SetString("Position", "East")
            else:
                pass

        radioRight.toggled.connect(toRight)

        def onLockToggle():
            if lockAction.isChecked():
                tbDock.setTitleBarWidget(QtGui.QWidget(None))
                paramGet.SetBool("Lock", 1)
            else:
                tbDock.setTitleBarWidget(tbDockTitleBar)
                paramGet.SetBool("Lock", 0)

        lockAction.changed.connect(onLockToggle)

        prefButton.clicked.connect(onControl)

        def onOpen():
            if paramGet.GetString("Position"):
                if paramGet.GetString("Position") == "North":
                    radioTop.setChecked(True)
                elif paramGet.GetString("Position") == "South":
                    radioBottom.setChecked(True)
                elif paramGet.GetString("Position") == "West":
                    radioLeft.setChecked(True)
                elif paramGet.GetString("Position") == "East":
                    radioRight.setChecked(True)
            else:
                radioTop.setChecked(True)

            if paramGet.GetBool("Lock"):
                lockAction.setChecked(True)
            else:
                lockAction.setChecked(False)

        menu.aboutToShow.connect(onOpen)

        onOpen()

        return menuButton

    def addTabs():
        wbList = FreeCADGui.listWorkbenches()

        for i in wbList:
            widget = QtGui.QWidget()

            # TEMP
            btn = quickMenu()
            btn.resize(32, 32)
            btn.setParent(widget)
            #

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
