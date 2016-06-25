import enaml
import os
import widgets
from enamlkv.kv.kv_application import KvApplication
from kivymd.theming import ThemeManager

class EnamlKvApp(KvApplication):
    def build(self):
        self._kvapp.theme_cls = ThemeManager()
        with enaml.imports():
            from view import Main
            
        view = Main()
        view.show()
        
        return super(EnamlKvApp, self).build()

def main():
    app = EnamlKvApp()
    app.start()


if __name__ == "__main__":
    main()
