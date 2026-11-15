import asyncio

import pytest

import mdi


def run_query(text):
    async def collect():
        return [result async for result in mdi.query(text)]

    return asyncio.run(collect())


@pytest.fixture
def action_keyword():
    launcher = mdi.plugin.launcher
    launcher.action_keyword = "mdi"
    yield launcher
    launcher.action_keyword = ""
