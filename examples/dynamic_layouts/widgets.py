#------------------------------------------------------------------------------
# Copyright (c) 2016, frmdstryr.
#
# Distributed under the terms of the MIT License.
#
# The full license is in the file LICENSE, distributed with this software.
#------------------------------------------------------------------------------
from kivy.uix.widget import Widget
'''
Created on Jun 23, 2016

@author: jrm
'''
from enamlkv.kv.kv_factories import get_control


from kivy.garden import graph

class _Graph(graph.Graph):
    """ So we can define plots in Enaml nicely"""
    def add_widget(self,widget):
        if isinstance(widget,graph.Plot):
            self.add_plot(widget)
            return
        super(_Graph, self).add_widget(widget)
    
    def remove_widget(self,widget):
        if isinstance(widget,graph.Plot):
            self.remove_plot(widget)
            return
        super(_Graph, self).remove_widget(widget)
        
class _MeshLinePlot(graph.MeshLinePlot,Widget):
    pass

Toolbar = get_control("kivymd.toolbar.Toolbar")
NavigationDrawer = get_control("kivymd.navigationdrawer.NavigationDrawer")
NavigationDrawerIconButton = get_control("kivymd.navigationdrawer.NavigationDrawerIconButton")
SmartTile = get_control("kivymd.grid.SmartTile")
MDRaisedButton = get_control("kivymd.button.MDRaisedButton")#,read_only_properties=['elevation_normal'])
MDFloatingActionButton = get_control("kivymd.button.MDFloatingActionButton")
MDDropdownMenu = get_control("kivymd.menu.MDDropdownMenu")
MDCheckbox = get_control("kivymd.selectioncontrols.MDCheckbox")
MDSwitch = get_control("kivymd.selectioncontrols.MDSwitch")
MDSpinner = get_control("kivymd.spinner.MDSpinner")
MDLabel = get_control("kivymd.label.MDLabel")
MDCard = get_control("kivymd.card.MDCard")
MDList = get_control("kivymd.list.MDList")
OneLineListItem = get_control("kivymd.list.OneLineListItem")
TwoLineListItem = get_control("kivymd.list.TwoLineListItem")
ThreeLineListItem = get_control("kivymd.list.ThreeLineListItem")
OneLineIconListItem = get_control("kivymd.list.OneLineIconListItem")
OneLineAvatarIconListItem = get_control("kivymd.list.OneLineAvatarIconListItem")
SingleLineTextField = get_control("kivymd.textfields.SingleLineTextField",read_only_properties=['keyboard'])
Graph = get_control(_Graph)
MeshLinePlot = get_control(_MeshLinePlot)
