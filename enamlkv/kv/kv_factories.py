#------------------------------------------------------------------------------
# Copyright (c) 2016, frmdstryr.
# Copyright (c) 2014, Nucleic Development Team.
#
# Distributed under the terms of the MIT License.
#
# The full license is in the file LICENSE, distributed with this software.
#------------------------------------------------------------------------------
from pprint import pprint
'''
Created on Jun 18, 2016

Create enaml Controls for each Kivy widget

@author: frmdstryr
'''
import pydoc
import inspect
import logging

log = logging.getLogger("kivy")

from atom.api import Event,Instance,Typed,observe

from enaml.core.declarative import d_
from enaml.widgets.control import Control, ProxyControl

from kivy.uix.widget import Widget
from kivy.uix import behaviors
from kivy import properties

from .kv_widget import KvWidget

_CACHE = {}
_BEHAVIOR_MIXINS = [c for n,c in inspect.getmembers(behaviors,inspect.isclass)]
_BEHAVIOR_EVENTS = {behaviors.ButtonBehavior:['on_press','on_release']}

# Manually implemented factories
def window_factory():
    from .kv_window import KvWindow
    return KvWindow


KV_FACTORIES = {
    'Window': window_factory,
}

def get_proxy(dotted_widget_name):
    """ Helper to get the enaml Proxy class for a given Kivy widget. 
    
    """
    widget_class = pydoc.locate(dotted_widget_name)
    return kivy_enaml_factory(widget_class)['proxy']

def get_control(dotted_widget_name,read_only_properties=None):
    """ Helper to get the enaml Control class for a given Kivy widget.
    
    Only actually loads the widget if it is needed. 
    
    """
    log.info("Enaml: Creating control for {}".format(dotted_widget_name))
    read_only_properties = read_only_properties or []
    widget_name = dotted_widget_name.split('.')[-1]
    return kivy_enaml_factory(pydoc.locate(dotted_widget_name),read_only_properties=read_only_properties)['control']

def get_factory(dotted_widget_name):
    """ Helper to get the enaml widget factory class for a given Kivy widget. 
    
    """
    return lambda:kivy_enaml_factory(pydoc.locate(dotted_widget_name))['widget']

def kivy_enaml_factory(widget_class,read_only_properties=None):
    """ Generates the Enaml Control, Proxy, and Implementation classes for
    given Kivy widget so that it be used in an enaml file.
    
    Does this by converting the corresponding Kivy properties of the widget into
    atom properties. 
    
    """
    assert inspect.isclass(widget_class) and issubclass(widget_class, Widget), "Invalid widget class {}".format(widget_class)
    
    read_only_properties = read_only_properties or []
    
    # Try to load from cache
    if widget_class in _CACHE:
        log.info("Enaml: Loaded {} from cache".format(widget_class))
        return _CACHE[widget_class]

    # Set default base classes
    ProxyControlBase = ProxyControl
    ControlBase = Control
    KvWidgetBase = KvWidget
    
    # Find (and create if not done already) actual base classes
    _bases = None
    base_classes = inspect.getmro(widget_class)
    behavior_properties = {}
    behavior_events = []
    for cls in base_classes:
        if cls in [widget_class]:
            continue # Skip self
        elif issubclass(cls,Widget) and not _bases: # Find the first Widget superclass
            _bases = kivy_enaml_factory(cls)
            ProxyControlBase =_bases['proxy']
            ControlBase =_bases['control']
            KvWidgetBase = _bases['widget']
        # TODO: Handle behaviors
        elif cls in _BEHAVIOR_MIXINS:
            for bcls in inspect.getmro(cls):
                behavior_properties.update(bcls.__dict__.copy())
                if bcls in _BEHAVIOR_EVENTS:
                    behavior_events.extend(_BEHAVIOR_EVENTS[bcls])
    
    widget_name = widget_class.__name__
    widget_events = behavior_events
    if hasattr(widget_class,'__events__'):
        widget_events.extend(widget_class.__events__)
    widget_events = list(set(widget_events)) # Make unique
        
    log.debug("Enaml:Generating enaml classes for {}".format(widget_name))
    
    log.debug("Enaml:    Bases: {}".format((ProxyControlBase,ControlBase,KvWidgetBase)))
    
    # Properties for generic classes
    control_properties = {} 
    proxy_properties = {}
    observed_properties = []
    excluded_properties = ['parent','children','id','ids']
    default_property_values = {}
    
    # Convert all kivy properties to enaml ones
    kivy_properties = widget_class.__dict__.copy()
    
    # And behavior properties
    kivy_properties.update(behavior_properties)
    
    
    for k,v in kivy_properties.items():
        is_writable = k not in read_only_properties
        if k in excluded_properties:
            continue
        if k in widget_events:
            control_properties[k] = d_(Event(),writable=False)
            read_only_properties.append(k)
        elif isinstance(v,properties.ReferenceListProperty):
            default_value = (p.defaultvalue for p in v.defaultvalue)
            default_property_values[k] = default_value
            control_properties[k] = d_(Instance((list,tuple),factory=lambda default_value=default_value:default_value),writable=is_writable)
        #elif isinstance(v,properties.AliasProperty):# and (hasattr(v,'allownone') and v.allownone==1):
        #    # Let type checking be done by Kivy Properties
        #    control_properties[k] = d_(Instance(object,factory=lambda v=v:v.defaultvalue),writable=False)
        #    read_only_properties.append(k)
        elif isinstance(v,properties.Property):# and (hasattr(v,'allownone') and v.allownone==1):
            # Let type checking be done by Kivy Properties
            default_value = v.defaultvalue
            default_property_values[k] = default_value
            control_properties[k] = d_(Instance(object,factory=lambda default_value=default_value:default_value),writable=is_writable)
            
        # Create setter method for this property
        if (k in control_properties) and (k not in widget_events) and (k not in excluded_properties) and (not k.startswith("_")):
            observed_properties.append(k)
            
            # Write changes from Enaml to widget
            def set_property(self,value,k=k):
                #log.info("Enaml: {}.set_{}({})".format(self,k,value))
                try:
                    setattr(self.widget,k,value)
                except (KeyError,AttributeError) as e:
                    msg = "Enaml: Could not set {}.{}: {}.".format(self,k,e)
                    if "read-only" in str(e):
                        msg+=" You probably want to add this to the read_only_properties list."
                    log.error(msg)   
                    #raise
            
            # Read changes from widget to Enaml    
            def on_property(self,instance,value,k=k):
                #log.info("Enaml: {}.on_{}({},{})".format(self,k,instance,value))
                setattr(self.declaration,k,getattr(self.widget,k))
            
            if is_writable:
                proxy_properties["set_{}".format(k)] = set_property
            proxy_properties["on_{}".format(k)] = on_property
                
        
    log.debug("Enaml:    Events: {}".format(widget_events))
    log.debug("Enaml:    Properties: {}".format(observed_properties))
    
    proxy_properties['declaration'] = Instance(Control)    
    
    # Create the Proxy that defines what the implementation must implement
    ProxyWidgetControl = type("Proxy{}".format(widget_name),(ProxyControlBase,),proxy_properties)
    log.debug("Enaml:        Created proxy {} from {}".format(ProxyWidgetControl,proxy_properties))

        
    # Create the Enaml Control for this widget for use in enaml files
    # Create the Enaml ProxyControl for this widget
    @observe(*observed_properties)
    def _update_proxy(self, change):
        ControlBase._update_proxy(self,change)

    control_properties['proxy']=Typed(ProxyWidgetControl)
    control_properties['_update_proxy'] = _update_proxy  
    WidgetControl = type(widget_name,(ControlBase,),control_properties)
    log.debug("Enaml:        Created control {} from {}".format(WidgetControl,control_properties))
    
    # Create the Enaml ToolkitObject for this widget
    def create_widget(self):
        #log.verbose("{}.create_widget()".format(self))
        self.widget = widget_class()
    
    def init_widget(self):
        """ Set initial values and connect signals"""
        #log.verbose("{}.init_widget()".format(KvWidgetBase))
        KvWidgetBase.init_widget(self)
        d = self.declaration
        
        # Set initial property values
        for p in observed_properties:
            # Set initial values
            if p not in read_only_properties:
                try:
                    value = getattr(d,p)
                    #log.info("Enaml: value={},default={}".format(value,default_value))
                    # We don't have to set defaults again as this overrides properties set by rules  
                    if value!=default_property_values[p]:
                        handler = getattr(self,'set_{}'.format(p))
                        handler(value)
                except TypeError as e:
                    log.warn("Enaml: Failed to set initial value for {} on {}. Reason: {}".format(p,self,e))
            
            # Bind observers
            handler = getattr(self,"on_{}".format(p))
            binding = {p:handler}
            #log.verbose("Enaml: {}.bind({})".format(self.widget,binding))
            self.widget.bind(**binding)
        
        # Connect signals so callbacks get handled by Enaml events
        for on_event in widget_events:
            handler = getattr(self,on_event)
            binding = {on_event:handler}
            #log.verbose("Enaml: {}.bind({})".format(self.widget,binding))
            self.widget.bind(**binding)

    
    widget_properties = {
        'widget': Instance(widget_class),
        'create_widget':create_widget,
        'init_widget':init_widget
    }
    
    # Create signal handlers for the widget
    for e in widget_events:
        def on_event(self,*args,**kwargs):
            d = self.declaration
            name = kwargs.pop('__event__')
            #log.verbose("Enaml: {}.{}({})".format(self,name,args))
            event = getattr(d,name)
            #TODO: Is state already in sync?
            # Trigger enaml event
            event(args) # this doesnt do anything???
            
        widget_properties[e] = lambda self,*args:on_event(self,*args,__event__=e)
    
    #: Create the Kivy implementation of this Enaml proxy widget
    
    KvWidgetImpl = type("Kv{}".format(widget_name),(KvWidgetBase,ProxyWidgetControl),widget_properties)
    log.debug("Enaml:        Created widget impl {} from {}".format(KvWidgetImpl,widget_properties))

    # Put in cache so we don't have to recreate later
    _CACHE[widget_class] = {
        'control':WidgetControl,
        'proxy':ProxyWidgetControl,
        'widget':KvWidgetImpl
    }
    
    # Automatically add
    if widget_name not in KV_FACTORIES:
        KV_FACTORIES[widget_name] = lambda:KvWidgetImpl # Does not work
    
    # Return classes
    return _CACHE[widget_class]





