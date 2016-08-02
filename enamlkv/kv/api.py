#------------------------------------------------------------------------------
# Copyright (c) 2016, frmdstryr.
#
# Distributed under the terms of the MIT License.
#
# The full license is in the file LICENSE, distributed with this software.
#------------------------------------------------------------------------------
import sys
from types import ModuleType
from enamlkv.kv.kv_factories import get_control

KV_CONTROLS = dict(
    # Layouts
    BoxLayout=lambda: get_control('kivy.uix.boxlayout.BoxLayout'),
    FloatLayout = lambda: get_control('kivy.uix.floatlayout.FloatLayout'),
    RelativeLayout = lambda: get_control('kivy.uix.relativelayout.RelativeLayout'),
    GridLayout = lambda: get_control('kivy.uix.gridlayout.GridLayout'),
    AnchorLayout = lambda: get_control('kivy.uix.anchorlayout.AnchorLayout'),
    PageLayout = lambda: get_control('kivy.uix.pagelayout.PageLayout'),
    ScatterLayout = lambda: get_control('kivy.uix.scatterlayout.ScatterLayout'),
    ScatterPlaneLayout = lambda: get_control('kivy.uix.scatterlayout.ScatterPlaneLayout'),
    Spacer = lambda: get_control('kivy.uix.widget.Widget'),
    
    StackLayout = lambda: get_control('kivy.uix.stacklayout.StackLayout'),
    # Ux Widgets
    Label = lambda: get_control('kivy.uix.label.Label'),
    Button = lambda: get_control('kivy.uix.button.Button'),
    CheckBox = lambda: get_control('kivy.uix.checkbox.CheckBox'),
    Image = lambda: get_control('kivy.uix.image.Image'),
    AsyncImage = lambda: get_control('kivy.uix.image.AsyncImage'),
    Slider = lambda: get_control('kivy.uix.slider.Slider'),
    ProgressBar = lambda: get_control('kivy.uix.progressbar.ProgressBar'),
    TextInput = lambda: get_control('kivy.uix.textinput.TextInput',read_only_properties=['keyboard','cursor_pos','cursor_col','cursor_row','minimum_height']),
    ToggleButton = lambda: get_control('kivy.uix.togglebutton.ToggleButton'),
    Switch = lambda: get_control('kivy.uix.switch.Switch'),
    Video = lambda: get_control('kivy.uix.video.Video'),
    Camera = lambda: get_control('kivy.uix.camera.Camera',read_only_properties=['norm_image_size']),
    
    Accordion = lambda: get_control("kivy.uix.accordion.Accordion"),
    AccordionItem = lambda: get_control("kivy.uix.accordion.AccordionItem"),
    
    ActionBar = lambda: get_control("kivy.uix.actionbar.ActionBar"),
    ActionButton = lambda: get_control("kivy.uix.actionbar.ActionButton"),
    ActionToggleButton = lambda: get_control("kivy.uix.actionbar.ActionToggleButton"),
    ActionCheck = lambda: get_control("kivy.uix.actionbar.ActionCheck"),
    ActionSeparator = lambda: get_control("kivy.uix.actionbar.ActionSeparator"),
    ActionDropDown = lambda: get_control("kivy.uix.actionbar.ActionDropDown"),
    ActionGroup = lambda: get_control("kivy.uix.actionbar.ActionGroup"),
    ActionOverflow = lambda: get_control("kivy.uix.actionbar.ActionOverflow"),
    ActionView = lambda: get_control("kivy.uix.actionbar.ActionView"),
    ActionPrevious = lambda: get_control("kivy.uix.actionbar.ActionPrevious"),
    
    ScreenManager = lambda: get_control("kivy.uix.screenmanager.ScreenManager",read_only_properties=['screen_names']),
    Screen = lambda: get_control("kivy.uix.screenmanager.Screen"),
    
    CodeInput = lambda: get_control("kivy.uix.codeinput.CodeInput"),
    
    DropDown = lambda: get_control("kivy.uix.dropdown.DropDown"),
    Spinner = lambda: get_control("kivy.uix.spinner.Spinner"),
    #SpinnerButton = lambda: get_control("kivy.uix.spinner.SpinnerButton"),
    Splitter = lambda: get_control("kivy.uix.splitter.Splitter"),
    ColorPicker = lambda: get_control("kivy.uix.colorpicker.ColorPicker",read_only_properties=['wheel']),
    
    Popup = lambda: get_control("kivy.uix.popup.Popup"),
    
    TabbedPanel = lambda: get_control("kivy.uix.tabbedpanel.TabbedPanel",read_only_properties=['content','tab_list','default_tab',"_current_tab","_default_tab"]),
    TabbedPanelContent = lambda: get_control("kivy.uix.tabbedpanel.TabbedPanelContent"),
    TabbedPanelHeader = lambda: get_control("kivy.uix.tabbedpanel.TabbedPanelHeader"),
    TabbedPanelItem = lambda: get_control("kivy.uix.tabbedpanel.TabbedPanelItem"),
    TabbedPanelStrip = lambda: get_control("kivy.uix.tabbedpanel.TabbedPanelStrip"),
    
    ScrollView = lambda: get_control("kivy.uix.scrollview.ScrollView",read_only_properties=['hbar','vbar','bbox']),
    
    RstDocument = lambda: get_control("kivy.uix.rst.RstDocument"),
    RstVideoPlayer = lambda: get_control("kivy.uix.rst.RstVideoPlayer"),
    RstTitle = lambda: get_control("kivy.uix.rst.RstTitle"),
    RstParagraph = lambda: get_control("kivy.uix.rst.RstParagraph"),
    RstTerm = lambda: get_control("kivy.uix.rst.RstTerm"),
    RstBlockQuote = lambda: get_control("kivy.uix.rst.RstBlockQuote"),
    RstLiteralBlock = lambda: get_control("kivy.uix.rst.RstLiteralBlock"),
    RstList = lambda: get_control("kivy.uix.rst.RstList"),
    RstListItem = lambda: get_control("kivy.uix.rst.RstListItem"),
    RstListBullet = lambda: get_control("kivy.uix.rst.RstListBullet"),
    RstSystemMessage = lambda: get_control("kivy.uix.rst.RstSystemMessage"),
    RstWarning = lambda: get_control("kivy.uix.rst.RstWarning"),
    RstNote = lambda: get_control("kivy.uix.rst.RstNote"),
    RstImage = lambda: get_control("kivy.uix.rst.RstImage"),
    RstAsyncImage = lambda: get_control("kivy.uix.rst.RstAsyncImage"),
    RstDefinitionList = lambda: get_control("kivy.uix.rst.RstDefinitionList"),
    RstDefinition = lambda: get_control("kivy.uix.rst.RstDefinition"),
    RstFieldList = lambda: get_control("kivy.uix.rst.RstFieldList"),
    RstFieldName = lambda: get_control("kivy.uix.rst.RstFieldName"),
    RstFieldBody = lambda: get_control("kivy.uix.rst.RstFieldBody"),
    RstGridLayout = lambda: get_control("kivy.uix.rst.RstGridLayout"),
    RstTable = lambda: get_control("kivy.uix.rst.RstTable"),
    RstEntry = lambda: get_control("kivy.uix.rst.RstEntry"),
    RstTransition = lambda: get_control("kivy.uix.rst.RstTransition"),
    RstEmptySpace = lambda: get_control("kivy.uix.rst.RstEmptySpace"),
    RstDefinitionSpace = lambda: get_control("kivy.uix.rst.RstDefinitionSpace"),
    
    Sandbox = lambda: get_control("kivy.uix.sandbox.Sandbox"),
    Scatter = lambda: get_control("kivy.uix.scatter.Scatter",read_only_properties=['bbox']),
    ScatterPlane = lambda: get_control("kivy.uix.scatter.ScatterPlane"),
    
    Settings = lambda: get_control("kivy.uix.settings.Settings"),
    SettingsWithSidebar = lambda: get_control("kivy.uix.settings.SettingsWithSidebar"),
    SettingsWithSpinner = lambda: get_control("kivy.uix.settings.SettingsWithSpinner"),
    SettingsWithTabbedPanel = lambda: get_control("kivy.uix.settings.SettingsWithTabbedPanel"),
    SettingsWithNoMenu = lambda: get_control("kivy.uix.settings.SettingsWithNoMenu"),
    SettingSpacer = lambda: get_control("kivy.uix.settings.SettingSpacer"),
    SettingItem = lambda: get_control("kivy.uix.settings.SettingItem"),
    SettingBoolean = lambda: get_control("kivy.uix.settings.SettingBoolean"),
    SettingString = lambda: get_control("kivy.uix.settings.SettingString"),
    SettingPath = lambda: get_control("kivy.uix.settings.SettingPath"),
    SettingNumeric = lambda: get_control("kivy.uix.settings.SettingNumeric"),
    SettingOptions = lambda: get_control("kivy.uix.settings.SettingOptions"),
    SettingTitle = lambda: get_control("kivy.uix.settings.SettingTitle"),
    SettingsPanel = lambda: get_control("kivy.uix.settings.SettingsPanel"),
    InterfaceWithSidebar = lambda: get_control("kivy.uix.settings.InterfaceWithSidebar"),
    InterfaceWithSpinner = lambda: get_control("kivy.uix.settings.InterfaceWithSpinner"),
    InterfaceWithNoMenu = lambda: get_control("kivy.uix.settings.InterfaceWithNoMenu"),
    InterfaceWithTabbedPanel = lambda: get_control("kivy.uix.settings.InterfaceWithTabbedPanel"),
    ContentPanel = lambda: get_control("kivy.uix.settings.ContentPanel"),
    MenuSidebar = lambda: get_control("kivy.uix.settings.MenuSidebar"),
    SettingSidebarLabel = lambda: get_control("kivy.uix.settings.SettingSidebarLabel"),
    
    
    VKeyboard = lambda: get_control("kivy.uix.vkeyboard.VKeyboard"),
)

class DynamicImporter(ModuleType):
    """ Only create widgets that are actually used so that
    unused widgets do not need to be imported.
    """
    
    def __getattr__(self,name):
        #print("Loading {}".format(name))
        return KV_CONTROLS[name]()

old_module = sys.modules[__name__] # So it's not garbage collected
new_module = sys.modules[__name__] = DynamicImporter(__name__)
new_module.__dict__.update({
    '__file__':         __file__,
    '__doc__':          __doc__,
    '__all__':           KV_CONTROLS.keys(),
})


