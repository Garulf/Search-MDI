# -*- coding: utf-8 -*-
import json
import os

import win32clipboard


from flowlauncher import FlowLauncher, FlowLauncherAPI


MAX_RESULTS = 20
SVG_FILE = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="24" height="24" viewBox="0 0 24 24"><path d="{}" /></svg>'

class MDI(FlowLauncher):

    def __init__(self):
        self.result = []
        with open("./icons.json", "r", "utf-8") as f:
            self.icons = json.load(f)
        super().__init__()

    def filter(self, icon):
        if not os.path.isfile('./icons/{}.svg'.format(icon['name'])):
            with open('./icons/{}.svg'.format(icon['name']), 'w') as f:
                f.write(SVG_FILE.format(icon['data']))
        self.result.append(
            {
                "Title": icon['name'],
                "SubTitle": 'Press ENTER to copy to clipboard',
                "IcoPath": f'./icons/{icon["name"]}.svg',
                "JsonRPCAction": {
                    "method": "copy_to_clipboard",
                    "parameters": [icon['name']]
                }
            }
        )

    def query(self, query):
        f = codecs.open("./icons.json", "r", "utf-8")
        icons = json.load(f)
        f.close()
        result = []
        names = [icon['name'] for icon in icons['icons']]
        q = query.lower()
        
        if len(q) > 0:
            for icon in icons['icons']:
                # If only one char search by first letter only
                if len(q) < 2 and icon['name'].startswith(q):
                    self.filter(icon)
                elif len(q) > 1 and q in icon['name'] or q in icon['aliases']:
                    self.filter(icon)
                if len(self.result) >= MAX_RESULTS:
                    break
        else:
            self.result.append(
                {
                    "Title": 'Type more then 1 Character to begin search...',
                    "SubTitle": '...'
                }
            )
        return self.result

    def copy_to_clipboard(self, icon_name):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(icon_name)
        win32clipboard.CloseClipboard()


if __name__ == "__main__":
    MDI()
