# -*- coding: utf-8 -*-
import json
import os
import webbrowser

import pyperclip


try:
    from wox import Wox as FlowLauncher
except ModuleNotFoundError:
    from flowlauncher import FlowLauncher

ICON_FOLDER = './icons/'
MAX_RESULTS = 20
SVG_FILE = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="24" height="24" viewBox="0 0 24 24"><path d="{}" /></svg>'
MDI_URL = "https://materialdesignicons.com/icon/"

class MDI(FlowLauncher):

    def __init__(self):

        self.results = []
        with open("./plugin/icons.json", "r") as f:
            self.icons = json.load(f)
        if not os.path.exists(ICON_FOLDER):
            os.mkdir(ICON_FOLDER)
        super().__init__()

    def filter(self, icon):

        if not os.path.isfile(f"{ICON_FOLDER}{icon['name']}.svg"):
            with open(f"{ICON_FOLDER}{icon['name']}.svg", 'w') as f:
                f.write(SVG_FILE.format(icon['data']))
        self.add_item(
            title=icon['name'],
            subtitle='Press ENTER to copy to clipboard (SHIFT+ENTER for more options)',
            icon=icon["name"],
            context=[icon["name"]],
            method="copy_to_clipboard",
            parameters= [icon['name']]
        )

    def add_item(self, title, subtitle='', icon=None, method=None, parameters=None, context=None, hide=False):
        icon = f"{ICON_FOLDER}{icon}.svg"
        
        item = {
            "Title": title,
            "SubTitle": subtitle,
            "IcoPath": icon,
            "ContextData": context,
            "JsonRPCAction": {}
        }
        item['JsonRPCAction']['method'] = method
        item['JsonRPCAction']['parameters'] = parameters
        item['JsonRPCAction']['dontHideAfterAction'] = hide        
        self.results.append(item)

    def context_menu(self, data):
        self.add_item(
            title='View icon on website',
            subtitle=f"{MDI_URL}{data[0]}",
            method="open_web",
            parameters=[data[0]]
        )
        return self.results

    def query(self, query):
        # names = [icon['name'] for icon in icons['icons']]
        q = query.lower()
        
        if len(q) > 0:
            for icon in self.icons['icons']:
                # If only one char search by first letter only
                if len(q) < 2 and icon['name'].startswith(q):
                    self.filter(icon)
                elif len(q) > 1 and q in icon['name'] or q in icon['aliases']:
                    self.filter(icon)
                if len(self.results) >= MAX_RESULTS:
                    break
        else:
            self.results.append(
                {
                    "Title": 'Please enter your search term',
                    "SubTitle": '...'
                }
            )
        return self.results[:10]


    def copy_to_clipboard(self, icon_name):
        pyperclip.copy(icon_name)

    def open_web(self, icon_name):
        webbrowser.open(f"{MDI_URL}{icon_name}")

if __name__ == "__main__":
    MDI()
