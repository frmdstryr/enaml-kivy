#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import Instance, atomref

from enaml.layout.geometry import Pos, Rect, Size
from enaml.widgets.window import ProxyWindow, CloseEvent

#from .QtCore import Qt, QPoint, QRect, QSize
#from .QtGui import QApplication, QIcon


from .k_deferred_caller import deferredCall
from .kv_widget import KvWidget
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from enamlkv.kv.kv_application import KvApplication


# MODALITY = {
#     'non_modal': Qt.NonModal,
#     'application_modal': Qt.ApplicationModal,
#     'window_modal': Qt.WindowModal,
# }


def finalize_close(d):
    """ Finalize the closing of the declaration object.

    This is performed as a deferred call so that the window may fully
    close before the declaration is potentially destroyed.

    """
    d.visible = False
    d.closed()
    if d.destroy_on_close:
        d.destroy()


# class KWindow(KWindowBase):
#     """ A window base subclass which handles the close event.
# 
#     The window layout computes the min/max size of the window based
#     on its central widget, unless the user explicitly changes them.
# 
#     """
#     def __init__(self, proxy, parent=None, flags=0):
#         """ Initialize a QWindow.
# 
#         Parameters
#         ----------
#         proxy : QtWindow
#             The proxy object which owns this window. Only an atomref
#             will be maintained to this object.
# 
#         parent : QWidget, optional
#             The parent of the window.
# 
#         flags : Qt.WindowFlags, optional
#             The window flags to pass to the parent constructor.
# 
#         """
#         super(KWindow, self).__init__(parent)#, Qt.Window | flags)
#         self._proxy_ref = atomref(proxy)
# 
#     def closeEvent(self, event):
#         """ Handle the close event for the window.
# 
#         """
#         event.accept()
#         if not self._proxy_ref:
#             return
#         proxy = self._proxy_ref()
#         d = proxy.declaration
#         d_event = CloseEvent()
#         d.closing(d_event)
#         if d_event.is_accepted():
#             deferredCall(finalize_close, d)
#         else:
#             event.ignore()


class KvWindow(KvWidget, ProxyWindow):
    """ A Qt implementation of an Enaml ProxyWindow.

    """
    #: A reference to the toolkit widget created by the proxy.
    widget = Instance(Widget)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the QWindow widget.

        """
        app = KvApplication.instance()
        self.widget = FloatLayout()
        app.root = self.widget

    def init_widget(self):
        """ Initialize the widget.

        """
        super(KvWindow, self).init_widget()
        d = self.declaration
        if d.title:
            self.set_title(d.title)
        if -1 not in d.initial_size:
            self.widget.size = d.initial_size
        if -1 not in d.initial_position:
            self.widget.position = d.initial_position
        if d.modality != 'non_modal':
            self.set_modality(d.modality)
        if d.icon:
            self.set_icon(d.icon)

    def init_layout(self):
        """ Initialize the widget layout.

        """
        super(KvWindow, self).init_layout()
#        for widget in self.child_widgets():
#            self.widget.add_widget(widget)

    #--------------------------------------------------------------------------
    # Public API
    #--------------------------------------------------------------------------
    def central_widget(self):
        """ Find and return the central widget child for this widget.

        Returns
        -------
        result : QWidget or None
            The central widget defined for this widget, or None if one
            is not defined.

        """
        d = self.declaration.central_widget()
        if d is not None:
            return d.proxy.widget

    #--------------------------------------------------------------------------
    # Child Events
    #--------------------------------------------------------------------------
    def child_added(self, child):
        """ Handle the child added event for a QtWindow.

        """
        super(KvWindow, self).child_added(child)
        if isinstance(child, KvWidget):
            self.widget.add_widget(child.widget)

    def child_removed(self, child):
        """ Handle the child added event for a QtWindow.

        """
        super(KvWindow, self).child_removed(child)
        if isinstance(child, KvWidget):
            self.widget.remove_widget(child.widget)

    #--------------------------------------------------------------------------
    # ProxyWindow API
    #--------------------------------------------------------------------------
    def set_title(self, title):
        """ Set the title of the window.

        """
        app = KvApplication.instance()
        app.proxy.title = str(title)

    def set_modality(self, modality):
        """ Set the modality of the window.

        """
        print("set_modality not implemented!")
        return 
        self.widget.setWindowModality(MODALITY[modality])

    def set_icon(self, icon):
        """ Set the window icon.

        """
        app = KvApplication.instance()
        app.proxy.icon = str(icon)
        return

    def position(self):
        """ Get the position of the of the window.

        """
        return Pos(*self.widget.position)

    def set_position(self, pos):
        """ Set the position of the window.

        """
        self.widget.move(*pos)

    def size(self):
        """ Get the size of the window.

        """
        return Size(*self.widget.size)

    def set_size(self, size):
        """ Set the size of the window.

        """
        size = QSize(*size)
        if size.isValid():
            self.widget.resize(size)

    def geometry(self):
        """ Get the geometry of the window.

        """
        return Rect(self.widget.x, self.widget.y, self.widget.width, self.widget.height)

    def set_geometry(self, rect):
        """ Set the geometry of the window.

        """
        rect = QRect(*rect)
        if rect.isValid():
            self.widget.setGeometry(rect)

    def frame_geometry(self):
        """ Get the geometry of the window.

        """
        rect = self.widget.frameGeometry()
        return Rect(rect.x(), rect.y(), rect.width(), rect.height())

    def maximize(self):
        """ Maximize the window.

        """
        self.widget.maximize()

    def is_maximized(self):
        """ Get whether the window is maximized.

        """
        return bool(self.widget.windowState() & Qt.WindowMaximized)

    def minimize(self):
        """ Minimize the window.

        """
        self.widget.minimize()

    def is_minimized(self):
        """ Get whether the window is minimized.

        """
        return bool(self.widget.windowState() & Qt.WindowMinimized)

    def restore(self):
        """ Restore the window after a minimize or maximize.

        """
        self.widget.restore()

    def send_to_front(self):
        """ Move the window to the top of the Z order.

        """
        self.widget.raise_window()

    def send_to_back(self):
        """ Move the window to the bottom of the Z order.

        """
        #self.widget.lo
        pass

    def activate_window(self):
        """ Activate the underlying window widget.

        """
        pass
        #self.widget.activateWindow()
        #if sys.platform == 'win32':
        #    # For some reason, this needs to be called twice on Windows
        #    # in order to get the taskbar entry to flash.
        #    self.widget.activateWindow()

    def center_on_screen(self):
        """ Center the window on the screen.

        """
        widget = self.widget
        rect = QRect(QPoint(0, 0), widget.frameGeometry().size())
        geo = QApplication.desktop().screenGeometry(widget)
        widget.move(geo.center() - rect.center())

    def center_on_widget(self, other):
        """ Center the window on another widget.

        """
        widget = self.widget
        rect = QRect(QPoint(0, 0), widget.frameGeometry().size())
        other_widget = other.proxy.widget
        if other_widget.isWindow():
            geo = other_widget.frameGeometry()
        else:
            size = other_widget.size()
            point = other_widget.mapToGlobal(QPoint(0, 0))
            geo = QRect(point, size)
        widget.move(geo.center() - rect.center())

    def close(self):
        """ Close the window.

        """
        self.widget.close()
