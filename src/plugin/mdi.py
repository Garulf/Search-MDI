import asyncio
from pathlib import Path
from typing import List, Optional

from pyflowlauncher import Plugin, Result
from pyflowlauncher.models.result import Glyph, PreviewInfo

import icons
from launcher import KeywordLauncher

MDI_URL = "https://materialdesignicons.com/icon/"
PLUGIN_ICON = str(Path(__file__).resolve().parent.parent / "icon.png")
ICONS_PER_YIELD = 250

plugin = Plugin(launcher=KeywordLauncher())
ICONS = icons.load_icons()


def icon_url(name: str) -> str:
    return f"{MDI_URL}{name}"


def auto_complete_text(name: str) -> str:
    keyword = plugin.launcher.action_keyword
    return f"{keyword} {name}" if keyword else name


def preview(description: str) -> PreviewInfo:
    return PreviewInfo(PreviewImagePath=None, Description=description, IsMedia=False, PreviewDeligate=None)


def icon_result(icon: icons.Icon, icon_score: float) -> Result:
    return Result(
        title=icon.name,
        subtitle=", ".join(icon.aliases),
        icon=PLUGIN_ICON,
        score=int(icon_score),
        glyph=Glyph(Glyph=icon.glyph, FontFamily=icons.FONT_FAMILY),
        context_data=[icon.name],
        auto_complete_text=auto_complete_text(icon.name),
        preview=preview(icon.name),
    ).add_action(plugin.launcher.api.copy_to_clipboard(icon.name, show_default_notification=False))


@plugin.on_method
async def query(query: str):
    for index, icon in enumerate(ICONS):
        if index % ICONS_PER_YIELD == 0:
            await asyncio.sleep(0)
        icon_score = icons.score(query, icon)
        if icons.matches(query, icon_score):
            yield icon_result(icon, icon_score)


def context_menu(data: Optional[List[str]]) -> List[Result]:
    if not data:
        return []
    url = icon_url(data[0])
    return [
        Result(
            title="View icon on website",
            subtitle=url,
            icon=plugin.launcher.icons.browser or PLUGIN_ICON,
            preview=preview(url),
        ).add_action(plugin.launcher.api.open_url(url))
    ]


plugin.add_method(context_menu, name="context_menu")
