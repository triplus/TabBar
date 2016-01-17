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

    def wbIcon(i):

        if str(i.find("XPM")) != "-1":
            icon = QtGui.QIcon(QtGui.QPixmap(xpmParse(i)))
        else:
            icon = QtGui.QIcon(QtGui.QPixmap(i))

        if icon.pixmap(QSize(16, 16)).isNull():
            icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))
        else:
            pass
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
        widget.setMovable(True)
        return widget

    tbTabs = tabWidget()
    tbDock.setWidget(tbTabs)
    tbDockTitleBar = tbDock.titleBarWidget()

    def tabPrefGeneral():
        groupTabStyle = QtGui.QGroupBox("Tab style:")
        layoutTabStyle = QtGui.QVBoxLayout()
        groupTabStyle.setLayout(layoutTabStyle)

        radioTabStyleDefault = QtGui.QRadioButton("Default")
        radioTabStyleIcon = QtGui.QRadioButton("Icon")
        radioTabStyleText = QtGui.QRadioButton("Text")

        layoutTabStyle.addWidget(radioTabStyleDefault)
        layoutTabStyle.addWidget(radioTabStyleIcon)
        layoutTabStyle.addWidget(radioTabStyleText)
        layoutTabStyle.addStretch(1)

        def onTabStyleDefault():
            paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

            if radioTabStyleDefault.isChecked():
                for i in xrange(tbTabs.count()):
                    try:
                        icon = wbIcon((FreeCADGui
                                      .getWorkbench(tbTabs.widget(i)
                                       .objectName())).Icon)
                    except:
                        icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))
                    tbTabs.setTabIcon(i, icon)
                    tbTabs.setTabText(i, tbTabs.widget(i).windowTitle())
                paramGet.SetString("TabStyle", "Default")
            else:
                pass

        radioTabStyleDefault.toggled.connect(onTabStyleDefault)

        def onTabStyleIcon():
            paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

            if radioTabStyleIcon.isChecked():
                for i in xrange(tbTabs.count()):
                    try:
                        icon = wbIcon((FreeCADGui
                                      .getWorkbench(tbTabs.widget(i)
                                       .objectName())).Icon)
                    except:
                        icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))
                    tbTabs.setTabText(i, "")
                    tbTabs.setTabIcon(i, icon)
                paramGet.SetString("TabStyle", "Icon")
            else:
                pass

        radioTabStyleIcon.toggled.connect(onTabStyleIcon)

        def onTabStyleText():
            paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

            if radioTabStyleText.isChecked():
                for i in xrange(tbTabs.count()):
                    tbTabs.setTabIcon(i, QtGui.QIcon())
                    tbTabs.setTabText(i, tbTabs.widget(i).windowTitle())
                paramGet.SetString("TabStyle", "Text")
            else:
                pass

        radioTabStyleText.toggled.connect(onTabStyleText)

        widgetGeneral = QtGui.QWidget()
        layoutGeneral = QtGui.QHBoxLayout()
        widgetGeneral.setLayout(layoutGeneral)

        layoutGeneralLeft = QtGui.QVBoxLayout()
        layoutGeneral.addLayout(layoutGeneralLeft)
        layoutGeneralLeft.addWidget(groupTabStyle)

        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

        if paramGet.GetString("TabStyle"):
            if paramGet.GetString("TabStyle") == "Default":
                radioTabStyleDefault.setChecked(True)
            elif paramGet.GetString("TabStyle") == "Icon":
                radioTabStyleIcon.setChecked(True)
            elif paramGet.GetString("TabStyle") == "Text":
                radioTabStyleText.setChecked(True)
        else:
            radioTabStyleDefault.setChecked(True)

        return widgetGeneral

    def onControl():
        mw = FreeCADGui.getMainWindow()

        for i in mw.findChildren(QtGui.QDialog):
            if i.objectName() == "tbPreferences":
                i.deleteLater()

        tbPrefDialog = QtGui.QDialog(mw)
        tbPrefDialog.resize(600, 400)
        tbPrefDialog.setObjectName("tbPreferences")
        tbPrefDialog.setWindowTitle("TabBar")
        tbPrefDialogLayout = QtGui.QVBoxLayout()
        tbPrefDialog.setLayout(tbPrefDialogLayout)
        tbPrefDialog.show()

        tbPrefTabs = QtGui.QTabWidget()
        tbPrefDialogLayout.addWidget(tbPrefTabs)

        tbPrefTabs.addTab(tabPrefGeneral(), "General")

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
        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")
        paramWBGet = App.ParamGet("User parameter:BaseApp/Workbenches")

        unsortedWBList = []
        for i in wbList:
            unsortedWBList.append(i)

        sortedWBList = sorted(unsortedWBList)

        if paramWBGet.GetString("Disabled"):
            disabledWB = (((paramWBGet.GetString("Disabled"))
                          .rsplit(',', 1)[0])
                          .split(","))
            for i in disabledWB:
                if i in sortedWBList:
                    sortedWBList.remove(i)
        else:
            pass

        if paramWBGet.GetString("Enabled"):
            tempWBList = []
            enabledWB = (((paramWBGet.GetString("Enabled"))
                         .rsplit(',', 1)[0])
                         .split(","))
            for i in enabledWB:
                if i in sortedWBList:
                    tempWBList.append(i)
            sortedWBList = tempWBList
        else:
            pass

        for i in sortedWBList:
            if i in wbList:
                widget = QtGui.QWidget()
                widget.setObjectName(i)

                # TEMP
                widget.setWindowTitle(wbList[i].MenuText)
                btn = quickMenu()
                btn.resize(32, 32)
                btn.setParent(widget)
                #

                try:
                    icon = wbIcon(wbList[i].Icon)
                except:
                    icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))

                if paramGet.GetString("TabStyle"):
                    if paramGet.GetString("TabStyle") == "Default":
                        tbTabs.addTab(widget, icon, wbList[i].MenuText)
                    elif paramGet.GetString("TabStyle") == "Icon":
                        tbTabs.addTab(widget, icon, "")
                    elif paramGet.GetString("TabStyle") == "Text":
                        tbTabs.addTab(widget, wbList[i].MenuText)
                else:
                    tbTabs.addTab(widget, icon, wbList[i].MenuText)

                tbTabs.setTabToolTip(tbTabs.indexOf(widget), wbList[i].ToolTip)

    addTabs()

    def afterStart():
        mw = FreeCADGui.getMainWindow()
        paramGet = App.ParamGet("User parameter:BaseApp/TabBar")

        if paramGet.GetString("Position"):
            if paramGet.GetString("Position") == "North":
                tbTabs.setTabPosition(QtGui.QTabWidget.North)
            elif paramGet.GetString("Position") == "South":
                tbTabs.setTabPosition(QtGui.QTabWidget.South)
            elif paramGet.GetString("Position") == "West":
                tbTabs.setTabPosition(QtGui.QTabWidget.West)
            elif paramGet.GetString("Position") == "East":
                tbTabs.setTabPosition(QtGui.QTabWidget.East)
        else:
            tbTabs.setTabPosition(QtGui.QTabWidget.North)

        if paramGet.GetBool("Lock"):
            tbDock.setTitleBarWidget(QtGui.QWidget(None))
        else:
            tbDock.setTitleBarWidget(tbDockTitleBar)

        activeWB = Gui.activeWorkbench().name()

        # TEMP
        for i in mw.findChildren(QtGui.QWidget):
        #
            if i.objectName() == activeWB:
                tbTabs.setCurrentIndex(tbTabs.indexOf(i))

    afterStart()

timer = QtCore.QTimer()
timer.setSingleShot(True)
timer.timeout.connect(guiUp)
timer.start(1000)
FreeCAD.timer = timer
