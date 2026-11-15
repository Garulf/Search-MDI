import json

import icons
import mdi
from conftest import run_query


def by_title(results):
    return {result.title: result for result in results}


def test_empty_query_lists_every_icon():
    results = run_query("")
    assert len(results) == len(mdi.ICONS)
    assert {result.score for result in results} == {0}


def test_query_returns_matching_icons_with_scores():
    results = by_title(run_query("home"))
    assert results["home"].score == 100
    assert "zzz" not in results
    assert all(result.score > icons.MATCH_THRESHOLD for result in results.values())


def test_result_shows_the_icon_glyph_and_aliases():
    home = by_title(run_query("home"))["home"].to_json()
    assert home["Glyph"] == {"Glyph": "\U000F02DC", "FontFamily": icons.FONT_FAMILY}
    assert home["SubTitle"] == ", ".join(next(icon.aliases for icon in mdi.ICONS if icon.name == "home"))
    assert home["IcoPath"] == mdi.PLUGIN_ICON
    assert home["ContextData"] == ["home"]


def test_selecting_a_result_copies_the_icon_name():
    home = by_title(run_query("home"))["home"]
    assert home.json_rpc_action == {
        "Method": "Flow.Launcher.CopyToClipboard",
        "Parameters": ["home", False, False],
        "DontHideAfterAction": False,
    }


def test_auto_complete_includes_the_action_keyword(action_keyword):
    home = by_title(run_query("home"))["home"]
    assert home.auto_complete_text == "mdi home"


def test_auto_complete_without_keyword_for_global_queries():
    home = by_title(run_query("home"))["home"]
    assert home.auto_complete_text == "home"


def test_results_always_carry_a_preview():
    home = by_title(run_query("home"))["home"].to_json()
    assert home["Preview"] is not None


def test_results_serialize_to_json():
    json.dumps([result.to_json() for result in run_query("account")])


def test_context_menu_opens_the_icon_page():
    (item,) = mdi.context_menu(["home"])
    assert item.title == "View icon on website"
    assert item.subtitle == mdi.icon_url("home")
    assert item.json_rpc_action["Method"] == "Flow.Launcher.OpenUrl"
    assert item.json_rpc_action["Parameters"] == [mdi.icon_url("home"), False]
    assert item.to_json()["Preview"] is not None


def test_context_menu_without_data_is_empty():
    assert mdi.context_menu([]) == []
    assert mdi.context_menu(None) == []
