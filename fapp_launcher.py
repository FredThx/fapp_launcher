import pystray
from PIL import Image
from pathlib import Path
import os, sys
import argparse

class FAppLauncher:
    '''Un lanceur de raccourcis pour windows
    '''
    icon_path = "icon.jpg"
    sys_events = {
        'event_reload' : "Recharger",
        'event_open_folder' : "Ouvrir le repertoire",
        'event_quit' : "Quit",
    }

    def __init__(self, path:str|Path=None, title:str = "FAppLaucher"):
        self.path = Path(path) if path else None
        self.title = title
        self.icon = pystray.Icon("Fapplauncher",
                                 Image.open(self.resource_path(self.icon_path)),
                                 self.title)
        self.load_path()
        self.icon.run()

    def load_path(self, path:str|Path|None = None):
        '''read the path, populate self.shortcuts and update self.icon
        '''
        self.path = Path(path) if path else self.path
        try:
            self.shortcuts = [file for file in self.path.iterdir() if file.is_file()]
        except FileNotFoundError:
            self.shortcuts = []
        self.icon.menu = pystray.Menu(
                        *[pystray.MenuItem(link, self.on_event) for link in self.names],
                        pystray.MenuItem("----", None),
                        *[pystray.MenuItem(event, self.on_event) for event in self.sys_events.values()]
                        )
    @property
    def names(self)->list[str]:
        return [file.stem for file in self.shortcuts]

    def on_event(self, icon, query):
        print(f"{query=}")
        if str(query) == self.sys_events['event_quit']:
            icon.stop()
        elif str(query) == self.sys_events['event_reload']:
            self.load_path()
        elif str(query) == self.sys_events['event_open_folder']:
            os.startfile(self.path)
        # Gestion des liens
        elif str(query) in self.names:
            shortcut = [file for file in self.shortcuts if file.stem == str(query)][0]
            print(f"{shortcut=}")
            os.startfile(f"{shortcut}")

    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    parser =  argparse.ArgumentParser(
        prog="FappLauncher",
        description= "A systray launcher",
        epilog= "Thanks to use it. FredThx"
        )
    parser.add_argument('path', nargs='?', default='./menu', help = 'path with shortcuts or documents')
    parser.add_argument('title', nargs= '?', default=None, help="Title on systray")
    args = parser.parse_args()
    app = FAppLauncher(path = args.path,title=args.title)