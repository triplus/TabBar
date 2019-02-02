# TabBar widget for FreeCAD
# Copyright (C) 2015, 2016, 2017, 2018 triplus @ FreeCAD
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

"""TabBar widget for FreeCAD."""


import os
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtGui
from PySide import QtCore


actions = {}
mw = Gui.getMainWindow()
group = QtGui.QActionGroup(mw)
p = App.ParamGet("User parameter:BaseApp/TabBar")
path = os.path.dirname(__file__) + "/Resources/icons/"


def wbIcon(i):
    """Create workbench icon."""
    if str(i.find("XPM")) != "-1":
        icon = []
        for a in ((((i
                     .split('{', 1)[1])
                    .rsplit('}', 1)[0])
                   .strip())
                  .split("\n")):
            icon.append((a
                         .split('"', 1)[1])
                        .rsplit('"', 1)[0])
        icon = QtGui.QIcon(QtGui.QPixmap(icon))
    else:
        icon = QtGui.QIcon(QtGui.QPixmap(i))
    if icon.isNull():
        icon = QtGui.QIcon(":/icons/freecad")
    return icon


def wbActions():
    """Create workbench actions."""
    wbList = Gui.listWorkbenches()
    for i in wbList:
        if i not in actions:
            action = QtGui.QAction(group)
            action.setCheckable(True)
            action.setText(wbList[i].MenuText)
            action.setData(i)
            try:
                action.setIcon(wbIcon(wbList[i].Icon))
            except:
                action.setIcon(QtGui.QIcon(":/icons/freecad"))
            actions[i] = action


def defaults():
    """Sorted string of available workbenches."""
    d = Gui.listWorkbenches()
    d = list(d)
    d.sort()
    d = ",".join(d)
    return d


def onOrientationChanged(w):
    """Set the tabs orientation."""
    tab = w[0]
    btn = w[1]
    orientation = p.GetString("Orientation", "Auto")

    def layout():
        """Support menu for West and East orientations."""
        wid = QtGui.QWidget()
        lo = QtGui.QVBoxLayout()
        lo.addWidget(tab)
        lo.addWidget(btn)
        wid.setLayout(lo)
        tb.addWidget(wid)
        lo.setContentsMargins(0, 0, 0, 0)
        btn.setMaximumWidth(tab.height())

    if orientation == "Auto":
        if mw.toolBarArea(tb) == QtCore.Qt.ToolBarArea.TopToolBarArea:
            tb.addWidget(tab)
            tab.setTabPosition(QtGui.QTabWidget.North)
            tab.setCornerWidget(btn)
        elif mw.toolBarArea(tb) == QtCore.Qt.ToolBarArea.BottomToolBarArea:
            tb.addWidget(tab)
            tab.setTabPosition(QtGui.QTabWidget.South)
            tab.setCornerWidget(btn)
        elif mw.toolBarArea(tb) == QtCore.Qt.ToolBarArea.LeftToolBarArea:
            tab.setTabPosition(QtGui.QTabWidget.West)
            layout()
        elif mw.toolBarArea(tb) == QtCore.Qt.ToolBarArea.RightToolBarArea:
            tab.setTabPosition(QtGui.QTabWidget.East)
            layout()
        elif tb.orientation() == QtCore.Qt.Orientation.Horizontal:
            tb.addWidget(tab)
            tab.setTabPosition(QtGui.QTabWidget.North)
            tab.setCornerWidget(btn)
        elif tb.orientation() == QtCore.Qt.Orientation.Vertical:
            tab.setTabPosition(QtGui.QTabWidget.West)
            layout()
        else:
            pass
    else:
        if orientation == "North":
            tb.addWidget(tab)
            tab.setTabPosition(QtGui.QTabWidget.North)
            tab.setCornerWidget(btn)
        elif orientation == "South":
            tb.addWidget(tab)
            tab.setTabPosition(QtGui.QTabWidget.South)
            tab.setCornerWidget(btn)
        elif orientation == "West":
            tab.setTabPosition(QtGui.QTabWidget.West)
            layout()
        elif orientation == "East":
            tab.setTabPosition(QtGui.QTabWidget.East)
            layout()
        else:
            pass

    prefbutton = p.GetString("PrefButton", "On")
    if prefbutton == "On":
        btn.show()
    else:
        btn.hide()


def tabs():
    """Tabs widget."""
    tb.clear()
    wbActions()
    default = defaults()
    w = QtGui.QTabWidget(tb)
    active = Gui.activeWorkbench().__class__.__name__

    enabled = p.GetString("Enabled", default)
    enabled = enabled.split(",")
    partially = p.GetString("Partially")
    partially = partially.split(",")
    unchecked = p.GetString("Unchecked")
    unchecked = unchecked.split(",")
    position = p.GetString("Position")
    position = position.split(",")

    # Menu
    btn = QtGui.QPushButton(w)
    btn.setFlat(True)
    btn.setIcon(QtGui.QIcon(path + "TabBar_AddWorkbench.svg"))
    menu = QtGui.QMenu(btn)
    btn.setMenu(menu)

    if active in partially:
        partially.remove(active)

    for i in partially:
        if i in actions:
            menu.addAction(actions[i])

    menu.addSeparator()
    pref = QtGui.QAction(menu)
    pref.setText("Preferences")
    pref.triggered.connect(onPreferences)
    menu.addAction(pref)

    # Tabs
    w.setDocumentMode(True)
    w.setUsesScrollButtons(True)
    w.tabBar().setDrawBase(True)
    w.setObjectName("TabBar")

    default = default.split(",")
    for i in default:
        if (i not in partially and
                i not in enabled and
                i not in unchecked):
            enabled.append(i)

    if active not in enabled:
        enabled.append(active)

    for i in enabled:
        if i in actions:
            if p.GetString("Style") == "IconText":
                r = w.tabBar().addTab(actions[i].icon(), actions[i].text())
            elif p.GetString("Style") == "Text":
                r = w.tabBar().addTab(actions[i].text())
            else:
                r = w.tabBar().addTab(actions[i].icon(), None)
            w.tabBar().setTabData(r, i)
            w.tabBar().setTabToolTip(r, actions[i].text())

    for i in range(w.count()):
        if w.tabBar().tabData(i) == active:
            w.tabBar().setCurrentIndex(i)

    def onTab(d):
        """Activate workbench on tab."""
        data = w.tabBar().tabData(d)
        if data:
            for i in actions:
                if actions[i].data() == data:
                    actions[i].trigger()
        w.currentChanged.disconnect(onTab)

    w.currentChanged.connect(onTab)

    return [w, btn]


def onWorkbenchActivated():
    """Populate the tabs toolbar."""
    for i in tb.findChildren(QtGui.QTabWidget, "TabBar"):
        i.deleteLater()
    for i in tb.findChildren(QtGui.QWidgetAction):
        i.deleteLater()

    w = tabs()
    onOrientationChanged(w)


def onGroup(a):
    """Activate workbench on action."""
    data = a.data()
    if data:
        try:
            Gui.doCommand('Gui.activateWorkbench("' + data + '")')
        except KeyError:
            pass


def prefDialog():
    """Preferences dialog."""
    wbActions()
    dialog = QtGui.QDialog(mw)
    dialog.setModal(True)
    dialog.resize(800, 450)
    dialog.setWindowTitle("TabBar preferences")
    layout = QtGui.QVBoxLayout()
    dialog.setLayout(layout)
    selector = QtGui.QListWidget(dialog)
    selector.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    btnClose = QtGui.QPushButton("Close", dialog)
    btnClose.setToolTip("Close the preferences dialog")
    btnClose.setDefault(True)
    btnUp = QtGui.QPushButton(dialog)
    btnUp.setToolTip("Move selected item up")
    btnUp.setIcon(QtGui.QIcon(path + "TabBar_MoveUp"))
    btnDown = QtGui.QPushButton(dialog)
    btnDown.setToolTip("Move selected item down")
    btnDown.setIcon(QtGui.QIcon(path + "TabBar_MoveDown"))
    l0 = QtGui.QVBoxLayout()
    g0 = QtGui.QGroupBox("Style:")
    g0.setLayout(l0)
    r0 = QtGui.QRadioButton("Icon", g0)
    r0.setObjectName("Icon")
    r0.setToolTip("TabBar icon style")
    r1 = QtGui.QRadioButton("Text", g0)
    r1.setObjectName("Text")
    r1.setToolTip("TabBar text style")
    r2 = QtGui.QRadioButton("Icon and text", g0)
    r2.setObjectName("IconText")
    r2.setToolTip("TabBar icon and text style")
    l0.addWidget(r0)
    l0.addWidget(r1)
    l0.addWidget(r2)
    l1 = QtGui.QVBoxLayout()
    g1 = QtGui.QGroupBox("Tab orientation:")
    g1.setLayout(l1)
    r3 = QtGui.QRadioButton("Auto", g1)
    r3.setObjectName("Auto")
    r3.setToolTip("Set based on the orientation")
    r4 = QtGui.QRadioButton("Top", g1)
    r4.setObjectName("North")
    r4.setToolTip("Tabs at top")
    r5 = QtGui.QRadioButton("Bottom", g1)
    r5.setObjectName("South")
    r5.setToolTip("Tabs at bottom")
    r6 = QtGui.QRadioButton("Left", g1)
    r6.setObjectName("West")
    r6.setToolTip("Tabs at left")
    r7 = QtGui.QRadioButton("Right", g1)
    r7.setObjectName("East")
    r7.setToolTip("Tabs at right")
    l1.addWidget(r3)
    l1.addWidget(r4)
    l1.addWidget(r5)
    l1.addWidget(r6)
    l1.addWidget(r7)
    l2 = QtGui.QHBoxLayout()
    l2.addWidget(btnUp)
    l2.addWidget(btnDown)
    l2.addStretch(1)
    l2.addWidget(btnClose)
    l3 = QtGui.QHBoxLayout()
    l3.addStretch()
    l4 = QtGui.QVBoxLayout()
    l4.addWidget(g0)
    l4.addWidget(g1)
    l6 = QtGui.QVBoxLayout()
    g6 = QtGui.QGroupBox("Preferences button on tabbar:")
    g6.setLayout(l6)
    r8 = QtGui.QRadioButton("On", g6)
    r8.setObjectName("On")
    r8.setToolTip("A preference button appears on the right/bottom of the tabbar")
    r9 = QtGui.QRadioButton("Off", g6)
    r9.setObjectName("Off")
    r8.setToolTip("No button on the tabbar (only via menu Tools -> Acessories")
    l6.addWidget(r8)
    l6.addWidget(r9)
    l4.addWidget(g6)
    l4.addStretch()
    l4.insertLayout(0, l3)
    l5 = QtGui.QHBoxLayout()
    l5.addWidget(selector)
    l5.insertLayout(1, l4)
    layout.insertLayout(0, l5)
    layout.insertLayout(1, l2)

    def onAccepted():
        """Close dialog on button close."""
        dialog.done(1)

    def onFinished():
        """Delete dialog on close."""
        dialog.deleteLater()

    def onItemChanged(item=None):
        """Save workbench list state."""
        if item:
            selector.blockSignals(True)
            if item.data(50) == "Unchecked":
                item.setCheckState(QtCore.Qt.CheckState(1))
                item.setData(50, "Partially")
            elif item.data(50) == "Partially":
                item.setCheckState(QtCore.Qt.CheckState(2))
                item.setData(50, "Checked")
            else:
                item.setCheckState(QtCore.Qt.CheckState(0))
                item.setData(50, "Unchecked")
            selector.blockSignals(False)
        enabled = []
        partially = []
        unchecked = []
        for index in range(selector.count()):
            if selector.item(index).checkState() == QtCore.Qt.Checked:
                enabled.append(selector.item(index).data(32))
            elif (selector.item(index).checkState() ==
                  QtCore.Qt.PartiallyChecked):
                partially.append(selector.item(index).data(32))
            else:
                unchecked.append(selector.item(index).data(32))
        p.SetString("Enabled", ",".join(enabled))
        p.SetString("Partially", ",".join(partially))
        p.SetString("Unchecked", ",".join(unchecked))
        onWorkbenchActivated()

    def onUp():
        """Save workbench position list."""
        currentIndex = selector.currentRow()
        if currentIndex != 0:
            selector.blockSignals(True)
            currentItem = selector.takeItem(currentIndex)
            selector.insertItem(currentIndex - 1, currentItem)
            selector.setCurrentRow(currentIndex - 1)
            selector.blockSignals(False)
            position = []
            for index in range(selector.count()):
                position.append(selector.item(index).data(32))
            p.SetString("Position", ",".join(position))
            onItemChanged()

    def onDown():
        """Save workbench position list."""
        currentIndex = selector.currentRow()
        if currentIndex != selector.count() - 1 and currentIndex != -1:
            selector.blockSignals(True)
            currentItem = selector.takeItem(currentIndex)
            selector.insertItem(currentIndex + 1, currentItem)
            selector.setCurrentRow(currentIndex + 1)
            selector.blockSignals(False)
            position = []
            for index in range(selector.count()):
                position.append(selector.item(index).data(32))
            p.SetString("Position", ",".join(position))
            onItemChanged()

    def onG0(r):
        """Set TabBar style."""
        if r:
            for i in g0.findChildren(QtGui.QRadioButton):
                if i.isChecked():
                    p.SetString("Style", i.objectName())
            onWorkbenchActivated()

    def onG1(r):
        """Set TabBar orientation."""
        if r:
            for i in g1.findChildren(QtGui.QRadioButton):
                if i.isChecked():
                    p.SetString("Orientation", i.objectName())
            onWorkbenchActivated()

    def onG6(r):
        """Set pref button."""
        if r:
            for i in g6.findChildren(QtGui.QRadioButton):
                if i.isChecked():
                    p.SetString("PrefButton", i.objectName())
            onWorkbenchActivated()

    default = defaults()
    enabled = p.GetString("Enabled", default)
    enabled = enabled.split(",")
    partially = p.GetString("Partially")
    partially = partially.split(",")
    unchecked = p.GetString("Unchecked")
    unchecked = unchecked.split(",")
    position = p.GetString("Position")
    position = position.split(",")
    default = default.split(",")
    for i in default:
        if i not in position:
            position.append(i)
    for i in position:
        if i in actions:
            item = QtGui.QListWidgetItem(selector)
            item.setText(actions[i].text())
            item.setIcon(actions[i].icon())
            item.setData(32, actions[i].data())
            if actions[i].data() in enabled:
                item.setCheckState(QtCore.Qt.CheckState(2))
                item.setData(50, "Checked")
            elif actions[i].data() in partially:
                item.setCheckState(QtCore.Qt.CheckState(1))
                item.setData(50, "Partially")
            elif actions[i].data() in unchecked:
                item.setCheckState(QtCore.Qt.CheckState(0))
                item.setData(50, "Unchecked")
            else:
                item.setCheckState(QtCore.Qt.CheckState(2))
                item.setData(50, "Checked")

    style = p.GetString("Style")
    if style == "Text":
        r1.setChecked(True)
    elif style == "IconText":
        r2.setChecked(True)
    else:
        r0.setChecked(True)
    orientation = p.GetString("Orientation")
    if orientation == "North":
        r4.setChecked(True)
    elif orientation == "South":
        r5.setChecked(True)
    elif orientation == "West":
        r6.setChecked(True)
    elif orientation == "East":
        r7.setChecked(True)
    else:
        r3.setChecked(True)
    prefbutton = p.GetString("PrefButton", "On")
    if prefbutton == "On":
        r8.setChecked(True)
    else:
        r9.setChecked(True)
    r0.toggled.connect(onG0)
    r1.toggled.connect(onG0)
    r2.toggled.connect(onG0)
    r3.toggled.connect(onG1)
    r4.toggled.connect(onG1)
    r5.toggled.connect(onG1)
    r6.toggled.connect(onG1)
    r7.toggled.connect(onG1)
    r8.toggled.connect(onG6)
    r9.toggled.connect(onG6)
    btnUp.clicked.connect(onUp)
    btnDown.clicked.connect(onDown)
    selector.itemChanged.connect(onItemChanged)
    dialog.finished.connect(onFinished)
    btnClose.clicked.connect(onAccepted)

    return dialog


def onPreferences():
    """Open the preferences dialog."""
    dialog = prefDialog()
    dialog.show()


def accessoriesMenu():
    """Add TabBar preferences to accessories menu."""
    pref = QtGui.QAction(mw)
    pref.setText("TabBar")
    pref.setObjectName("TabBar")
    pref.triggered.connect(onPreferences)
    try:
        import AccessoriesMenu
        AccessoriesMenu.addItem("TabBar")
    except ImportError:
        a = mw.findChild(QtGui.QAction, "AccessoriesMenu")
        if a:
            a.menu().addAction(pref)
        else:
            mb = mw.menuBar()
            actionAccessories = QtGui.QAction(mw)
            actionAccessories.setObjectName("AccessoriesMenu")
            actionAccessories.setIconText("Accessories")
            menu = QtGui.QMenu()
            actionAccessories.setMenu(menu)
            menu.addAction(pref)

            def addMenu():
                """Add accessories menu to the menu bar."""
                toolsMenu = mb.findChild(QtGui.QMenu, "&Tools")
                if toolsMenu:
                    toolsMenu.addAction(actionAccessories)
                    actionAccessories.setVisible(True)

            addMenu()
            mw.workbenchActivated.connect(addMenu)


def onClose():
    """Remove tabs toolbar on FreeCAD close."""
    g = App.ParamGet("User parameter:BaseApp/Workbench/Global/Toolbar")
    g.RemGroup("Tabs")


def onStart():
    """Start TabBar."""
    start = False
    try:
        mw.workbenchActivated
        mw.mainWindowClosed
        global tb
        tb = mw.findChild(QtGui.QToolBar, "Tabs")
        tb.orientation
        start = True
    except AttributeError:
        pass
    if start:
        t.stop()
        t.deleteLater()
        accessoriesMenu()
        onWorkbenchActivated()
        group.triggered.connect(onGroup)
        mw.mainWindowClosed.connect(onClose)
        mw.workbenchActivated.connect(onWorkbenchActivated)
        tb.orientationChanged.connect(onWorkbenchActivated)
        tb.topLevelChanged.connect(onWorkbenchActivated)


def onPreStart():
    """Improve start reliability and maintain FreeCAD 0.16 support."""
    if App.Version()[1] < "17":
        onStart()
    else:
        if mw.property("eventLoop"):
            onStart()


t = QtCore.QTimer()
t.timeout.connect(onPreStart)
t.start(500)
