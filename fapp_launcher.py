import PySimpleGUI as sg
from psgtray import SystemTray
from pathlib import Path
import os

class FAppLauncher:
    '''Un lanceur de raccourcis pour windows
    '''

    def __init__(self, path:str|Path=None, title:str = "FAppLaucher", tooltip:str=None):
        self.path = Path(path) if path else None
        self.title = title
        self.tooltip = tooltip or self.title
        self.shortcuts = [file for file in self.path.iterdir() if file.is_file()]
        menu = ['', self.names + ['---','Parametres','Quitter']]

        layout = [[sg.Text("Lanceur d'applications ")],
                [sg.T('Repertoire des raccourcis:'), sg.Input(self.path or "", key='-IN-', s=(20,1)), sg.B('TODO : change')],
                [sg.B('Masquer'), sg.Button('Quitter')]]

        self.window = sg.Window(self.title, layout, finalize=True, enable_close_attempted_event=True)
        self.window.hide()
        
        self.tray = SystemTray(menu, single_click_events=False, window=self.window, tooltip=self.tooltip, icon="OLFA-LOGO_200_132.jpg")

    @property
    def names(self)->list[str]:
        return [file.stem for file in self.shortcuts]

    def main(self):
        while True:
            event, values = self.window.read()
            if event == self.tray.key:
                print(f'System Tray Event = {values[event]}')
                event = values[event]       # use the System Tray's event as if was from the window
            print(event, values)
            # Fermeture Application
            if event in (sg.WIN_CLOSED, 'Quitter'):
                break
            # Fenetre principale (parametres)
            if event in ("Parametres", sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
                self.window.un_hide()
                self.window.bring_to_front()
            elif event in ('Masquer', sg.WIN_CLOSE_ATTEMPTED_EVENT):
                self.window.hide()
                self.tray.show_icon()
            # Gestion des liens
            elif event in self.names:
                shortcut = [file for file in self.shortcuts if file.stem == event][0]
                print(f"{shortcut=}")
                os.startfile(f"{shortcut}")
        self.tray.close()
        self.window.close()

if __name__ == '__main__':
    app = FAppLauncher(path = r'\\SRV-DATA\commun\Applications OLFA\Applications OLFA',tooltip="Applications OLFA")
    app.main()