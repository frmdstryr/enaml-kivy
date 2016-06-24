import enaml
from enamlkv.kv.kv_application import KvApplication

class EnamlKvApp(KvApplication):
    def build(self):
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
