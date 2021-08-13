# -*- coding: utf-8 -*-
import json
import os
import webbrowser


from flox import Flox

import pyperclip

ICON_FOLDER = "./icons/"
MAX_RESULTS = 100
SVG_FILE = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="24" height="24" viewBox="0 0 24 24"><path d="{}" /></svg>'
MDI_URL = "https://materialdesignicons.com/icon/"


class MDI(Flox):
    def __init__(self):
        with open("./plugin/icons.json", "r") as f:
            self.icons = json.load(f)
        if not os.path.exists(ICON_FOLDER):
            os.mkdir(ICON_FOLDER)
        super().__init__()

    def create_icon(self, icon_name):
        if not os.path.isfile(f"{ICON_FOLDER}{icon_name}.svg"):
            for icon in self.icons["icons"]:
                if icon["name"] == icon_name:
                    with open(f"{ICON_FOLDER}{icon['name']}.svg", "w") as f:
                        f.write(SVG_FILE.format(icon["data"]))
        return f"{ICON_FOLDER}{icon_name}.svg"

    def filter(self, icon):

        self.add_item(
            title=icon["name"],
            subtitle="Press ENTER to copy to clipboard (SHIFT+ENTER for more options)",
            icon=self.create_icon(icon["name"]),
            context=[icon["name"]],
            method="copy_to_clipboard",
            parameters=[icon["name"]],
        )

    def context_menu(self, data):
        self.add_item(
            title="View icon on website",
            subtitle=f"{MDI_URL}{data[0]}",
            icon=self.create_icon("web"),
            method="open_web",
            parameters=[data[0]],
        )
        return self._results

    def query(self, query):
        # names = [icon['name'] for icon in icons['icons']]
        q = query.lower()

        for icon in self.icons["icons"]:
            # If only one char search by first letter only
            if len(q) < 2 and icon["name"].startswith(q):
                self.filter(icon)
            elif len(q) > 1 and q in icon["name"] or q in icon["aliases"]:
                self.filter(icon)
            if len(self._results) >= MAX_RESULTS:
                break

        return self._results

    def copy_to_clipboard(self, icon_name):
        pyperclip.copy(icon_name)

    def open_web(self, icon_name):
        webbrowser.open(f"{MDI_URL}{icon_name}")


if __name__ == "__main__":
    MDI()
