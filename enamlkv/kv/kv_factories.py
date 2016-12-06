#------------------------------------------------------------------------------
# Copyright (c) 2016, frmdstryr.
# Copyright (c) 2014, Nucleic Development Team.
#
# Distributed under the terms of the MIT License.
#
# The full license is in the file LICENSE, distributed with this software.
#------------------------------------------------------------------------------
'''
Created on Jun 18, 2016

Create enaml Controls for each Kivy widget

@author: frmdstryr
'''
import pydoc
import inspect
import logging
#import os
log = logging.getLogger("kivy")

from functools import partial

from atom.api import Event,Instance,Value,Typed,observe

from enaml.core.declarative import d_
from enaml.widgets.control import Control, ProxyControl
#from enaml.application import timed_call

from kivy.uix.widget import Widget
from kivy.uix import behaviors
from kivy import properties

from .kv_widget import KvWidget

_CACHE = {'loaded':False,'updates':0}
_BEHAVIOR_MIXINS = [c for n,c in inspect.getmembers(behaviors,inspect.isclass)]
_BEHAVIOR_EVENTS = {behaviors.ButtonBehavior:['on_press','on_release']}
_CACHE_FILE = 'enaml-kivy.cache'

#: My tests show this is slower than not caching...
# def _load_cache():
#     try:
#         import jsonpickle as pickle
#         with open(_CACHE_FILE,'rb') as f:
#             cache = pickle.loads(f.read())
#         log.debug("Loaded enaml-kivy widgets from cache")
#         _CACHE.update(cache)
#     except Exception as e:
#         log.warn("Error loading enaml-kivy widgets from cache | {}".format(e))
#     finally:
#         _CACHE['loaded'] = True
# 
# def _save_cache():
#     """ Save the loaded classes into the cache file
#         of them have been imported.
#     """ 
#     _CACHE['updates'] -=1 
#     if _CACHE['updates']!=0:
#         return
#     try:
#         import jsonpickle as pickle
#         with open(_CACHE_FILE,'wb') as f:
#             f.write(pickle.dumps(_CACHE))
#         log.debug("Updated enaml-kivy widget cache")
#     except ImportError as e:
#         pass
#     except Exception as e:
#         log.warn("Error updating enaml-kivy widgets cache | {}".format(e))

# Manually implemented factories
def window_factory():
    from .kv_window import KvWindow
    return KvWindow


KV_FACTORIES = {
    'Window': window_factory,
}

class partialmethod(partial):
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return partial(self.func, instance,*(self.args or ()), **(self.keywords or {}))

def get_proxy(dotted_widget_name):
    """ Helper to get the enaml Proxy class for a given Kivy widget. 
    
    """
    widget_class = pydoc.locate(dotted_widget_name)
    return kivy_enaml_factory(widget_class)['proxy']

def get_control(dotted_widget_name,read_only_properties=None):
    """ Helper to get the enaml Control class for a given Kivy widget.
    
    Only actually loads the widget if it is needed. 
    
    """
    #if not _CACHE['loaded']:
    #    _load_cache()
    log.info("Enaml: Creating control for {}".format(dotted_widget_name))
    read_only_properties = read_only_properties or []
    widget_class = pydoc.locate(dotted_widget_name) if isinstance(dotted_widget_name,basestring) else dotted_widget_name
    return kivy_enaml_factory(widget_class,read_only_properties=read_only_properties)['control']

def get_factory(dotted_widget_name):
    """ Helper to get the enaml widget factory class for a given Kivy widget. 
    
    """
    return lambda:kivy_enaml_factory(pydoc.locate(dotted_widget_name))['widget']

def kivy_enaml_factory(widget_class,read_only_properties=None,widget_events=None):
    """ Generates the Enaml Control, Proxy, and Implementation classes for
    given Kivy widget so that it be used in an enaml file.
    
    Does this by converting the corresponding Kivy properties of the widget into
    atom properties. 
    
    """
    assert inspect.isclass(widget_class) and issubclass(widget_class, Widget), "Invalid widget class {}".format(widget_class)
    
    read_only_properties = read_only_properties or []
    widget_events = widget_events or []
    
    # Get file updated time
    #_updated_time = os.path.getmtime(inspect.getfile(widget_class))
    
    # Try to load from cache
    if widget_class in _CACHE:# and _CACHE[widget_class]['updated']==_updated_time:
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
    for cls in base_classes:
        if hasattr(cls,'__events__'):
            widget_events.extend(widget_class.__events__)
        if cls in [widget_class]:
            continue # Skip self
        elif issubclass(cls,Widget) and not _bases: # Find the first Widget superclass
            _bases = kivy_enaml_factory(cls,read_only_properties=read_only_properties)
            ProxyControlBase =_bases['proxy']
            ControlBase =_bases['control']
            KvWidgetBase = _bases['widget']
        # TODO: Handle behaviors
        else:
            
            behavior_properties.update(cls.__dict__.copy())
            if cls in _BEHAVIOR_EVENTS:
                widget_events.extend(_BEHAVIOR_EVENTS[cls])
    
    widget_name = widget_class.__name__
    
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
        elif isinstance(v,properties.Property):
            # Let type checking be done by Kivy Properties
            default_value = v.defaultvalue
            default_property_values[k] = default_value
            control_properties[k] = d_(Value(factory=lambda default_value=default_value:default_value),writable=is_writable)
            
        # Create setter method for this property
        if (k in control_properties) and (k not in widget_events) and (k not in excluded_properties) and (not k.startswith("_")):
            observed_properties.append(k)
            
            # TODO: Feedback loops are issues!
            
            # Write changes from Enaml to widget
            def set_property(self,value,k=k):
                
                #log.info("Enaml: {}.set_{}({})".format(self,k,value))
                key = (self,k)
                guards = self._guards
                if key not in guards:
                    guards.add(key)
                    try:
                        setattr(self.widget,k,value)
                    except (KeyError,AttributeError) as e:
                        msg = "Enaml: Could not set {}.{}: {}.".format(self,k,e)
                        if "read-only" in str(e):
                            msg+=" You probably want to add this to the read_only_properties list."
                        log.error(msg)   
                    finally:
                        guards.remove(key)
                        #raise
            
            # Read changes from widget to Enaml    
            def on_property(self,instance,value,k=k):
                #log.info("Enaml: {}.on_{}({},{})".format(self,k,instance,value))
                if self.declaration and self.widget:
                    key = (self,k)
                    guards = self._guards
                    if key not in guards:
                        guards.add(key)
                        try:
                            setattr(self.declaration,k,getattr(self.widget,k))
                        finally:
                            guards.remove(key)
            
            if is_writable:
                proxy_properties["set_{}".format(k)] = set_property
            proxy_properties["on_{}".format(k)] = on_property
                
        
    log.debug("Enaml:    Events: {}".format(widget_events))
    log.debug("Enaml:    Properties: {}".format(observed_properties))
    
    proxy_properties['declaration'] = Instance(Control)
    
    # This is used to prevent feedback loops when one property 
    # updates another property that updates the original property (creating a loop)
    proxy_properties['_guards'] = Typed(set,())    
    
    # Create the Proxy that defines what the implementation must implement
    ProxyWidgetControl = type("Proxy{}".format(widget_name),(ProxyControlBase,),proxy_properties)
    log.debug("Enaml:        Created proxy {} from {}".format(ProxyWidgetControl,proxy_properties))

        
    # Create the Enaml Control for this widget for use in enaml files
    # Create the Enaml ProxyControl for this widget
    @observe(*observed_properties)
    def _update_proxy(self, change):
        ControlBase._update_proxy(self,change)
        
    def __getattr__(self,name):
        """ Attempt to map function calls on the declaration to  
            the Kivy proxy widget so you don't have to use 
            self.proxy.widget.<method>() all the time
        """
        return getattr(self.proxy.widget,name)

    control_properties['proxy'] = Typed(ProxyWidgetControl)
    control_properties['_update_proxy'] = _update_proxy
    control_properties['__getattr__'] = __getattr__    
    WidgetControl = type(widget_name,(ControlBase,),control_properties)
    log.debug("Enaml:        Created control {} from {}".format(WidgetControl,control_properties))
    
    # Create the Enaml ToolkitObject for this widget
    def create_widget(self):
        #log.debug("{}.create_widget()".format(self))
        self.widget = widget_class()
        
        # Sync initial state of any properties NOT set in enaml
        d = self.declaration
        for p in observed_properties:
            try:
                value = getattr(d,p)
                if value==default_property_values[p]:
                    # Load initial state
                    setattr(d,p,getattr(self.widget,p))
            except TypeError as e:
                log.debug("Enaml: Failed to sync initial value for {} on {}. Reason: {}".format(p,self,e))

    
    def init_widget(self):
        """ Set initial values and connect signals"""
        #log.debug("{}.init_widget()".format(KvWidgetBase))
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
                    log.debug("Enaml: Failed to set initial value for {} on {}. Reason: {}".format(p,self,e))
            
            # Bind observers
            handler = getattr(self,"on_{}".format(p))
            binding = {p:handler}
            #log.debug("Enaml: {}.bind({})".format(self.widget,binding))
            self.widget.bind(**binding)
            
        # Connect signals so callbacks get handled by Enaml events
        for on_event in widget_events:
            handler = getattr(self,on_event)
            binding = {on_event:handler}
            #log.info("Enaml: {}.bind({})".format(self.widget,binding))
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
            if d is None:
                return # Already destroyed
            name = kwargs.pop('__event__')
            #log.debug("Enaml: {}.{}({})".format(self,name,args))
            event = getattr(d,name)
            #TODO: Is state already in sync?
            # Trigger enaml event
            event(args) # this doesnt do anything???
            
        widget_properties[e] = partialmethod(on_event,__event__=e)
    
    #: Create the Kivy implementation of this Enaml proxy widget
    
    KvWidgetImpl = type("Kv{}".format(widget_name),(KvWidgetBase,ProxyWidgetControl),widget_properties)
    log.debug("Enaml:        Created widget impl {} from {}".format(KvWidgetImpl,widget_properties))

    # Put in cache so we don't have to recreate later
    _CACHE[widget_class] = {
        'control':WidgetControl,
        'proxy':ProxyWidgetControl,
        'widget':KvWidgetImpl,
    #    'updated': _updated_time,
    }
    
    # Save the cache
    #_CACHE['updates'] +=1
    #timed_call(1000,_save_cache)
    
    # Automatically add
    if widget_name not in KV_FACTORIES:
        KV_FACTORIES[widget_name] = lambda:KvWidgetImpl # Does not work
    
    # Return classes
    return _CACHE[widget_class]





