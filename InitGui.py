#TabBar widget for FreeCAD
#Copyright (C) 2015, 2016  triplus @ FreeCAD
#
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA


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
    import FlowLayout
    import InstallEvent

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

    quickMenuStyle = ("padding: 5px")

    scrollStyle = ("""
        QScrollArea {
            border: none;
            background: transparent;
        }

        QScrollArea > QWidget > QWidget {
            border: none;
            background: transparent;
        }

        QScrollArea QToolButton {
            margin: 0;
            padding: 2px;
            padding-left: 4px;
            padding-right: 4px;
            border: 1px solid transparent;
            border-radius: 2px;
        }

        QScrollArea QToolButton#menuButton {
            padding-left: 1px;
            padding-right: 7px;
        }

        QScrollArea QToolButton:hover {
            border: 1px solid lightblue;
        }

        QScrollArea QToolButton:pressed {
            padding-left: 5px;
            padding-top: 3px;
        }

        QScrollArea QToolButton#menuButton:pressed {
            padding-left: 2px;
            padding-top: 3px;
        }

        QScrollArea QToolButton#menuButton::menu-button,
        QScrollArea QToolButton#menuButton::menu-indicator {
            margin: 0;
            padding: 0;
            border: none;
            background: transparent;
            width: 11px;
            height: 14px;
            subcontrol-origin: padding;
            subcontrol-position: bottom right;
        }
        """)

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

    def wbToolbars():
        mw = FreeCADGui.getMainWindow()

        for i in mw.findChildren(QtGui.QAction):
            if i.objectName() == "Std_ToolBarMenu":
                menu = i.menu()

        tempButton = QtGui.QPushButton(mw)
        tempButton.clicked.connect(menu.aboutToShow)
        tempButton.click()
        tempButton.deleteLater()

        toolbarList = []
        menuActions = menu.actions()
        for i in menuActions:
            if i.isEnabled():
                toolbarList.append(i.text())
        return toolbarList

    def findDockWidget():
        mw = FreeCADGui.getMainWindow()

        for i in mw.findChildren(QtGui.QDockWidget):
            if i.objectName() == "TabBar":
                dockWidget = i
        return dockWidget

    tbDock = findDockWidget()

    def tabWidget():
        widget = QtGui.QTabWidget()
        widget.tabBar().setDrawBase(False)
        widget.setMovable(True)
        return widget

    tbTabs = tabWidget()
    tbTabs.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
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
        menu.setStyleSheet(quickMenuStyle)

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
                layout = FlowLayout.FlowLayout()
                layout.setObjectName(i)
                widget.setLayout(layout)
                widget.setSizePolicy(QtGui.QSizePolicy.Ignored,
                                     QtGui.QSizePolicy.Ignored)
                scroll = QtGui.QScrollArea()
                scroll.setStyleSheet(scrollStyle)
                scroll.setObjectName(i)
                scroll.setWindowTitle(wbList[i].MenuText)
                scroll.setWidgetResizable(True)
                scroll.setVerticalScrollBarPolicy((QtCore.Qt
                                                  .ScrollBarAlwaysOff))
                scroll.setHorizontalScrollBarPolicy((QtCore.Qt
                                                    .ScrollBarAlwaysOff))
                scroll.setWidget(widget)

                try:
                    icon = wbIcon(wbList[i].Icon)
                except:
                    icon = QtGui.QIcon(QtGui.QPixmap(noneIcon))

                if paramGet.GetString("TabStyle"):
                    if paramGet.GetString("TabStyle") == "Default":
                        tbTabs.addTab(scroll, icon, wbList[i].MenuText)
                    elif paramGet.GetString("TabStyle") == "Icon":
                        tbTabs.addTab(scroll, icon, "")
                    elif paramGet.GetString("TabStyle") == "Text":
                        tbTabs.addTab(scroll, wbList[i].MenuText)
                else:
                    tbTabs.addTab(scroll, icon, wbList[i].MenuText)

                tbTabs.setTabToolTip(tbTabs.indexOf(scroll), wbList[i].ToolTip)

    addTabs()

    def onTabChange():
        mw = FreeCADGui.getMainWindow()
        activeWB = Gui.activeWorkbench().name()
        activeTab = tbTabs.currentWidget().objectName()

        if activeWB == activeTab:
            pass
        else:
            FreeCADGui.doCommand((str('Gui.activateWorkbench("'
                                 + activeTab + '")')))

        paramGen = App.ParamGet("User parameter:BaseApp/Preferences/General")

        iconSize = paramGen.GetInt("ToolbarIconSize")

        if not iconSize:
            iconSize = 24

        layout = []
        for i in mw.findChildren(QtGui.QLayout):
            if i.objectName() == activeTab:
                layout = i

        item = layout.takeAt(0)
        while item:
            item.widget().hide()
            del item
            item = layout.takeAt(0)

        toolbarAll = {}
        for i in mw.findChildren(QtGui.QToolBar):
            toolbarAll[i.windowTitle()] = i

        toolbarList = wbToolbars()

        toolbarButtons = []
        for a in toolbarList:
            if a in toolbarAll:
                for b in toolbarAll[a].findChildren(QtGui.QToolButton):
                    try:
                        if not b.defaultAction().isSeparator():
                            toolbarButtons.append(b)
                    except:
                        pass

        def buttonAdd(i):
            if i.menu() is None:
                toolButton = QtGui.QToolButton()
                toolButton.setAutoRaise(i.autoRaise())
                toolButton.setDefaultAction(i.defaultAction())
                toolButton.setIconSize(QSize(iconSize, iconSize))
                toolButton.installEventFilter((InstallEvent
                                              .InstallEvent(toolButton)))
                layout.addWidget(toolButton)

                if i.defaultAction().menu() is None:
                    pass
                else:
                    toolButton.setObjectName("menuButton")

            else:
                toolButton = QtGui.QToolButton()
                toolButton.setObjectName("menuButton")
                toolButton.setAutoRaise(i.autoRaise())
                toolButton.setDefaultAction(i.defaultAction())
                toolButton.setIconSize(QSize(iconSize, iconSize))
                toolButton.installEventFilter((InstallEvent
                                              .InstallEvent(toolButton)))
                toolButton.setMenu(i.menu())
                toolButton.setPopupMode(i.popupMode())
                layout.addWidget(toolButton)

        for i in toolbarButtons:
            buttonAdd(i)

        quickMenuButton = quickMenu()
        quickMenuButton.setIconSize(QSize(iconSize, iconSize))

        layout.addWidget(quickMenuButton)

    tbTabs.currentChanged.connect(onTabChange)

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

        for i in mw.findChildren(QtGui.QScrollArea):
            if i.objectName() == activeWB:
                tbTabs.setCurrentIndex(tbTabs.indexOf(i))

        onTabChange()

    afterStart()

timer = QtCore.QTimer()
timer.setSingleShot(True)
timer.timeout.connect(guiUp)
timer.start(1000)
FreeCAD.timer = timer
