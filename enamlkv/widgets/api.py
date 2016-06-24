from enamlkv.kv.kv_factories import get_control

# Layouts
BoxLayout = get_control('kivy.uix.boxlayout.BoxLayout')
FloatLayout = get_control('kivy.uix.floatlayout.FloatLayout')
RelativeLayout = get_control('kivy.uix.relativelayout.RelativeLayout')
GridLayout = get_control('kivy.uix.gridlayout.GridLayout')
AnchorLayout = get_control('kivy.uix.anchorlayout.AnchorLayout')
PageLayout = get_control('kivy.uix.pagelayout.PageLayout')
ScatterLayout = get_control('kivy.uix.scatterlayout.ScatterLayout')
StackLayout = get_control('kivy.uix.stacklayout.StackLayout')

# Ux Widgets
Label = get_control('kivy.uix.label.Label')
Button = get_control('kivy.uix.button.Button')
CheckBox = get_control('kivy.uix.checkbox.CheckBox')
Image = get_control('kivy.uix.image.Image')
AsyncImage = get_control('kivy.uix.image.AsyncImage')
Slider = get_control('kivy.uix.slider.Slider')
ProgressBar = get_control('kivy.uix.progressbar.ProgressBar')
TextInput = get_control('kivy.uix.textinput.TextInput')
ToggleButton = get_control('kivy.uix.togglebutton.ToggleButton')
Switch = get_control('kivy.uix.switch.Switch')
Video = get_control('kivy.uix.video.Video')
Camera = get_control('kivy.uix.camera.Camera')

Accordion = get_control("kivy.uix.accordion.Accordion")
AccordionItem = get_control("kivy.uix.accordion.AccordionItem")

ActionBar = get_control("kivy.uix.actionbar.ActionBar")
ActionButton = get_control("kivy.uix.actionbar.ActionButton")
ActionToggleButton = get_control("kivy.uix.actionbar.ActionToggleButton")
ActionCheck = get_control("kivy.uix.actionbar.ActionCheck")
ActionSeparator = get_control("kivy.uix.actionbar.ActionSeparator")
ActionDropDown = get_control("kivy.uix.actionbar.ActionDropDown")
ActionGroup = get_control("kivy.uix.actionbar.ActionGroup")
ActionOverflow = get_control("kivy.uix.actionbar.ActionOverflow")
ActionView = get_control("kivy.uix.actionbar.ActionView")
ActionPrevious = get_control("kivy.uix.actionbar.ActionPrevious")

ScreenManager = get_control("kivy.uix.screenmanager.ScreenManager")
Screen = get_control("kivy.uix.screenmanager.Screen")

CodeInput = get_control("kivy.uix.codeinput.CodeInput")

DropDown = get_control("kivy.uix.dropdown.DropDown")
Spinner = get_control("kivy.uix.spinner.Spinner")
Splitter = get_control("kivy.uix.splitter.Splitter")
ColorPicker = get_control("kivy.uix.colorpicker.ColorPicker",read_only_properties=['wheel'])

TabbedPanel = get_control("kivy.uix.tabbedpanel.TabbedPanel",read_only_properties=['content','tab_list','default_tab',"_current_tab","_default_tab"])
TabbedPanelContent = get_control("kivy.uix.tabbedpanel.TabbedPanelContent")
TabbedPanelHeader = get_control("kivy.uix.tabbedpanel.TabbedPanelHeader")
TabbedPanelItem = get_control("kivy.uix.tabbedpanel.TabbedPanelItem")
TabbedPanelStrip = get_control("kivy.uix.tabbedpanel.TabbedPanelStrip")

ScrollView = get_control("kivy.uix.scrollview.ScrollView") 

