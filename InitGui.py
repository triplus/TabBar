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


p = FreeCAD.ParamGet("User parameter:BaseApp/TabBar")


if p.GetBool("Enabled", 1):
    # Delete duplicate toolbars (can be added by customize dialog).
    pathTB = "User parameter:BaseApp/Workbench/Global/Toolbar"
    pTB = FreeCAD.ParamGet(pathTB)
    n = 1
    while n < 30:
        group = "Custom_" + str(n)
        if pTB.HasGroup(group):
            if pTB.GetGroup(group).GetString("Name") == "Tabs":
                pTB.RemGroup(group)
        n += 1

    # Create toolbar.
    pathTB = "User parameter:BaseApp/Workbench/Global/Toolbar/Tabs"
    pTB = FreeCAD.ParamGet(pathTB)
    pTB.SetString("Name", "Tabs")
    pTB.SetBool("Active", 1)

    import TabBar_Gui
