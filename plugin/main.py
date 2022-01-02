# -*- coding: utf-8 -*-
import json
import os
import webbrowser
from pathlib import Path


from flox import Flox, Clipboard


META_FILE = "meta.json"
META_PATH = Path(Path.cwd(), META_FILE)
MAX_RESULTS = 100
MDI_URL = "https://materialdesignicons.com/icon/"


class MDI(Flox):
    def __init__(self):
        with open(META_PATH, "r") as f:
            self.icons = json.load(f)
        super().__init__()

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
            self.add_item(
                title=icon["name"],
            )
            

        return self._results

    def copy_to_clipboard(self, icon_name):
        pyperclip.copy(icon_name)

    def open_web(self, icon_name):
        webbrowser.open(f"{MDI_URL}{icon_name}")


if __name__ == "__main__":
    MDI()
