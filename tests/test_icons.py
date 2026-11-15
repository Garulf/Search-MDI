import json

import pytest

import icons
from icons import Icon


def test_shipped_icon_set_loads():
    loaded = icons.load_icons()
    assert len(loaded) == 6595
    assert loaded[0] == Icon("ab-testing", [], "F01C9")


def test_glyph_is_the_codepoint_character():
    assert Icon("home", [], "F02DC").glyph == "\U000F02DC"


def test_load_icons_tolerates_missing_aliases(tmp_path):
    meta = tmp_path / "meta.json"
    meta.write_text(json.dumps([{"name": "home", "codepoint": "F02DC"}]), encoding="utf-8")
    assert icons.load_icons(meta) == [Icon("home", [], "F02DC")]


def test_exact_name_scores_100():
    assert icons.score("home", Icon("home", ["house"], "F02DC")) == 100


def test_best_of_name_and_aliases_wins():
    icon = Icon("home", ["house", "home-outline"], "F02DC")
    assert icons.score("HOUSE", icon) == 100


def test_unrelated_query_scores_low():
    assert icons.score("zzz", Icon("home", ["house"], "F02DC")) == 0


@pytest.mark.parametrize(
    "query, icon_score, expected",
    [("", 0, True), ("home", 100, True), ("home", 50, False), ("home", 51, True)],
)
def test_matches(query, icon_score, expected):
    assert icons.matches(query, icon_score) is expected


def test_font_family_points_at_the_shipped_font():
    font_dir, family = icons.FONT_FAMILY.rsplit("#", 1)
    assert family == "Material Design Icons Desktop"
    assert (icons.ASSETS_DIR / "MaterialDesignIconsDesktop.ttf").is_file()
    assert font_dir.rstrip("/\\") == str(icons.ASSETS_DIR)
