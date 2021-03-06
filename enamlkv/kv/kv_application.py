#------------------------------------------------------------------------------
# Copyright (c) 2016, frmdstryr.
# Copyright (c) 2014, Nucleic Development Team.
#
# Distributed under the terms of the MIT License.
#
# The full license is in the file LICENSE, distributed with this software.
#------------------------------------------------------------------------------
import threading

from atom.api import Instance

from enaml.application import Application, ProxyResolver

from kivy.app import App
from kivy.uix.widget import Widget

from kivy.clock import Clock
from . import kv_factories
from .kv_mime_data import KvMimeData

class KvApplication(Application):
    """ A Kivy implementation of an Enaml application.

    An application that uses the Kivy toolkit to implement an Enaml UI that
    runs in the local process.

    """
    #: The private App instance.
    _kvapp = Instance(App)
    
    root = Instance(Widget)

    def __init__(self):
        """ Initialize a KvApplication.

        """
        super(KvApplication, self).__init__()
        self._kvapp = App()
        self._kvapp.build = self.build
        self.resolver = ProxyResolver(factories=kv_factories.KV_FACTORIES)
        kv_factories.KV_FACTORIES = self.resolver.factories # So any dynamic loads get added 
    
    @property
    def proxy(self):
        return self._kvapp

    #--------------------------------------------------------------------------
    # Abstract API Implementation
    #--------------------------------------------------------------------------
    def start(self):
        """ Start the application's main event loop.

        """
        app = self._kvapp
        if not getattr(app, '_in_event_loop', False):
            app._in_event_loop = True
            app.run()
            app._in_event_loop = False

    def stop(self):
        """ Stop the application's main event loop.

        """
        app = self._kvapp
        app.stop()
        app._in_event_loop = False

    def deferred_call(self, callback, *args, **kwargs):
        """ Invoke a callable on the next cycle of the main event loop
        thread.

        Parameters
        ----------
        callback : callable
            The callable object to execute at some point in the future.

        *args, **kwargs
            Any additional positional and keyword arguments to pass to
            the callback.

        """
        Clock.schedule_once(lambda dt,callback=callback,args=args,kwargs=kwargs:callback(*args, **kwargs))

    def timed_call(self, ms, callback, *args, **kwargs):
        """ Invoke a callable on the main event loop thread at a
        specified time in the future.

        Parameters
        ----------
        ms : int
            The time to delay, in milliseconds, before executing the
            callable.

        callback : callable
            The callable object to execute at some point in the future.

        *args, **kwargs
            Any additional positional and keyword arguments to pass to
            the callback.

        """
        Clock.schedule_once(lambda dt,ms=ms,callback=callback,args=args,kwargs=kwargs:callback(*args, **kwargs),ms/1000.0)

    def is_main_thread(self):
        """ Indicates whether the caller is on the main gui thread.

        Returns
        -------
        result : bool
            True if called from the main gui thread. False otherwise.

        """
        return threading.current_thread().name=='MainThread'

    def create_mime_data(self):
        """ Create a new mime data object to be filled by the user.

        Returns
        -------
        result : KvMimeData
            A concrete implementation of the MimeData class.

        """
        return KvMimeData()
    
    def create_proxy(self, declaration):
        proxy = super(KvApplication, self).create_proxy(declaration)
        #print("Created {} from {}".format(proxy,declaration))
        return proxy
    
    def build(self):
        return self.root
    