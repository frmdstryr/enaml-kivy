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
    
    ScreenManager = lambda: get_control("kivy.uix.screenmanager.ScreenManager"),
    Screen = lambda: get_control("kivy.uix.screenmanager.Screen"),
    
    CodeInput = lambda: get_control("kivy.uix.codeinput.CodeInput"),
    
    DropDown = lambda: get_control("kivy.uix.dropdown.DropDown"),
    Spinner = lambda: get_control("kivy.uix.spinner.Spinner"),
    Splitter = lambda: get_control("kivy.uix.splitter.Splitter"),
    ColorPicker = lambda: get_control("kivy.uix.colorpicker.ColorPicker",read_only_properties=['wheel']),
    
    TabbedPanel = lambda: get_control("kivy.uix.tabbedpanel.TabbedPanel",read_only_properties=['content','tab_list','default_tab',"_current_tab","_default_tab"]),
    TabbedPanelContent = lambda: get_control("kivy.uix.tabbedpanel.TabbedPanelContent"),
    TabbedPanelHeader = lambda: get_control("kivy.uix.tabbedpanel.TabbedPanelHeader"),
    TabbedPanelItem = lambda: get_control("kivy.uix.tabbedpanel.TabbedPanelItem"),
    TabbedPanelStrip = lambda: get_control("kivy.uix.tabbedpanel.TabbedPanelStrip"),
    ScrollView = lambda: get_control("kivy.uix.scrollview.ScrollView",read_only_properties=['vbar','bbox']),
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