# -*- coding: utf-8 -*-
import json
import os
import webbrowser
from pathlib import Path
from difflib import SequenceMatcher as sm


from flox import Flox, Clipboard, ICON_BROWSER


META_FILE = "meta.json"
META_PATH = Path(Path.cwd(), 'plugin', META_FILE)
MAX_RESULTS = 100
MDI_URL = "https://materialdesignicons.com/icon/"


class MDI(Flox, Clipboard):
    def __init__(self):
        with open(META_PATH, "r") as f:
            self.icons = json.load(f)
        super().__init__()

    def context_menu(self, data):
        name = data[0]
        self.add_item(
            title="View icon on website",
            subtitle=f"{MDI_URL}{name}",
            icon=ICON_BROWSER,
            method="open_web",
            parameters=[data[0]],
        )
        return self._results

    def codepoint_to_char(self, codepoint):
        return chr(int(codepoint, 16))

    def match(self, query, icon_name, aliases):
        query = query.lower()
        score = []
        for alias in aliases:
            _ = sm(lambda x: x==" " or x=="-", query, alias.lower())
            score.append(_.ratio() * 100)
        _ = sm(lambda x: x==" " or x=="-", query, icon_name.lower())
        score.append(_.ratio() * 100)
        return max(score)

    def query(self, query):
        for icon in self.icons:
            score = self.match(query, icon["name"], icon['aliases'])
            if score > 50 or query == '':
                self.add_item(
                    title=icon["name"],
                    subtitle=", ".join(icon['aliases']),
                    glyph=self.codepoint_to_char(icon["codepoint"]),
                    font_family=str(
                                Path(self.plugindir).joinpath(
                                    'plugin',
                                    "#Material Design Icons Desktop"
                                )
                    ),
                    score=int(score),
                    context=[icon["name"]],
                    method=self.put,
                    parameters=[icon["name"]],
                )

    def open_web(self, icon_name):
        webbrowser.open(f"{MDI_URL}{icon_name}")


if __name__ == "__main__":
    MDI()
